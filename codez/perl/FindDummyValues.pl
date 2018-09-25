#!/usr/bin/perl
# FindDummy_Values.pl 
# chris.downs\@reticulipictures.com

use strict;
use warnings;
use Getopt::Std;

#Args
my %args;
getopts("e:?", \%args);
if ( $args{e} ) {
	my $Env = $args{e};
	if ( $Env =~  /cloud|prod|qa|staging|dev/ ) {
		&Parse($Env);
	} else {	
		print "\nNot a valid Env!\n";
		print "Valid Envs: cloud|prod|qa|staging|dev\n\n";
		sleep 1;
		&Usage();
	}
}
if ( $args{"?"} ) {
	&Usage();
}

# Parse_Properties
sub Parse() {
	my $Env = shift;
	print "FILE: $Env\_secret.properties\n";
	if ( $Env =~ /staging|dev/ ) {
		open ( PROP, "<", "/etc/pki/somecompany/$Env\_secret.properties" )
			or die "Cannot Open$!\n";
	} else {
		open ( PROP, "<", "/etc/pki/somecompany/private/$Env\_secret.properties" )
			or die "Cannot Open $!\n";
		while( <PROP> ) {
			if ( $_ =~ /dummy/i ) {
				$_ =~ /^#/ && next;
				print "$_";
			} else {
				next;
			}
		}	
		close(PROP);
	}
}

# Usage
sub Usage() {
    print <<USAGE;
Usage: FindDummy_Values.pl -e?
	-e Env
	-? This Menu

Examples:
    sudo FindDummy_Values.pl -e prod

USAGE
exit;
}

