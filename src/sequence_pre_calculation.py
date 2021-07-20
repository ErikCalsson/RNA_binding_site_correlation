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
with open("secondSeq.fa.out", "r") as in_file:
    seq_two = in_file.readlines()

# k-mer Lists calculation

# k-mer size
ksize = 3
if pars.args.ksize is not None:
    ksize = int(pars.args.ksize)


# getting k-mers from a single sequence
def make_kmer_list(seq, size, index):
    list_out = []
    tmp_kmers = []
    n_kmers = len(seq) - size + 1
    for i in range(n_kmers):
        kmer = seq[i:i + size]
        # for peak call later
        list_all.append((kmer, index, i))
        # not allowing duplicates
        if kmer not in tmp_kmers:
            tmp_kmers.append(kmer)
            list_out.append((kmer, index, i))  # offset = i
    return list_out


# make new list of unique k-mers
def remove_duplicates(list_in):
    list_out = []
    [list_out.append(x) for x in list_in if x not in list_out]
    return list_out


sub_seq_index = 0
list_unique_one = []
list_unique_two = []
list_all = []  # for peak call later
for sub_seq in range(0, len(seq_one)):
    # get k-mers for each sub_seq
    out_list = make_kmer_list(seq_one[sub_seq], ksize, sub_seq_index)
    list_unique_one.extend(out_list)
    sub_seq_index += 1


sub_seq_index = 0
for sub_seq in range(0, len(seq_two)):
    # get k-mers for each sub_seq
    out_list = make_kmer_list(seq_two[sub_seq], ksize, sub_seq_index)
    list_unique_two.extend(out_list)
    sub_seq_index += 1


# sorting list after kmers
list_unique_one.sort(key=lambda a: a[0])
list_unique_two.sort(key=lambda a: a[0])


# foreach element in second dataset
pointerA = 0
pointerB = pointerA + 1
# foreach element in first dataset
pointerC = 0

dict_SD = dict()
while pointerC < len(list_unique_one) and pointerB < len(list_unique_two) and pointerA < len(list_unique_two):
    while pointerB < len(list_unique_two) and list_unique_one[pointerC][0] == list_unique_two[pointerB][0]:
        pointerB += 1
    for elem_y in range(pointerA, pointerB):
        # only compare sub_seq of similar length. Here shorter at least 80% of longer one in log 2
        # TODO length similarity as input variable ?
        if np.math.log(len(seq_one[list_unique_one[pointerC][1]])) >= np.math.log(
            len(seq_two[list_unique_two[elem_y][1]]) * 0.8) \
            or np.math.log(len(seq_two[list_unique_two[elem_y][1]])) >= np.math.log(
                np.math.log(len(seq_one[list_unique_one[pointerC][1]]))):

            key_part_one = str(list_unique_one[pointerC][1])
            key_part_two = "-"
            key_part_three = str(list_unique_two[elem_y][1])
            dict_key = key_part_one + key_part_two + key_part_three
            if dict_key in dict_SD.keys():
                dict_SD[dict_key] = ((dict_SD.get(dict_key)) + 1)
            else:
                dict_SD.update({dict_key: 1})
    pointerA = pointerB
    pointerB = pointerA + 1
    pointerC += 1

v50 = 0
v60 = 0
v70 = 0
v80 = 0
v90 = 0
less50 = 0
more50 = 0
sumSD = 0
zal = 0
wrong = 0


# dicts for best entries from each row or column
dict_best_one = dict()
dict_best_two = dict()

for key in dict_SD:
    dex = key.split("-")
    first_dex = int(dex[0])
    second_dex = int(dex[1])
    SD = (200 * dict_SD[key]) / ((len(seq_one[first_dex]) - ksize + 1) + (len(seq_two[second_dex]) - ksize + 1))
    dict_SD[key] = SD

    # add best SD values for each row or col into own dict
    if first_dex in dict_best_one.keys():
        if dict_best_one[first_dex] < SD:
            dict_best_one[first_dex] = SD
    else:
        dict_best_one.update({first_dex: SD})
    if second_dex in dict_best_two.keys():
        if dict_best_two[second_dex] < SD:
            dict_best_two[second_dex] = SD
    else:
        dict_best_two.update({second_dex: SD})

    sumSD += SD
    zal += 1
    if SD > 100:
        wrong += 1
    if SD < 50:
        less50 += 1
    elif SD >= 50:
        more50 += 1
        if SD <= 90:
            v80 += 1
        elif SD <= 100:
            v90 += 1
        elif SD <= 80:
            v70 += 1
        elif SD <= 70:
            v60 += 1
        elif SD <= 60:
            v50 += 1
print("counts")
print("less50", less50)
print("more50", more50)
print(">50", v50)
print(">60", v60)
print(">70", v70)
print(">80", v80)
print(">90", v90)
print("avg: ", sumSD/zal)
print("wrong: ", wrong)


# TODO empty list for RAM saving ?
#count_list_one = []
#count_list_two = []


# genrate k-mer list for PCA
bases = ['A', 'T', 'G', 'C']
kmer_list = []
k = 3
for i in range(1, k + 1):
     kmer_list.extend([''.join(p) for p in itertools.product(bases, repeat=i)])

#TODO
# pro seq
# pro sub seq
# Anz kmere x Anz subseqs
# dict statt matrix
# extra spalte damit usprungs sequ bekannt bleibt
# => df hat

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

