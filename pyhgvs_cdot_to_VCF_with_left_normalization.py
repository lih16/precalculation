#takes as arg1 a list of NM_:cdot HGVS variants and outputs the left-normalized VCF format for each in order
#output file is arg2
#
import sys #command line argument passing
import pyhgvs as hgvs
import pyhgvs.utils as hgvs_utils
import pygr.seqdb
from pygr.seqdb import SequenceFileDB

hg19 = SequenceFileDB('/sc/orga/projects/chenr02a/KBase/download/hgdownload.cse.ucsc.edu/goldenPath/hg19.fa')

with open('/hpc/users/soensz01/AILUN/soensz01_temp/MVL_tran_ver_cdot.current.refGene_table') as infile:
#with open('/sc/orga/projects/AILUN/soensz01_temp/refGene.uta_20170907.txt') as infile: #use uta for all transcript versions dating back several years
#with open('/hpc/users/soensz01/python_practice/pyHGVS/genes.refGene') as infile: #use genes.refGene for a snapshot with transcript versions (ensure your transcript version matches what is present here)
#with open('/hpc/users/soensz01/AILUN/soensz01_temp/refGene.txt') as infile: #use refGene.txt for no transcript versions (most recent version from Sept 2017)
    transcripts = hgvs_utils.read_transcripts(infile)

def get_transcript(name):
    return transcripts.get(name)

out = open(sys.argv[2], 'w')
with open (sys.argv[1]) as input:
	for variant in input:
		variant=variant.strip()
#		print(line+"\n")
#		out.write(line+"\n")
		chrom, offset, ref, alt = hgvs.parse_hgvs_name(variant, hg19, get_transcript=get_transcript)
		out.write(chrom+"\t"+str(offset)+"\t"+ref+"\t"+alt+"\n")

