# imports extern
import pandas as pd
import numpy as np

# imports intern
import sequence_pre_calculation as pre_calc
import graph_creation as graph_creat

# TODO statistical calculation here

print("________________________")
print(graph_creat.finalDf.head())
print("________________________")

#TODO !!!!!!!!!!!!!!!
# review code below, wrong attempt
# automatic class creation for each column (X, Y axis separately)
# normalizing each of the two on its own
# bar chart for test


grouped_Df_first_col = graph_creat.finalDf  # pd.DataFrame()
grouped_Df_first_col['my index'] = range(1, len(grouped_Df_first_col) + 1)
grouped_Df_second_col = graph_creat.finalDf  # pd.DataFrame()
grouped_Df_second_col['my index'] = range(1, len(grouped_Df_second_col) + 1)


grouped_Df_first_col.sort_values(by=['target', 'principal component 1', 'principal component 2'], inplace=True)
grouped_Df_second_col.sort_values(by=['target', 'principal component 2', 'principal component 1'], inplace=True)


# similarity range
sim_range = 5  # 2.5  # ~ -+5%


# first try, collect my_index entries for groups
def group_by_col(in_df, col_nr, sim_rng):
    out_matrix = np.empty((0, 0))
    add_list = []
    comp_row = in_df.head(1)
    max_border = comp_row[col_nr] + sim_rng * comp_row[col_nr] / 100
    for index, row in in_df.iterrows():
    #for row in range(1, in_df.shape[0]):
        # if row[col_nr] <= max_border:
        while row[col_nr] <= max_border:
            for index2, row2 in in_df.iterrows():
                add_list.append(row2[3])
        out_matrix = np.append(out_matrix, add_list, axis=0)  # .__add__(add_list)
        add_list.clear()
        max_border = row2[col_nr] + sim_rng * row2[col_nr] / 100
        # min_border = row[col_nr] - sim_rng * row[col_nr] / 100
    return out_matrix


# grouping similar row/column values by custom index
index_grouped_first = group_by_col(grouped_Df_first_col, 0, 5)
index_grouped_second = group_by_col(grouped_Df_second_col, 1, 5)


# emptying sorted df's for RAM
#grouped_Df_first_col = grouped_Df_first_col.iloc[0:0]
#grouped_Df_second_col = grouped_Df_second_col.iloc[0:0]


# new df by selecting intersection of custom index
keep_list = []
keep_matrix = np.empty((0, 0))
for outer_group in index_grouped_first:
    for inner_group in index_grouped_second:
        keep_list.append(outer_group.intersection(inner_group))
        keep_matrix = np.append(keep_matrix, keep_list, axis=0)
        keep_list.clear()


# removing not needed row from df, keeping only first
print(graph_creat.finalDf.shape)

# "drop df.row[my_index]" for all lists in keep_matrix except each first entry

#grouped_final_Df = graph_creat.finalDf


#max_len = finalDf.shape[0]
#outer_indices = 1
#inner_indices = 2
#containing = 0

#entry = finalDf.loc[0]
#groupedDf = groupedDf.append([entry])

#for outer_indices, outer_row in groupedDf.iterrows():
#    max_border1 = outer_row[0] + sim_range * outer_row[0] / 100
#    max_border2 = outer_row[1] - sim_range * outer_row[1] / 100
#    min_border1 = outer_row[0] + sim_range * outer_row[0] / 100
#    min_border2 = outer_row[1] - sim_range * outer_row[1] / 100
#    for inner_indices, inner_row in groupedDf.iterrows():
#        if outer_row[2] == inner_row[2]:
#            if min_border1 < inner_row[0] < max_border1 and min_border2 < inner_row[1] < max_border2:
#                groupedDf = groupedDf.drop(groupedDf.index[[inner_indices]])

#print(">= 95     : %d , %d" % (ov95[0]/len(pre_calc.seq_one), ov95[1]/len(pre_calc.seq_two)))

