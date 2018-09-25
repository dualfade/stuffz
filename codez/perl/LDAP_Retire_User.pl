#!/usr/bin/perl
# chris.downs\@reticulipictures.com
# LDAP administrative lock / mv to ou=FormerPeople
# Well you know.... In case they ever come back.

use strict;
use Net::LDAP;
use Term::ReadKey;

my $username = $ARGV[0];
if ( ! ($username =~ /^[a-zA-Z0-9\-_]+$/) ) {
    die "You specified a username of '$username', which does not look valid.\n";
}

my $privatefile = "/etc/pki/somecompany/private/ldap-mgr.txt";
open PRIVATE, "$privatefile" or die "Could not open $privatefile: $!\n";
my $ldappasswd = <PRIVATE>;
chomp $ldappasswd;
close PRIVATE;

my $ldap = Net::LDAP->new( 'ldaps://ldap.somecompany.com' );
my $res = $ldap->bind( 'cn=Manager,dc=somecompany,dc=com', password => $ldappasswd);

if ($res->code) {
    die "Error binding to LDAP: ". $res->error ."\n";
}

$res = $ldap->search( scope=>"one",
                      filter=> "(&(objectClass=posixAccount)(uid=$username))",
                      attrs=> ["uid","uidNumber","givenName","sn","loginShell","userpassword"],
                      base=>"ou=People,dc=somecompany,dc=com" );

if ($res->code) {
    die "Error searching LDAP: ". $res->error ."\n";
}
if ($res->count == 0) {
    die "Count not locate an LDAP user named $username\n";
}

my @entries = $res->entries;
my $account = shift @entries;
my $uid = $account->get_value("uidNumber");
my $fn = $account->get_value("givenName");
my $ln = $account->get_value("sn");
my $shell = $account->get_value("loginShell");
my $passhash = $account->get_value("userpassword");

print "username: $fn $ln ($username)\n";
print "UID: $uid\n";
print "Shell: $shell\n";

if ($passhash =~ s/^{(CRYPT|SSHA)}/{$1}!!/) {
    $account->replace ( "userpassword" => $passhash ); 
    $account->replace ( "loginShell" => "/bin/false" );
    $account->replace ( "pwdAccountLockedTime" => "000001010000Z" );
    $res = $account->update($ldap);
    if ($res->code) {
        print "Failed to lock account: ". $res->error ."\n";
    }
    my $groups = $ldap->search(
        base => "ou=Group,dc=somecompany,dc=com",
        filter => "(&(objectClass=posixGroup)(memberuid=$username))",
        attr   => ["cn"]
    );
    if ($groups->count == 0) {
        print "Couldn't find any group membership. That's ok.\n";
        &MovetoFormerPeople($username);        
    } else {
        foreach my $grp ($groups->entries) {
            my $grpdn = $grp->dn;
            my $grpname = $grp->get_value("cn");
            $grp->delete ( "memberuid" => $username );
            $res = $grp->update($ldap);
            if ($res->code) {
                print "Failed to remove from $grpname: ". $res->error ."\n";
                print "You should investigate the move to new superior.\n";
                print "You can manually do this with cr-move-to-formerpeople.pl -U <username>\n";
                print "This script will move the user to the ou=FormerPeople LDAP Branch\n";
            } else {
                print "Removed $username from $grpname.\n";
                &MovetoFormerPeople($username);        
            }
        }
    }
} else {
    die "There's something odd about their password hash.\nAborting...\n";
}

sub MovetoFormerPeople() {
    my $username = shift;
    my $B  = 'dc=somecompany,dc=com';
    my $P  = 'ou=People,dc=somecompany,dc=com';
    my $G  = 'ou=Group,ou=People,dc=somecompany,dc=com';
    my $FP = 'ou=FormerPeople,dc=somecompany,dc=com';
    my $FG = 'ou=Group,ou=FormerPeople,dc=somecompany,dc=com';

    my $ldap = Net::LDAP->new( 'ldaps://ldap.somecompany.com' )
        or die "LDAPS Connection Failed! $@\n";

    my $privatefile = "/etc/pki/somecompany/private/ldap-mgr.txt";
    open PRIVATE, "$privatefile" or die "Could not open $privatefile: $!\n";
    my $ldappasswd = <PRIVATE>;
    chomp $ldappasswd;
    close PRIVATE;

    $ldap->bind( 'cn=Manager,dc=somecompany,dc=com',
        password => $ldappasswd );

    print "Modifying rdn to newsuperior: uid=$username,$FP\n";
    print "Modifying rdg to newsuperior: cn=$username,$FG\n";
    my $rdn = 'uid=' . $username .',' . $P;
    my $rdg = 'cn=' . $username . ',' . $G;
    my $nrdn = 'uid=' . $username;
    my $nrdg = 'cn=' . $username;
    my $result = $ldap->moddn ( $rdn,
        newrdn => $nrdn,
        deleteoldrdn => '1',
        newsuperior => $FP
   );
    $result = $ldap->moddn ( $rdg,
        newrdn => $nrdg,
        deleteoldrdn => '1',
        newsuperior => $FG
   );
   return $result;
   $result = $ldap->unbind; 
}

