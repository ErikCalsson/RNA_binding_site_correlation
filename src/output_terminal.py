# imports extern

# imports intern
import  src.Sequence_pre_calculation as calc



# start terminal output
def use_terminal():
    #for i in calc.sim_matrix:
    for i in calc.count_matrix:
        print('\t'.join(map(str, i)))
