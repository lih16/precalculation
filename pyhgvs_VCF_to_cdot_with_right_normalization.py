#takes as arg1 a list of tab-delimited VCF-format variants with a desired refGene transcript ("chr\tpos\tref\talt\tNM_111") and outputs the right-normalized cdot
#output file is arg2

#IMPORTANT: the input VCF should be preprocessed to add anchor bases (something like /hpc/users/soensz01/scripts/add_anchor_base_to_MVL_VCF.pl)
#
import sys #command line argument passing
import pyhgvs as hgvs
import pyhgvs.utils as hgvs_utils
import pygr.seqdb
from pygr.seqdb import SequenceFileDB

hg19 = SequenceFileDB('/sc/orga/projects/chenr02a/KBase/download/hgdownload.cse.ucsc.edu/goldenPath/hg19.fa')

#with open('/hpc/users/soensz01/python_practice/pyHGVS/genes.refGene') as infile: #use genes.refGene for a snapshot with transcript versions (ensure your transcript version matches what is present here)
with open('/hpc/users/soensz01/AILUN/soensz01_temp/refGene.txt') as infile:
    transcripts = hgvs_utils.read_transcripts(infile)

def get_transcript(name):
    return transcripts.get(name)

out = open(sys.argv[2], 'w')
with open (sys.argv[1]) as input:
	for variant in input:
		variant=variant.strip()
                chr_original, pos_original, ref_original, alt_original, transcript_original = variant.split("\t")
                if chr_original == 'chrMT': #hg19 chr QC
                        chr_original = 'chrM'
                if not chr_original.startswith('chr'): #hg19 chr QC
                        chr_original = "chr"+chr_original
		out.write(hgvs.format_hgvs_name(chr_original, int(pos_original), ref_original, alt_original, hg19, get_transcript(transcript_original), use_gene=False, max_allele_length=100)+"\n")

#########Default usage for format_hgvs_name:
#	 format_hgvs_name(chrom, offset, ref, alt, genome, transcript, use_prefix=True, use_gene=True, use_counsyl=False, max_allele_length=4)
#
#        Generate a HGVS name from a genomic coordinate.
#        
#        chrom: Chromosome name.
#        offset: Genomic offset of allele.
#        ref: Reference allele.
#        alt: Alternate allele.
#        genome: pygr compatible genome object.
#        transcript: Transcript corresponding to allele.
#        use_prefix: Include a transcript/gene/chromosome prefix in HGVS name.
#        use_gene: Include gene name in HGVS prefix.
#        max_allele_length: If allele is greater than this use allele length.
