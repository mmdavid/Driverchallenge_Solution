####Driver Challenge
Here is my answer for the data challenge given by Annie Morrison by email, using python 2.7. 

####Usage: 
python parser.py --help
python graph.py --help
You must run parser.py BEFORE graph.py, and all the output will be saved in a folder called "results" 

####Example:
Step 1 - Build the contig:
python parser.py -i data/coding_challenge_data_set.txt -o results/
Step 2 - Visualize the contig coverage, and create a png:
python graph.py -i graph.txt -o results/

####Description: 3 scripts:
- functions.py: Define the functions used
- parser.py: Script to run calling the functions to build the contig 
- graph.py: Which will plot the reads along the newly assembled sequence. This is can helpdul to have an idea of the coverage of our contig. 

####Approach: explanation of the functions: 

1. import_file_aslist(File): Import the text file provided and use biopython to read the fasta format. Create a Seq object for each sequence, stored in a list
2. find_overlap(seq1,seq2): Find the overlap between 2 DNA sequences. For example here:
 seq2        ATGCGTACGTAGCTAGTA
 		     |||||||||||
 seq1  ATGCGTATGCGTACGTA

 will return: ATGCGTACGTA

3. what_overlap(listofreads): Input the list of seq objects from step 1. Will return a dictionary of dictionaries. The keys are the sequence 1 and the value the overlap with the sequence 2. 
4. find_first_read(dict_overlaps): Look for the read that don't have an significant overlap on the left (i.e. is never a "sequence #2"), in order to return the id of the first read.
5. best_overlap_from_the_dict(dict_overlaps): Find the best overlap in the dictionary for each "sequence 1" with all the other sequences.
6. final_order(first, dict_overlaps): Input: the reads known as being the first one, and the dictionary of dictionaries. Look for the key (here:the sequence id) of the sequence with the largest overlap to add the name to the right, starting with the read already identified as the first one. Output a list of read IDs in the order of the contig we want to assemble. 
7. put_contig_together(read_order_ok, listofreads, dict_overlaps): Use the list of ids in order to find the next sequence. It will reconstruct using the part of the sequence that do NOT overlap with the next sequence (i.d. sequence1).
 seq2        ATGCGTACGTAGCTAGTA
 		     |||||||||||
 seq1  ATGCGTATGCGTACGTA
 Does this recursively, until the entire sequence of the last read is added.
 8. for_graph(read_order_ok,dict_overlaps, listofreads,concatenated): This will use matplotlib to draw a line with the index of each reads mapped on the contigs. It outputs a png graph.

####Comments
This script runs fast but rely on perfect matches between the sequences. I usually use other software (velvet for example) which will allow to assembly much bigger dataset with smaller size reads and some mismatches (the output of Hiseq dataset I have been working with are in the range of 250 bp). 

####Warning matlpotlib
Matplotlib may send out warnings "FutureWarning: elementwise comparison failed; returning scalar instead, but in the future ...." The developers indicated that the bug will be fixed "soon" on github. 

####Challenge:
The input to the problem is at most 50 DNA sequences (i.e, the character set is limited to T/C/G/A) whose length does not exceed 1000 characters. The sequences are given in FASTA format (https://en.wikipedia.org/wiki/FASTA_format). These sequences are all different fragments of one chromosome.

The specific set of sequences you will get satisfy a very unique property:  there exists a unique way to reconstruct the entire chromosome from these reads by gluing together pairs of reads that overlap by more than half their length. An example set of input strings is attached.

The output of your program should be this unique sequence that contains each of the given input strings as a substring.

In addition to the code you wrote, we also ask for a README describing your general approach as well as any additional code you wrote to evaluate your solution. We would prefer your code to be written in Python, Go, Scala, Javascript, or Java.

