#takes as arg1 a list of tab-delimited VCF-format variants("chr\tpos\tref\talt") and outputs the left-normalized version in the same format
#output file is arg2
#
##IMPORTANT: the input VCF should be preprocessed to add anchor bases (something like /hpc/users/soensz01/scripts/add_anchor_base_to_MVL_VCF.pl)

#
import sys #command line argument passing
import pyhgvs as hgvs
import pyhgvs.utils as hgvs_utils
import pygr.seqdb
from pygr.seqdb import SequenceFileDB
import os #OS interactions (cwd etc)
import re #perl-like regexp
#

hg19 = SequenceFileDB('/sc/orga/projects/chenr02a/KBase/download/hgdownload.cse.ucsc.edu/goldenPath/hg19.fa')

with open('/hpc/users/soensz01/AILUN/soensz01_temp/refGene.txt') as infile:
    transcripts = hgvs_utils.read_transcripts(infile)

def get_transcript(name):
    return transcripts.get(name)

out = open(sys.argv[2], 'w')
with open (sys.argv[1]) as input:
	for variant in input:
		variant=variant.strip()
		chr_original, pos_original, ref_original, alt_original = variant.split("\t")
		if chr_original == 'chrMT': #hg19 chr QC
			chr_original = 'chrM'
		if not chr_original.startswith('chr'): #hg19 chr QC
			chr_original = "chr"+chr_original
###This now commented out because pyhgvs does not handle adding anchor bases to blank alleles correctly, the input VCF should be preprocessed to add anchor bases (something like /hpc/users/soensz01/scripts/add_anchor_base_to_MVL_VCF.pl)
#		#if the alt or ref allele are not letters, interprets as a non-anchored deletion or insertion (ex: ".") and replaces with blank for pyhgvs (although pyhgvs handles "-")
#		if not alt_original.isupper() or alt_original.islower():
#			alt_original = ''
#		if not ref_original.isupper() or ref_original.islower():
#			ref_original = ''

		#one thing to be careful of is normalize_variant() expects the alt allele to be an array (in [])
		norm_var = hgvs.normalize_variant(str(chr_original), int(pos_original), ref_original, [alt_original], hg19)
                out.write(norm_var.position.chrom+"\t"+str(norm_var.position.chrom_start)+"\t"+norm_var.ref_allele+"\t"+norm_var.alt_alleles[0]+"\n")
