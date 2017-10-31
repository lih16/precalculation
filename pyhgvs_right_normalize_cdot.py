#takes as arg1 a list of NM_:cdot HGVS variants and outputs the right-normalized cdot HGVS format for each in order
#output file is arg2
#
import sys #command line argument passing
import pyhgvs as hgvs
import pyhgvs.utils as hgvs_utils
import pygr.seqdb
from pygr.seqdb import SequenceFileDB
#

hg19 = SequenceFileDB('/sc/orga/projects/chenr02a/KBase/download/hgdownload.cse.ucsc.edu/goldenPath/hg19.fa')

with open('/hpc/users/soensz01/AILUN/soensz01_temp/MVL_tran_ver_cdot.current.refGene_table') as infile:
#with open('/hpc/users/soensz01/AILUN/soensz01_temp/refGene.201710.txt') as infile:
    transcripts = hgvs_utils.read_transcripts(infile)

def get_transcript(name):
    return transcripts.get(name)

out = open(sys.argv[2], 'w')
with open (sys.argv[1]) as input:
	for variant in input:
		variant=variant.strip()
		transcript_original, cdot_original = variant.split(":")		
		chrom, offset, ref, alt = hgvs.parse_hgvs_name(variant, hg19, get_transcript=get_transcript)
		out.write(hgvs.format_hgvs_name(chrom, int(offset), ref, alt, hg19, get_transcript(transcript_original), use_gene=False, max_allele_length=100)+"\n")
