# imports extern

# imports intern
#import src.file_reader as file
import file_reader as file
#import src.argument_parser as pars
import argument_parser as pars

# BedTools .getfasta for extracting sequence
# https://bedtools.readthedocs.io/en/latest/content/tools/getfasta.html
seq_one = file.bed_one.getfasta(fi=file.ref_fasta, s=True, bedOut=True, fo="firstSeq.fa.out")
seq_two = file.bed_two.getfasta(fi=file.ref_fasta, s=True, bedOut=True, fo="secondSeq.fa.out")

# save getfasta output to local variable
with open("firstSeq.fa.out", "r") as in_file:
    seq_one = in_file.readlines()
with open("secondSeq.fa.out", "r") as in_file:
    seq_two = in_file.readlines()


# concat seq_one and seq_two to seq_three
seq_three = seq_one + seq_two

# k-mer Lists calculation

# k-mer size
ksize = 3
if pars.args.ksize is not None:
    ksize = int(pars.args.ksize)


# getting k-mers from a single sequence
def make_kmer_list(seq, size, index):
    list_tmp = []
    n_kmers = len(seq) - size + 1
    for i in range(n_kmers):
        kmer = seq[i:i + size]
        list_tmp.append((kmer, index, i))  # offset = i
    return list_tmp


# make new list of unique k-mers
def remove_duplicates(list_in):
    list_out = []
    [list_out.append(x) for x in list_in if x not in list_out]
    return list_out

sub_seq_index = 0
list_unique = []  # only unique k-mers for each sub_seq
list_unique_one = []
list_unique_two = []
list_all = []  # for peak call later
# for sub_seq in range(0, len(seq_three)):
for sub_seq in range(0, len(seq_one)):
    # get k-mers for each sub_seq
    #out_list = make_kmer_list(seq_three[sub_seq], ksize, sub_seq_index)
    out_list = make_kmer_list(seq_one[sub_seq], ksize, sub_seq_index)
    # add to list_all
    list_all.extend(out_list)
    # remove non unique
    # list_unique.extend(remove_duplicates(out_list))  # or remove duplicates instead
    list_unique_one.extend(remove_duplicates(out_list))  # or remove duplicates instead
    sub_seq_index += 1


sub_seq_index = 0
for sub_seq in range(0, len(seq_two)):
    # get k-mers for each sub_seq
    out_list = make_kmer_list(seq_two[sub_seq], ksize, sub_seq_index)
    # add to list_all
    list_all.extend(out_list)
    # remove non unique
    list_unique_two.extend(remove_duplicates(out_list))  # or remove duplicates instead
    sub_seq_index += 1


list_unique = list_unique_one
list_unique.extend(list_unique_two)


# TODO if sub_seq count to big, RAM usage at 100% for Laptop
# empty now unused variables -> saving a little RAM
work_len = len(seq_three)
#print(work_len)
#if len(seq_three) > 10000:  # <- caps RAM at around 4 GB usage
#    work_len = 10000


work_len_one = len(seq_one)
work_len_two = len(seq_two)


# create k-mer counts matrix filled with 0's
# count_matrix = [[0.0 for i in range(work_len)] for j in range(work_len)]
#count_matrix = [[0.0 for i in range(work_len_one)] for j in range(work_len_two)]


# filling the matrix
pointerA = 0
pointerB = pointerA + 1


# following code commented out:
# original approach used a matrix to compare each element separately, resulting
# in a matrix sizes of span 100,000 x 100,000.


# while pointerA < work_len_one and pointerB < work_len_two:
# while pointerA < work_len and pointerB < work_len:
#while pointerA < len(list_unique) and pointerB < len(list_unique):
    # elem1 = list_unique[pointerA]
    # elem2 = list_unique[pointerB]
    # while pointerB < work_len_two and elem1[0] == elem2[0]:
#    while pointerB < len(list_unique) and list_unique[pointerA][0] == list_unique[pointerB][0]:
#        pointerB += 1
#    for elem_x in range(pointerA, pointerB):
        # elem_item_x = list_unique[elem_x]
#        for elem_y in range(pointerA, pointerB):
            # elem_item_y = list_unique[elem_y]
#            count_matrix[list_unique[elem_x][1]][list_unique[elem_y][1]] += 1
#    pointerA = pointerB
#    pointerB = pointerA + 1


# create similarity matrix filled with 0's
# sim_matrix = [[0 for i in range(len(list_unique))] for j in range(len(list_unique))]
# or update count_matrix instead


#for col in range(0, len(count_matrix)):
    # elem1 = list_unique[col]
    # Ki = len(list_unique[col][0]) - ksize + 1
#    Ki = len(seq_three[col]) - ksize + 1
#    for row in range(0, len(count_matrix[col])):
        # use Sorensen-Dice similarity index
        # elem2 = list_unique[row]
        # Kj = (len(list_unique[row][0]) - ksize + 1)
#        Kj = len(seq_three[row]) - ksize + 1
#        if Ki + Kj != 0:
            # sim_matrix[col][row] = (200 * count_matrix[col][row])/(Ki + Kj)
#            count_matrix[col][row] = (200 * count_matrix[col][row])/(Ki + Kj)
#        else:
            # sim_matrix[col][row] = 0
#            count_matrix[col][row] = 0


# comparing each element of one dataset against the average of the other


# counts of occurrences of kmers and similarity
# count_list = [0 for i in range(len(list_unique))]
count_list_one = [0 for i in range(len(seq_one))]
sim_list_one = count_list_one.copy()
count_list_two = [0 for i in range(len(seq_two))]
sim_list_two = count_list_two.copy()


while pointerA < len(list_unique_one) and pointerB < len(list_unique_two):
    while pointerB < len(list_unique_two) and list_unique_one[pointerA][0] == list_unique_two[pointerB][0]:
        pointerB += 1
    for elem_x in range(pointerA, pointerB):
        for elem_y in range(pointerA, pointerB):
            count_list_one[list_unique_one[elem_x][1]] += 1
            count_list_two[list_unique_two[elem_y][1]] += 1
            # or for count_list each
    pointerA = pointerB
    pointerB = pointerA + 1


# average value
Kj_avg = 0
Ki_avg = 0
for row in range(0, len(count_list_two)):
    Kj_avg += (len(seq_two[row]) / len(count_list_two)) - ksize + 1

for col in range(0, len(count_list_one)):
    Ki = len(seq_one[col]) - ksize + 1
    Ki_avg += Ki
    # use Sorensen-Dice similarity index
    if Ki + Kj_avg != 0:
        sim_list_one[col] = (200 * count_list_one[col])/(Ki + Kj_avg)
    else:
        sim_list_one[col] = 0

for row in range(0, len(count_list_two)):
    Kj = len(seq_two[row]) - ksize + 1
    if Ki_avg + Kj != 0:
        sim_list_two[row] = (200 * count_list_two[row])/(Ki_avg + Kj)
    else:
        sim_list_two[row] = 0

# TODO empty list for RAM saving ?
count_list_one = []
count_list_two = []
