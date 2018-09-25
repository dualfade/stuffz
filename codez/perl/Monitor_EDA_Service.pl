#!/usr/bin/perl 
# MonitorEdaStart.pl
# chris.downs\@reticulipictures.com

# prod-bi01.somecompany.com 
# /var/reporting/tools
# crontab 
# */5 * * * * /var/reporting/tools/./MonitorEdaStart.pl 2&>1 /var/log/cron 

use strict;
use warnings;
use Socket;
use vars qw($timeout $host);

# Version
my $version = ("v1.1");

# Vars
my $host = "qa-bi01.somecompany.com";
my @ports = (8120,8123);
my $localtime = localtime(time);
my $timeout = 3;

unless ($< == 100) {
    print "You must run this script as iadmin\n";
    print "Exiting Now!\n";
    sleep 1;
    &Usage();
    exit;
}

# set Env
$ENV{'PATH'} = '/var/reporting/ibi/srv77/wfs/bin';
$ENV{SHELL} = '/bin/bash' if exists $ENV{SHELL};

## Start Main App
print "Starting: \n";
print "P: $ENV{'PATH'}\n";
print "S: $ENV{'SHELL'}\n";
my $App = &Status();;
print scalar "-> $App\n";
if (scalar $App =~ /\bRunning/) {
	print "R -> Checking Port Status: \n";
    &Ports(@ports);
}
elsif (scalar $App =~ /\bNotRunning/) {
	print "NR -> Checking port status: \n";
    &Start_App();
}

#Subs
sub Ports {
    my @port  = @_; 
    my $h = $host; 

    foreach my $p (@port) {
        my $ia = inet_aton($host);
        my $pa = sockaddr_in($p, $ia);
        my $pr = getprotobyname('tcp');
        socket(SOCKET, PF_INET, SOCK_STREAM, $pr) 
            or die "socket: $!\n"; 

        eval {
            local $SIG{ALRM} = sub { die "timeout" };
            alarm($timeout);
            connect(SOCKET, $pa) 
                or error(); 
            alarm(0);
        };

        if ($@) {
            close SOCKET || die "close: $!";
            print "$h is NOT listening on tcp port $p.\n";
            &Start_App();
            exit 1;
        } else {
            close SOCKET || die "close: $!";
            print "$h is listening on tcp port $p.\n";
            exit 0;
        } 

    }
}   

sub Start_App {
	print "Status: Starting iadmin\n";
	my $AppStop = `/var/reporting/ibi/srv77/wfs/bin/./edastart -stop`;
	sleep 3;
	my $AppStart = `/var/reporting/ibi/srv77/wfs/bin/./edastart -start`;
	&Log("$localtime Status: Restarted iadmin\n");
	print "E: Exiting Now\n";
	exit;
}

sub Status {
	print "Status: Checking\n";
	my $Status = `/var/reporting/ibi/srv77/wfs/bin/./edastart -status`;

}

sub Log {
    my @mes = @_;
	my $logfile = "/var/reporting/tools/MonitorLog.txt";
	print "Status: Logging\n";
    open LOG, (">>$logfile")
        or die "Cannot open $logfile for writing $!\n";
    print LOG @mes;
    close(LOG);
}
