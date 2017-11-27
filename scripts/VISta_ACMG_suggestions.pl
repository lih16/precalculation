#!/usr/bin/perl
#ideally will only need to take vkey and transcript as input to avoid using pyHGVS python module in perl code, but for testing purposes... todo: will provide a VCF-variant to vkey step
#
#perl VISta_ACMG_suggestions.pl chr1,pos,ref,alt NM_000310.3
#perl VISta_ACMG_suggestions.pl _12Ph@U2Ph@U01 NM_000310.3
#
#T = temporarily commented for testing
#D = a statement temporarily uncommented for debugging purposes
#
use strict;
use warnings;

use lib '/hpc/users/soensz01/scripts';
use VISta::VISta_library qw(get_highest_MAF);

my ($chrom, $pos, $ref, $alt, $vkey);
my $tranver = $ARGV[1];

if ($ARGV[0] =~ /^chr/){ #presumably no vkey starts with "chr" meaning the input is a VCF-format variant
#T	($chrom, $pos, $ref, $alt) = split /,/, $ARGV[0];
#T	$vkey=&get_vkey($chrom, $pos, $ref, $alt);
}
else { $vkey = $ARGV[0] }

my $highest_MAF=&get_highest_MAF($chrom, $pos, $vkey); #should return the highest sub-pop MAF or "Position not covered sufficiently"
print "highest MAF = $highest_MAF\n";
