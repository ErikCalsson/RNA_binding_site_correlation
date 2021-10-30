# imports extern
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

# imports intern
import sequence_pre_calculation as pre_calc
import graph_creation as graph_creat

# TODO statistical calculation here

#print("________________________")
#print(graph_creat.finalDf.head())
#print("________________________")


# sorting df after both pc columns
grouped_Df_first_col = graph_creat.finalDf
grouped_Df_second_col = graph_creat.finalDf
grouped_Df_first_col.sort_values(by=['target', 'principal component 1', 'principal component 2'], inplace=True)
grouped_Df_second_col.sort_values(by=['target', 'principal component 2', 'principal component 1'], inplace=True)


# getting min and max pca value
min_df_val = 0
max_df_val = 0

if grouped_Df_first_col["principal component 1"].iloc[0] < grouped_Df_second_col["principal component 2"].iloc[0]:
    min_df_val = grouped_Df_first_col["principal component 1"].iloc[0]
else:
    min_df_val = grouped_Df_second_col["principal component 2"].iloc[0]

if grouped_Df_first_col["principal component 1"].iloc[-1] > grouped_Df_second_col["principal component 2"].iloc[-1]:
    max_df_val = grouped_Df_first_col["principal component 1"].iloc[-1]
else:
    max_df_val = grouped_Df_second_col["principal component 2"].iloc[-1]


# separating PC1 and PC2 datasets
grouped_Df_first_col = grouped_Df_first_col[['principal component 1', 'target']]
grouped_Df_second_col = grouped_Df_second_col[['principal component 2', 'target']]


# separating seq 1 and seq 2 in both PCs, then dropping target column
df_first_s1 = grouped_Df_first_col.query('target == "seq_one"')
df_first_s1 = df_first_s1.drop('target', 1)
df_first_s2 = grouped_Df_first_col.query('target == "seq_two"')
df_first_s2 = df_first_s2.drop('target', 1)
df_second_s1 = grouped_Df_second_col.query('target == "seq_one"')
df_second_s1 = df_second_s1.drop('target', 1)
df_second_s2 = grouped_Df_second_col.query('target == "seq_two"')
df_second_s2 = df_second_s2.drop('target', 1)

#print("!!")
#print(df_first_s1.head())
#print("!!")


# grouping counts with cut. range of bins = 0.1 for
# cut(PC1 seq 1) vs cut(PC1 seq 2) and same with PC2
custom_bins = bins = np.arange(min_df_val, max_df_val + 0.1, 0.1)
df_first_s1['grouped'] = pd.cut(x=df_first_s1['principal component 1'],
                                bins=custom_bins)
df_first_s2['grouped'] = pd.cut(x=df_first_s2['principal component 1'],
                                bins=custom_bins)
df_second_s1['grouped'] = pd.cut(x=df_second_s1['principal component 2'],
                                 bins=custom_bins)
df_second_s2['grouped'] = pd.cut(x=df_second_s2['principal component 2'],
                                 bins=custom_bins)

# sorting after groups
df_first_s1.sort_values('grouped')
df_first_s2.sort_values('grouped')
df_second_s1.sort_values('grouped')
df_second_s2.sort_values('grouped')

# count occurrences of each group and normalize them
counted_first_s1 = df_first_s1['grouped'].value_counts(normalize=False).sort_index()
counted_first_s2 = df_first_s2['grouped'].value_counts(normalize=False).sort_index()
counted_second_s1 = df_second_s1['grouped'].value_counts(normalize=False).sort_index()
counted_second_s2 = df_second_s2['grouped'].value_counts(normalize=False).sort_index()

# turn Series into DataFrames
df_counted_first_s1 = pd.DataFrame({'range': counted_first_s1.index, 'counts_col1_seq1': counted_first_s1.values})
df_counted_first_s2 = pd.DataFrame({'range': counted_first_s2.index, 'counts_col1_seq2': counted_first_s2.values})
df_counted_second_s1 = pd.DataFrame({'range': counted_second_s1.index, 'counts_col2_seq1': counted_second_s1.values})
df_counted_second_s2 = pd.DataFrame({'range': counted_second_s2.index, 'counts_col2_seq2': counted_second_s2.values})

# combine to single Dataframe
df_counts_PC_1 = pd.merge(df_counted_first_s1, df_counted_first_s2)
df_counts_PC_2 = pd.merge(df_counted_second_s1, df_counted_second_s2)
df_merged_PCs = pd.merge(df_counts_PC_1, df_counts_PC_2)

print("!!!!")
print(df_counts_PC_1.head())


# bar chart for all
#https://stackoverflow.com/questions/29498652/plot-bar-graph-from-pandas-dataframe
ax = df_counts_PC_1[['counts_col1_seq1', 'counts_col1_seq2']].plot(kind='bar',
                                                                   title="Grouped PC values",
                                                                   figsize=(10, 12),
                                                                   legend=True,
                                                                   fontsize=12,
                                                                   alpha=0.3)
ax.set_xlabel("range", fontsize=12)
ax.set_ylabel("counts", fontsize=12)
plt.bar
plt.savefig('barGroupPC1.png')

ax = df_counts_PC_2[['counts_col2_seq1', 'counts_col2_seq2']].plot(kind='bar',
                                                                   title="Grouped PC values",
                                                                   figsize=(10, 12),
                                                                   legend=True,
                                                                   fontsize=12,
                                                                   alpha=0.3)
ax.set_xlabel("range", fontsize=12)
ax.set_ylabel("counts", fontsize=12)
plt.bar
plt.savefig('barGroupPC2.png')


#TODO stat. test!


# perform independent two sided t test
result_PC_1 = ttest_ind(df_counts_PC_1['counts_col1_seq1'], df_counts_PC_1['counts_col1_seq2'], equal_var=False)
result_PC_2 = ttest_ind(df_counts_PC_2['counts_col2_seq1'], df_counts_PC_2['counts_col2_seq2'], equal_var=False)

print('test:')
print(result_PC_1)
print(result_PC_2)


