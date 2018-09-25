#!/usr/bin/perl
# ChineseVCDRip2Xbox360.pl
# C.M. Downs info\@drippingdead.com
# Sun Oct 24 12:50:37 CDT 2010
#
# Note: Chinese VCD's come on two discs. Audio Left ( Mono Center Cantonese ) and Right ( Mono Center Mandarin )
# This script will let you select the langauge of choice but by default will USE left ( Cantonese ) as it primary
# input Audio stream.
#
# Note: We will convert the RAW FileName.DAT.
#
# Two streams will be created and them panned L:R according to create on Stereo track for the Output.
#
# About the Streaming media:
# Encoded for Xbox360 Streaming ( Video 320x240; Xvid AVI; libmp3lame Mp3 Layer3 44,100khz )
#
# Requirement:
# ffmpeg ( macports )
# sox ( macports SoX v14.3.1 )
# Note: aka -> sudo port install ffmpeg sox
# multimux ( http://panteltje.com/panteltje/dvd/multimux-0.2.5.2.tgz )
# make && sudo cp multimux /opt/local/bin/

use strict;
use warnings;
use Getopt::Std;

# Vars
# This was compiled on Snow Leopard 10.6.4
# Please define your Binarys $PATH
my $Sox = '/opt/local/bin/sox';
my $Multimux = '/opt/local/bin/multimux';
my $ffmpeg = '/opt/local/bin/ffmpeg';
my $Extension = '.DAT';

# Simple Args
my %args;
getopts("i:t:cm?",\%args);

# Main
# Define Video Stream
if ( $args{i} ) {
        my $VideoStreamInput = $args{i};
        my $NewTitleName = $args{t};
        &GetVideoStreamInput($VideoStreamInput, $Extension, $NewTitleName);
} else {
        Usage();
}

# Usage
if ( $args{"?"} ) {
        Usage();
        exit;
}

# Subs
sub GetVideoStreamInput() {
        my $VideoStreamInput = shift;
        my $Extension = shift;
        my $NewTitleName = shift;
        chomp $VideoStreamInput;
        print "Video Stream:\n\t => $VideoStreamInput\n";
        my @VideoNamePrefix = split(/$Extension/, $VideoStreamInput);
        print "Extracting Video:\n";
        ## Maintain Max DataRate --
        system `$ffmpeg -i $VideoStreamInput -an -b 6000k -bt 6000k -vcodec libxvid $VideoNamePrefix[0].avi`;
        print "Extracting Stereo Channel:\n";
        system `$ffmpeg -i $VideoStreamInput $VideoNamePrefix[0]_Stereo.wav`;
        print "Isolating Channels:\n";
        unless ( -e '$VideoNamePrefix[0].wav' ) {
                if ( $args{m} ) {
                        ## Madarin --
                        print "\t => R: $VideoNamePrefix[0]_ManRight.wav\n";
                        system `$Sox $VideoNamePrefix[0]_Stereo.wav $VideoNamePrefix[0]_ManRight.wav mixer -r channels 1`;
                        print "Creating Mp3 Stream:\n";
                        system `$ffmpeg -i $VideoNamePrefix[0]_ManRight.wav -ab 128k -acodec libmp3lame $VideoNamePrefix[0]_ManRight.mp3`;
                        print "Assembling Video:\n";
                        if ( $args{t} ) {
                                system `$ffmpeg -i $VideoNamePrefix[0].avi -i $VideoNamePrefix[0]_ManRight.mp3 -vcodec copy -acodec copy $NewTitleName.avi`;
                        } else {
                                system `$ffmpeg -i $VideoNamePrefix[0].avi -i $VideoNamePrefix[0]_ManRight.mp3 -vcodec copy -acodec copy MAN_NewTitleXBOX360.avi`;
                        }
                } else {
                        ## Cantonese --
                        print "\t => L: $VideoNamePrefix[0]_CanLeft.wav\n";
                        system `$Sox $VideoNamePrefix[0]_Stereo.wav $VideoNamePrefix[0]_CanLeft.wav mixer -l channels 1`;
                        print "Creating Mp3 Stream:\n";
                        system `$ffmpeg -i $VideoNamePrefix[0]_CanLeft.wav -ab 128k -acodec libmp3lame $VideoNamePrefix[0]_CanLeft.mp3`;
                        print "Assembling Video:\n";
                        if ( $args{t} ) {
                                system `$ffmpeg -i $VideoNamePrefix[0].avi -i $VideoNamePrefix[0]_CanLeft.mp3 -vcodec copy -acodec copy $NewTitleName.avi`;
                        } else {
                                system `$ffmpeg -i $VideoNamePrefix[0].avi -i $VideoNamePrefix[0]_CanLeft.mp3 -vcodec copy -acodec copy CAN_NewTitleXbox360.avi`;
                        }
                }
        }
}

sub CleanupWorkingDir() {
}

# Usage:
sub Usage {
        print <<USAGE;
Usage: ChineseVCDRip2Xbox360.pl -icmt? <Input Filename>
        -i InputFile
        -c Cantoese
        -m Mandarin
        -t New Title Name
        -? This Menu

Examples:
        perl ChineseVCDRip2Xbox360.pl -i AVSEQ02.DAT -c
        perl ChineseVCDRip2Xbox360.pl -i /Volumes/VIDEOCD/MPEGAV/AVSEQ02.DAT -m WombGhosts_Part1

USAGE
exit;
}
