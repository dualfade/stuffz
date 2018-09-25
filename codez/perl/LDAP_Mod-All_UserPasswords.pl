#!/usr/bin/perl 

use strict;
use warnings;

open (FILE, "</home/cdowns/Scripts/ldap_Users.txt")
	or die "Cannot open 'filename' $!\n";
while (<FILE>) {
	my ($f1,$f2,$f3) = split(/:/, $_);
	system (`/usr/bin/ldapmodify -H ldaps://master.ldap.somecompany.com -D "cn=Manager,dc=somecompany,dc=com" -W -x -f`);
	&LDIF($f1,$f2);
}
close(FILE);

sub LDIF {
	my $f1 = shift;
	my $f2 = shift;
	print <<LDIF;
dn: uid=$f1,ou=People,dc=somecompany,dc=com
changetype: modify
replace: userpassword
userpassword: {CRYPT}$f2
LDIF
sleep 1;
exit;
}
