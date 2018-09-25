#!/usr/bin/perl 
# chris.downs\@reticulipictures.com
# google doc crap --

use strict;
use warnings;
use Getopt::Std;
use Term::ReadKey;
use LWP::UserAgent;
use Data::Dumper qw(Dumper);

# Vars
our $ver = '0.1';
my $auth_token;
my %Envs; 

# Args
my %args;
getopts( "e:E:c:?", \%args);
if ( $args{e} && $args{E}) {
    my $Email = $args{e};
    my $Env = $args{E};
    chomp $Email;
    chomp $Env;
    &Get_Token($Email);
    &Gen_Data($auth_token);
    #&Parse_Data_Exec(\%Envs, $Env);
} else {
    &Usage();
}

sub Get_Token() {
    my $Email = shift;
    print "Username: $Email\n";
    print "Google Password: ";
    ReadMode('noecho');
    my $Passwd = <STDIN>;
    ReadMode(0);
    chomp $Passwd;
    my $key = "0AqxsBTWRR_FbdEtjeGlEaFJ6WXBLVE9CYTJ6enBONlE";
    my $service = "wise";
    my $ua = LWP::UserAgent->new;
    my $response = $ua->post (
        'https://www.google.com/accounts/ClientLogin',
        {
            accountType => 'GOOGLE',
            Email       => $Email,
            Passwd      => $Passwd,
            service     => $service,
            source      => 'LWP::UserAgent',
        }
    );
    die "\nError: ", $response->status_line unless $response->is_success;
    foreach my $line (split/\n/, $response->content) {
        if ($line =~ m/^Auth=(.+)$/) {
            $auth_token = $1;
            last;
        }
    }
    print "\nAuth: $auth_token\n";
    return ($auth_token);
}

# Gen_Data
sub Gen_Data() {
    my $auth_token = shift;
    my $Sheet = ('/usr/bin/curl');
    $Sheet .= ' --silent --header "Authorization: GoogleLogin auth="' . $auth_token;
    $Sheet .= ' "https://spreadsheets.google.com/feeds/list/0Au8StYf8-sfgK9DR3RYRy1yMXVBU3ZsMEhlR2k5NlE/od6/private/full" | tidy -xml -quiet';
    my @Parse_Sheet = `$Sheet`;
    foreach my $line ( @Parse_Sheet ) {
        if ( $line =~ /(\<gsx:name\>)(.+?)(\<\/gsx:name\>)/s ) {
            $line = $2;
            $line =~ /TBD/ && next;
            my $fqdn = $line . '.somecompany.com';
            push @{ $Envs{'name'} }, $fqdn;
        } elsif ( $line =~ /(\<gsx:environment\>)(.+?)(\<\/gsx:environment\>)/s ) {
            $line = $2;
            push @{ $Envs{'name'} }, $line;
        } elsif ( $line =~ /(\<gsx:os\>)(.+?)(\<\/gsx:os\>)/s ) {
            $line = $2;
            push @{ $Envs{'name'} }, $line;
        } elsif ( $line =~ /(\<gsx:usescnames\>)(.+?)(\<\/gsx:usescnames\>)/s ) {
            $line = $2;
            push @{ $Envs{'name'} }, $line;
        } elsif ( $line =~ /(\<gsx:active\>)(.+?)(\<\/gsx:active\>)/s ) {
            $line = $2;
            push @{ $Envs{'name'} }, $line;
        }
    }
    print Dumper \%Envs;
}

# Log
sub Log {
    my @mes = @_;
        my $logfile = "/tmp/output.txt";
    open LOG, (">>$logfile")
        or die "Cannot open $logfile for writing $!\n";
    print LOG @mes;
    close(LOG);
}

# Usage
sub Usage() {
        print <<USAGE;
ServerInfoSheet_ExecCommands.pl v:$ver
Usage: ServerInfoSheet_ExecCommands.pl -eEc? 
    -e Email Address
    -E Environment (prod|qa|staging|dev|smoke )
    -O OS (rhel|win)
    -C Usescnames
    -A Active (y|n)
    -c Remote Command
    -? This Menu

Examples:
    perl ServerInfoSheet_ExecCommands.pl -e 'chris.downs\@somecompany.com' -E prod -A y -c 'sudo cat /etc/redhat-release'

USAGE
exit;
}

__END__
