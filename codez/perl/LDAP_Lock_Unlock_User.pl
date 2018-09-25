#!/usr/bin/perl
# LDAP_Lock_Unlock_User.pl
# chris.downs\@reticulipictures.com
#
# Add Administrative openldap lock / unlock --

use strict;
use warnings;
use Net::LDAP;
use Getopt::Std;
use Term::ReadKey;

# Vars
my $epoch = int(time/(60*60*24));
my $ver = '1.1';

# Args
my %args;
getopts("CPluU:?", \%args);
if ( $args{l} || $args{u} ) {
    my $User = $args{U};
    if ( $args{C} ) {
        &pwdAccountLockedTime($User,$args{C});
        } elsif ( $args{P} ) {
            &pwdAccountLockedTime($User,$args{P});
    } else {
        &Usage()
    }
}
if ( $args{"?"} ) {
    &Usage();
}

sub pwdAccountLockedTime() { 
    my $User = shift;
    my $args = shift;
    my ($dn, $Shell);
    if ( $args{C} ) {
        $dn = "uid=$User,ou=Customers,dc=somecompay,dc=com";
    } 
    elsif ( $args{P} ) {
        $dn = "uid=$User,ou=People,dc=somecompay,dc=com";
    }
    print "DN: $dn\n";
    my $ldap = Net::LDAP->new( 'ldaps://ldap.somecompay.com' )
        or die "LDAPS Connection Failed! $@\n";

    print "Please enter the master LDAP password: ";
    ReadMode('noecho');
    my $ldappasswd = <STDIN>;
    ReadMode(0);
    print "\n";
    chomp $ldappasswd;
    $ldap->bind( 'cn=Manager,dc=somecompay,dc=com',
	        password => $ldappasswd );
    if ( $args{l} ) {
        print "Locking Account: $User\n";
        if ( $args{C} ) {
            print "Setting loginShell: /sbin/nologin\n";
            $Shell = '/sbin/nologin';
        } 
        elsif ( $args{P} ) {
            print "Setting loginShell: /bin/false\n";
            $Shell = '/bin/false';
        }
        my $lock = $ldap->modify( $dn, 
            changes => [
                add => [ 'pwdAccountLockedTime' => '000001010000Z'],
            replace => [ 'loginShell' => $Shell]
            ]
        );
        $lock->code && warn "failed to add entry: ", $lock->error;
        $lock = $ldap->unbind;
    }
    if ( $args{u} ) {
        print "Unlocking Account: $User\n";
        if ( $args{C} ) {
            print "Setting loginShell: /sbin/nologin\n";
            $Shell = '/sbin/nologin';
        } 
        elsif ( $args{P} ) {
            print "Setting loginShell: /bin/bash\n";
            $Shell = '/bin/bash';
        }
        my $unlock = $ldap->modify( $dn,
            changes => [
             delete => [ 'pwdAccountLockedTime' => '000001010000Z'],
            replace => [ 'loginShell' => $Shell]
            ]
        );
        $unlock->code && warn "failed to delete entry: ", $unlock->error;
        $unlock = $ldap->unbind;
    }
}

sub Usage {
    print <<USAGE;
LDAP_Lock_Unlock_User.pl v:$ver
Usage: LDAP_Lock_Unlock_User.pl CPluU? <username>
    -P ou=People
    -C ou=Customers
    -l Lock Account
    -u Unlock Account 
    -U Username 
    -? This Menu

Examples:
    perl LDAP_Lock_Unlock_User.pl -P -l -U cdowns 
    perl LDAP_Lock_Unlock_User.pl -P -u -U cdowns 
    perl LDAP_Lock_Unlock_User.pl -C -l -U 99Only 
    perl LDAP_Lock_Unlock_User.pl -C -u -U 99Only 

USAGE
exit;
}
