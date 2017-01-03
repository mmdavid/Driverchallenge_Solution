
#!/usr/bin/python
import matplotlib.pyplot as plt
import sys
import argparse
import json
import os


parser = argparse.ArgumentParser(description= \
'This scripts will plot the reads aligned against the contig generated', usage= "\n\
"'\033[96m' + "Argument -i Input File: "+'\033[0m' + "Text file output from parser script 'graph.txt'.\n\
"'\033[96m' + "Argument -o Ouput Directory: "+'\033[0m' + "Indicate the name of an output directory.")

parser.add_argument('-i',dest="Infile", help='Input file graph.txt: text file output from parser script',required=True)
parser.add_argument('-o',dest="Outdir", help='output directory',required=True)
(args) = parser.parse_args()


with open(args.Infile,"r") as graph:
    index_for_graph = json.load(graph)

fig, ax = plt.subplots()
for i in range(len(index_for_graph)):
    ax.broken_barh([(0,0),(index_for_graph[i][0],(index_for_graph[i][1]-index_for_graph[i][0]))],(i, 0.5),facecolors='blue')
ax.set_ylim(0,len(index_for_graph))
ax.set_xlim(0,index_for_graph[-1][1])
ax.set_ylabel('Number of Reads')
ax.set_xlabel('Reads Overlapping')
ax.grid(True)

if not os.path.exists(os.path.dirname(args.Outdir)):
	os.makedirs(os.path.dirname(args.Outdir))
plt.savefig(os.path.join(args.Outdir, 'Assembly_graph.png'))