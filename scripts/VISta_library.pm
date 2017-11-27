#T = temporarily commented for testing
#D = a statement temporarily uncommented for debugging purposes

package VISta::VISta_library;
use strict;
use warnings;

use Exporter qw(import);

our @EXPORT_OK = qw(get_highest_MAF is_pos_covered);# is_pos_covered suggest_BA1_BS1_PM2 get_genotype_counts suggest_BS2);

##SUBS FOR POPULATION FREQUENCY DATA: BEGIN

sub get_highest_MAF
#I: VCF variant // vkey
#O: highest subpopulation/ethnicity MAF with AC > 2000, only 0% if cov>20x/sample in gnomAD
{
	my $highest_MAF = 0;
	my ($chrom, $pos, $vkey) = @_;
	use DBI;

	####check gnomAD
	my $dbh = DBI->connect("DBI:mysql:database=var_gnomAD_r2d0d1_hg19_20170531;host=db2.ib.hpc.mssm.edu;port=3306", "vista_read_only", "Aq4W8FXRCDvEU9UmTf66hFD3");
	my $sth = $dbh->prepare("select AF_max from combined_vcf where vkey = \"$vkey\"");
	$sth->execute();
	my $hashref = $sth->fetchrow_hashref();
	if ($hashref){ #if a variant is found, hashref will be defined, and the MAF will be updated
		my %row = %{$hashref};
		$highest_MAF = $row{"AF_max"};
	}

	####check UK10K
	####check Qatar
	####check HGVD
	
	if($highest_MAF == 0 and ! &is_pos_covered($chrom, $pos)){ return "Position not covered sufficiently" }#flags that the 0 MAF cannot be trusted
	else { return $highest_MAF }
}

sub is_pos_covered
#I: Chromosomal position
#O: Is the position covered > 20x/sample on average? (yes or no)(1 or 0)
{
	my ($chrom, $pos) = @_;
######needs gnomAD coverage data loaded into db2!!
#T	use DBI;
#T      my $dbh = DBI->connect("DBI:mysql:database=proj_VISta;host=db2.ib.hpc.mssm.edu;port=3306", "vista_read_only", "Aq4W8FXRCDvEU9UmTf66hFD3");
#T      my $sth = $dbh->prepare("select mean from <<<table>>> where <<<chrom = $chrom AND pos = $pos>>> ); #ensure matching chr chrom usage
#T      $sth->execute();
####does this need a case to handle no match? all pos should be covered?
#T      my %row = %{$sth->fetchrow_hashref()};
#T	if ( $row{"mean"} >= 20 ){ return 1 }
#T	else { return 0 }
######needs gnomAD coverage data loaded into db2!!

	return 0;
}

#suggest_BA1_BS1_PM2
#I: VCF variant
#O: BA1, BS1, PM2, or other options
#sub suggest_BA1_BS1_PM2

#get_genotype_counts
#I: VCF variant
#O: genotype counts at this position (number homoz, hetero, hemiz)
#sub get_genotype_counts

#suggest_BS2
#I: VCF variant
#O: BS2 or other options
#sub suggest_BS2


##SUBS FOR POPULATION FREQUENCY DATA: END

END;
