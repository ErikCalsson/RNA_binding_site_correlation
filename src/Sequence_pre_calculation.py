# imports extern

# imports intern
import src.file_reader as file
import src.argument_parser as pars

# BedTools .getfasta for extracting sequence
# https://bedtools.readthedocs.io/en/latest/content/tools/getfasta.html
seq_one = file.bed_one.getfasta(fi=file.ref_fasta, s=True, bedOut=True, fo="seqOne.fa.out")
seq_two = file.bed_two.getfasta(fi=file.ref_fasta, s=True, bedOut=True, fo="seqTwo.fa.out")

# save getfasta output to local variable
with open("seqOne.fa.out", "r") as in_file:
    seq_one = in_file.readlines()
with open("seqTwo.fa.out", "r") as in_file:
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
list_all = []  # for peak call later
for sub_seq in range(0, len(seq_three)):
    # get k-mers for each sub_seq
    out_list = make_kmer_list(seq_three[sub_seq], ksize, sub_seq_index)
    # add to list_all
    #list_all.extend(out_list)
    # remove non unique
    list_unique.extend(remove_duplicates(out_list))  # or remove duplicates instead
    sub_seq_index += 1

# dict_unique = dict(list_unique)
# dict_all = dict(list_all)

# TODO if kmer count to big, RAM usage at 100% for Laptop
# empty now unused variables -> saving a little RAM
seq_one = []
seq_two = []
work_len = len(list_unique)
if len(list_unique) > 10000:  # <- caps RAM at around 4 GB usage
    work_len = 10000

# create k-mer counts matrix filled with 0's
#count_matrix = [[0 for i in range(len(list_unique))] for j in range(len(list_unique))]
count_matrix = [[0.0 for i in range(work_len)] for j in range(work_len)]


# filling the matrix
pointerA = 0
pointerB = pointerA + 1
#while pointerA < len(list_unique) and pointerB < len(list_unique):
while pointerA < work_len and pointerB < work_len:
    # elem1 = list_unique[pointerA]
    # elem2 = list_unique[pointerB]
    #while pointerB < len(list_unique) and elem1[0] == elem2[0]:
    while pointerB < work_len and list_unique[pointerA][0] == list_unique[pointerB][0]:
        pointerB += 1
    for elem_x in range(pointerA, pointerB):
        # elem_item_x = list_unique[elem_x]
        for elem_y in range(pointerA, pointerB):
            # elem_item_y = list_unique[elem_y]
            count_matrix[list_unique[elem_x][1]][list_unique[elem_y][1]] += 1
    pointerA = pointerB
    pointerB = pointerA + 1


# create similarity matrix filled with 0's
# sim_matrix = [[0 for i in range(len(list_unique))] for j in range(len(list_unique))]
# or update count_matrix instead


for col in range(0, len(count_matrix)):
    # elem1 = list_unique[col]
    # Ki = len(list_unique[col][0]) - ksize + 1
    Ki = len(seq_three[col]) - ksize + 1
    for row in range(0, len(count_matrix[col])):
        # use Sorensen-Dice similarity index
        # elem2 = list_unique[row]
        # Kj = (len(list_unique[row][0]) - ksize + 1)
        Kj = len(seq_three[row]) - ksize + 1
        if Ki + Kj != 0:
            # sim_matrix[col][row] = (200 * count_matrix[col][row])/(Ki + Kj)
            count_matrix[col][row] = (200 * count_matrix[col][row])/(Ki + Kj)
        else:
            # sim_matrix[col][row] = 0
            count_matrix[col][row] = 0
