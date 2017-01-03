
#!/usr/bin/python
import sys
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

def import_file_aslist(File):
    selectsewlist = list()
    with open(File, "rU") as input_handle:
        selectsewlist = list(SeqIO.parse(input_handle, "fasta"))
    return selectsewlist

def find_overlap(seq1,seq2):
    for i in range(len(seq1)):
        if seq1.seq[i:] == seq2.seq[:len(seq1.seq)-i]:
            sequencematching = seq1.seq[i:]
            return sequencematching

def what_overlap(listofreads):
    dict_reads = dict()
    for seq1 in listofreads:
        for seq2 in listofreads:
            if seq1.id == seq2.id:
                continue
            if seq1.id not in dict_reads:
                dict_reads[seq1.id] = dict()
            dict_reads[seq1.id][seq2.id] = len(str(find_overlap(seq1, seq2)))
    return dict_reads

def find_first_read(dict_overlaps):
    for i in dict_overlaps:
        signifOverlaps = False
        for j in dict_overlaps[i]:
            if dict_overlaps[j][i] > 5:
                signifOverlaps = True
        if not signifOverlaps:
            return i

def best_overlap_from_the_dict(dict_overlaps):
    m = max(d.values())
    for k in dict_overlaps:
        if dict_overlaps[k] == m:
            return k

def final_order(first, dict_overlaps):
    nextRead = best_overlap_from_the_dict(dict_overlaps[first])
    return [first] + final_order(nextRead, dict_overlaps)

def put_contig_together(read_order_ok, listofreads, dict_overlaps):
    contigs = list()
    for readName in read_order_ok[:-1]:
        overlap = max(x for x in dict_overlaps[readName].values() if x >= 5)
        overlapseq = [a for a in listofreads if a.id == readName]
        contigs += [b.seq[:-overlap] for b in overlapseq]
    contigs += [a.seq for a in listofreads if a.id == read_order_ok[-1]]
    concatenated = Seq("")
    for s in contigs:
        concatenated += s
    return concatenated

def for_graph(read_order_ok,dict_overlaps, listofreads,concatenated):
    no_overlaptot = list()
    overlaptot = list()
    lengthreadtot = list()
    for readName in read_order_ok[:-1]:
        overlap = max(x for x in dict_overlaps[readName].values() if x >= 5)
        overlapseq = [a for a in listofreads if a.id == readName]
        no_overlap = [len(b.seq[:-overlap]) for b in overlapseq]
        no_overlaptot.append(no_overlap)
        overlaptot.append(overlap)
        lengthreadtot.append([len(b.seq) for b in overlapseq])
        indexcoverage = ([[] for x in range(len(lengthreadtot))])
        begin = 0 
        for i in range(len(lengthreadtot)):
            indexcoverage[i].append(begin)
            indexcoverage[i].append(begin+lengthreadtot[i][0])
            begin += (lengthreadtot[i][0]-overlaptot[i])
        indexcoverage[-1][1] = len(concatenated)
    return indexcoverage
