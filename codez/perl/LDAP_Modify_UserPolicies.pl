#!/usr/bin/perl
# LDAP_Modify_UserPolicies.pl
# chris.downs\@reticulipictures.com

use strict;
use warnings;
use Net::LDAP;
use Term::ReadKey;

my $epoch = int(time/(60*60*24));
my $ldap = Net::LDAP->new( 'ldaps://ldap.somecompany.com' )
    or die "LDAPS Connection Failed! $@\n";

print "Please enter the master LDAP password: ";
ReadMode('noecho');
my $ldappasswd = <STDIN>;
ReadMode(0);
print "\n";
chomp $ldappasswd;
$ldap->bind( 'cn=Manager,dc=somecompany,dc=com',
	      password => $ldappasswd);

my $mesg = $ldap->search( 
   		base => "ou=People,dc=somecompany,dc=com",
   		filter => "(objectClass=posixAccount)",
		attr   => ["uid=*"],
	);
$mesg->code && die $mesg->error;
my $entr;
my $dn;
my $pass;
my @entries = $mesg->entries;
foreach $entr ( @entries ) {
    print "DN: ", $entr->dn, "\n";
    $dn = $entr->dn;
    $pass = $entr->get_value ("userpassword");
    &Add_Policy($dn, $pass);
    print "-----------------------------------------\n";
}
$mesg = $ldap->unbind;

sub Add_Policy() {
    my $dn = shift;
    my $pass = shift;
#    my $policy_modify = $ldap->modify( $dn,
#        add => {
#            'pwdPolicySubentry' => ['cn=People,ou=policies,dc=somecompany,dc=com']
#        }
#    );
#    $policy_modify->code && warn "failed to add entry: ", $policy_modify->error ;
    my $passwd_modify = $ldap->modify( $dn,
        replace => {
            'userpassword' => [$pass]
        }
    );
    $passwd_modify->code && warn "failed to add entry: ", $passwd_modify->error ;
}
