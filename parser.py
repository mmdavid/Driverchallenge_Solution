#!/usr/bin/python
import sys
import time
import argparse
import Bio
import os
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

#importing the other functions
from functions import import_file_aslist
from functions import find_overlap
from functions import what_overlap
from functions import find_first_read
from functions import best_overlap_from_the_dict
from functions import final_order
from functions import put_contig_together
from functions import for_graph


if __name__ == '__main__':
	#input and Output files description
	parser = argparse.ArgumentParser(description= \
	'This scripts will build a contig based on the fasta file imported.', usage= "\n\
	"'\033[96m' + "Argument -i Input File: "+'\033[0m' + "Fasta file containing sequences to align. \n\
	'\033[96m'" + "Argument -o Ouput Directory: "+'\033[0m' + "Indicate the name of an output directory."
	"The script will: \n\
	- print the final contig in the terminal, and save it to a fasta file 'assembly.fasta' \n\
	- save a text file that can be used to visualize coverage of the assembly 'graph.txt' \n\
	- save a log file (duration, number of read used, order of the reads, and the dicitonnanry fo overlaps")

	parser.add_argument('-i',dest="Infile", help='Input file, needs to be a fasta file',required=True)
	parser.add_argument('-o',dest="Outdir", help='output directory',required=True)
	(args) = parser.parse_args()

	#actual script
	start = time.time()
	selectlist = import_file_aslist(args.Infile)
	dict_overlap = what_overlap(selectlist)
	first_read = find_first_read(dict_overlap)
	orderok = final_order(first_read, dict_overlap)
	contig_final =put_contig_together(orderok, selectlist, dict_overlap)
	index_for_graph = for_graph(orderok,dict_overlap,selectlist,contig_final)
	end = time.time()
	duration = end-start

#making an output directory 
	if not os.path.exists(os.path.dirname(args.Outdir)):
		os.makedirs(os.path.dirname(args.Outdir))
#saving the assembly in a file called "assembly.fasta" and printing it on the termimal
	rec = SeqRecord(id='longestassembly', description='', seq=contig_final)
	print "The final contig has a length of %d bp, here it is \n%s" %(len(contig_final),contig_final)
	SeqIO.write(rec, os.path.join(args.Outdir,"assembly.fasta"), "fasta")

#saving log
	with open(os.path.join(args.Outdir, "log.txt"), "w") as f:
		sis=str(args.Infile)
		f.write("command: python parser_getthelongestcontig.py '-i' %s \n" %sis)
		sstime = str(duration)
		f.write("It took %s to assemble \n" %sstime)
		sorderok=str(orderok)
		f.write("Names of each sequenced align in that order %s\n" %sorderok)

#saving the text file for the graph
	with open(os.path.join(args.Outdir,"graph.txt"), "w") as g:
		sindex_for_graph = str(index_for_graph)
		g.write(sindex_for_graph)
