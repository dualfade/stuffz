#!/usr/bin/perl
# DatabaseTunnels.pl
# chris.downs\@reticulipictures.com

use strict;
use warnings;
use Getopt::Std;
use Term::ReadKey;

# Global Vars
my %args;

# AutoStart All Array
my %db = (
    db01_prod => [ 'db01.prod.company.com', '13311', '3306', ],
    db02_prod => [ 'db02.prod.company.com', '13312', '3306', ],
    dbdw_prod => [ 'dbdw.prod.company.com', '13313', '3306', ],
    db01_dr   => [ 'db01.dr.company.com', '13314', '3306', ],
    db01_wash => [ 'db-wash.company.com', '13315', '3306', ],
    db01_qa   => [ 'db01.qa.company.com', '13321', '3306', ],
    db01_staging => [ 'db01.staging.company.com', '13331', '3306', ],
    db01_dev  => [ 'db01.dev.company.com', '13332', '3306', ],
    db01_c2prod  => [ 'db01.c2-prod.company.com', '13341', '3306', ],
    db02_c2prod  => [ 'db02.c2-prod.company.com', '13342', '3306', ],
    db03_c2prod  => [ 'db03.c2-prod.company.com', '13343', '3306', ],
    dbdr_c2prod  => [ 'dbdr.c2-prod.company.com', '13344', '3306', ],
    db01_c2qa    => [ 'db01.c2-qa.company.com', '13351', '3306', ],
    db01_c3prod    => [ 'db01.c3-prod.company.com', '13371', '3306', ],
    db02_c3prod    => [ 'db02.c3-prod.company.com', '13372', '3306', ],
    dbdw_c3prod    => [ 'dbdw.c3-prod.company.com', '13373', '3306', ],
    disney_dev   => [ 'disney.dev.company.com', '13361', '3306', ],
    disney_staging  => [ 'disney.staging.company.com', '13362', '3306', ],
    disney_prod     => [ 'disney.prod.company.com', '13363', '3306', ],
    disney_c2prod   => [ 'disney.c2-prod.company.com', '13364', '3306', ],
    disney_c3prod   => [ 'disney.c3-prod.company.com', '13365', '3306', ],
    db01_c3prod  => [ 'db01.c3-prod.company.com', '13371', '3306', ],
);

# Getops
getopts("AA:RR:DD:KK:MM:h:p:e:?", \%args);
if ( $args{A} ) {
    &AutoStart();
} elsif ( $args{R} ) {
    my $host = $args{h};
    my $port = $args{p};
    &StartTunnel($host, $port);
} elsif ( $args{D} ) {
    my $env = $args{e};
    &DestroyTunnel($env);
} elsif ( $args{K} ) {
    &Killall();
} elsif ( $args{M} ) {
    &Monitor();
} else {
    &Usage();
}

# AutoStart All hashed tunnels
sub AutoStart() {
    for my $dbname ( keys %db ) {
        print "INITIATE: Starting Connection: ssh -f -N -L $db{$dbname}[1]:localhost:3306 tunnel\@$db{$dbname}[0]\n";
        system ("ssh -f -N -L $db{$dbname}[1]:localhost:$db{$dbname}[2] tunnel\@$db{$dbname}[0]");
        if ( $? == -1 ) {
            print "STATUS: Execution failed$!\n"
        } else {
            printf "STATUS: Connected => Status %d\n", $? >> 8;
        }
    }
}

# Kill All Tunnels
sub Killall() {
    my $i;
    my @PID;
    print "QUESTION: Destroy All Active Tunnels?\n";
    print "ANSWER: Are you Sure?? ( yes|no ) ";
    ReadMode('normal');
    my $Answer = <STDIN>;
    chomp $Answer;
    unless ( $Answer eq 'yes' ) {
        print "BAILED: Ermmm.... Ok.. So Am I !\n";
        exit;
    } else {
        print "STATUS: Gathering PID's\n";
        sleep 1;
        $ENV{'PATH'} = '/bin:/usr/bin/';
        my @Destroy = `ps -ef | grep 'ssh -f -N -L' | grep 'tunnel\@' | grep -v 'sh -c ps'`;
        print "DESTROY: Tunnels\n";
        foreach my $pid ( @Destroy ) {
            print "$pid";
            my @ps =  split('\s+', $pid, 13);
            my $pkill = system ("kill -9 $ps[1]");
        }
    }
}

# Monitor Mode
sub Monitor() {
    print "CONNECTIONS:\n";
    $ENV{'PATH'} = '/bin:/usr/bin/';
    for my $dbname ( keys %db ) {
        print "Checking Connection: $dbname\n";
        my @Cmd = `ps -ef | grep 'ssh -f -N -L' | grep 'tunnel\@' | grep -v 'sh -c ps'`;
        if ( grep { /$db{$dbname}[0]/ } @Cmd ) {
            next;
        } else {
            print "NOT RUNNING: $db{$dbname}[0]\n";
            print "INITIATE: Starting Connection: ssh -f -N -L $db{$dbname}[1]:localhost:3306 tunnel\@$db{$dbname}[0]\n";
            system ("ssh -f -N -L $db{$dbname}[1]:localhost:$db{$dbname}[2] tunnel\@$db{$dbname}[0]");
        }
    }
}

# Start New Tunnel 
sub StartTunnel() {
    my $host = shift;
    my $port = shift;
    print "Starting Connection: ssh -f -N -L $port:localhost:3306 tunnel\@$host\n";
    $ENV{'PATH'} = '/usr/bin/';
    system ("ssh -f -N -L $port:localhost:3306 tunnel\@$host");
    if ( $? == -1 ) {
        print "STATUS: Execution failed$!\n"
    } else {
        printf "STATUS: Exited with value %d\n", $? >> 8;
    }
}

# Destroy Existing Tunnel
sub DestroyTunnel() {
    my $env = shift;
    print "STATUS: Checking for existing connections\n";
    $ENV{'$PATH'} = '/bin';
    my $parse = system("ps -ef | grep $env | grep 'ssh -f -N -L' | grep -v 'sh -c ps' | awk {'print \$2,\$8,\$9,\$10,\$11,\$12,\$13'}");
    print "WARNING: Kill which pre existing tunnel ? (PID): ";
    ReadMode('normal');
    my $kill = <STDIN>;
    chomp $kill;
    print "OK: Teminating $kill\n";
    system ("kill -9 $kill");
    if ( $? == -1 ) {
        print "STATUS: Execution failed$!\n"
    } else {
        printf "STATUS: Exited with value %d\n", $? >> 8;
    }
}

sub Usage {
    print <<USAGE;
Usage: DatabaseTunnels -ARDKhpe?
    -A Autostart All
    -R Run a single instance
    -D Destroy an instance
    -K Kill all Tunnels
    -M Monitor mode ( Use for cronjob )
    -h Host
    -p Port (Local listener)
    -e Environment
    -? This Menu

Examples:
    perl DatabaseTunnels.pl -R -h db.qa.company.com -p 13321
    perl DatabaseTunnels.pl -D -e qa
    perl DatabaseTunnels.pl -A
    perl DatabaseTunnels.pl -K
    perl DatabaseTunnels.pl -M

USAGE
exit;
}
