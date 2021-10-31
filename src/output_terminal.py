# imports extern

# imports intern
# import sequence_pre_calculation as calc
# import graph_creation as graph
import data_calculation as dat


# start terminal output
def use_terminal():
    print("See output barGroupPC1.png or barGroupPC2.png for visualisation of final results")
    # output message with statistic
    print("PC1: ", str(dat.result_PC_1[0]) + ",p-value: ", dat.result_PC_1[1])
    print("PC2: ", dat.result_PC_2[0], ",p-value: ", dat.result_PC_2[1])
    print("remember: t > T and alpha > p-value")
    print("T = [ 0.995 -> 2.576, 0.99 -> 2.326, 0.975 -> 1.96, 0.95 -> 1.645]")

