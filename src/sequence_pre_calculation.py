# imports extern
import itertools
import numpy as np

# imports intern
# import src.file_reader as file
import file_reader as file
# import src.argument_parser as pars
import argument_parser as pars

# BedTools .getfasta for extracting sequence
# https://bedtools.readthedocs.io/en/latest/content/tools/getfasta.html
# seq_one =
file.bed_one.getfasta(fi=file.ref_fasta, s=True, bedOut=True, fo="firstSeq.fa.out")
# seq_two =
file.bed_two.getfasta(fi=file.ref_fasta, s=True, bedOut=True, fo="secondSeq.fa.out")

# save getfasta output to local variable
with open("firstSeq.fa.out", "r") as in_file:
    seq_one = in_file.readlines()
in_file.close()
with open("secondSeq.fa.out", "r") as in_file:
    seq_two = in_file.readlines()
in_file.close()

# k-mer Lists calculation

# k-mer size
ksize = 3
if pars.args.ksize is not None:
    ksize = int(pars.args.ksize)


# genrate k-mer list for PCA
bases = ['A', 'T', 'G', 'C']
kmer_list = []
k = 3
for i in range(1, k + 1):
    kmer_list.extend([''.join(p) for p in itertools.product(bases, repeat=i)])


# count k-mer occurrences in each sequence for each subsequence
list_all_kmer_counts = np.zeros(((len(seq_one) + len(seq_two)), len(kmer_list)), int)
row_number = 0
col_number = 0
for subseq in seq_one:
    col_number = 0
    for kmer in kmer_list:
        list_all_kmer_counts[row_number][col_number] = subseq.count(kmer)
        col_number += 1
    row_number += 1
for subseq in seq_two:
    col_number = 0
    for kmer in kmer_list:
        list_all_kmer_counts[row_number][col_number] = subseq.count(kmer)
        col_number += 1
    row_number += 1


# count k-mer occurrences in each sequence
col_count = 0
kmer_matrix = np.zeros((2, len(kmer_list)))
for kmer in kmer_list:
    for subseq in seq_one:
        kmer_matrix[0][col_count] += subseq.count(kmer)
    col_count += 1
col_count = 0
for kmer in kmer_list:
    for subseq in seq_two:
        kmer_matrix[1][col_count] += subseq.count(kmer)
    col_count += 1
