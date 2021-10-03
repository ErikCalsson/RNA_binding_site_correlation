# imports extern
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
#from sklearn.preprocessing import scale
#from sklearn import model_selection
#from sklearn.model_selection import RepeatedKFold
#from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
#from sklearn.linear_model import LinearRegression
#from sklearn.metrics import mean_squared_error
from matplotlib import pyplot

# imports intern
import sequence_pre_calculation as pre_calc

# pre_calc.kmer_matrix
kmer_dataset = pd.DataFrame(pre_calc.list_all_kmer_counts)

# https://towardsdatascience.com/pca-using-python-scikit-learn-e653f8989e60

features = []  # features
y = []  # targets
for i in range(0, kmer_dataset.shape[1]):
    features.append(i)

x = kmer_dataset.loc[:, features].values

# add column with data origin
origin_of_seq = []
for sub_seq in pre_calc.seq_one:
    origin_of_seq.append('seq_one')
for sub_seq in pre_calc.seq_two:
    origin_of_seq.append('seq_two')
kmer_dataset['target'] = origin_of_seq

y = kmer_dataset.loc[:, ['target']].values

x = StandardScaler().fit_transform(x)
pca = PCA(n_components=2)
principalComponents = pca.fit_transform(x)
principalDf = pd.DataFrame(data=principalComponents,
                           columns=['principal component 1', 'principal component 2'])

finalDf = pd.concat([principalDf, kmer_dataset[['target']]], axis=1)


fig = plt.figure(figsize=(12, 12))
ax = fig.add_subplot(1, 1, 1)
ax.set_xlabel('Principal Component 1', fontsize=15)
ax.set_ylabel('Principal Component 2', fontsize=15)
ax.set_title('2 component PCA', fontsize=20)
targets = ['seq_one', 'seq_two']
colors = ['r', 'b']
for target, color in zip(targets, colors):
    indicesToKeep = finalDf['target'] == target
    ax.scatter(finalDf.loc[indicesToKeep, 'principal component 1']
               , finalDf.loc[indicesToKeep, 'principal component 2']
               , c=color
               , s=10
               , alpha=0.2)
ax.legend(targets)
ax.grid()

fig.savefig('plot.png')

fig = plt.figure(figsize=(12, 12))
ax = fig.add_subplot(1, 1, 1)
ax.set_xlabel('Principal Component 1', fontsize=15)
ax.set_ylabel('Principal Component 2', fontsize=15)
ax.set_title('2 component PCA', fontsize=20)
targets = ['seq_one']
colors = ['r']
for target, color in zip(targets, colors):
    indicesToKeep = finalDf['target'] == target
    ax.scatter(finalDf.loc[indicesToKeep, 'principal component 1']
               , finalDf.loc[indicesToKeep, 'principal component 2']
               , c=color
               , s=10
               , alpha=0.2)
ax.legend(targets)
ax.grid()
fig.savefig('plot_seq_one.png')

fig = plt.figure(figsize=(12, 12))
ax = fig.add_subplot(1, 1, 1)
ax.set_xlabel('Principal Component 1', fontsize=15)
ax.set_ylabel('Principal Component 2', fontsize=15)
ax.set_title('2 component PCA', fontsize=20)
targets = ['seq_two']
colors = ['b']
for target, color in zip(targets, colors):
    indicesToKeep = finalDf['target'] == target
    ax.scatter(finalDf.loc[indicesToKeep, 'principal component 1']
               , finalDf.loc[indicesToKeep, 'principal component 2']
               , c=color
               , s=10
               , alpha=0.2)
ax.legend(targets)
ax.grid()
fig.savefig('plot_seq_two.png')


# making histogram for PCA values values
bins = np.linspace(-10, 10, 100)

fig, ax = pyplot.subplots()
# indicesToKeep = finalDf['target'] == ['seq_one']
# pyplot.hist(finalDf.loc[indicesToKeep, 'principal component 2'], bins, alpha=0.1, label='pca_2')
pyplot.hist(finalDf['principal component 1'], bins, color='red', alpha=0.1, label='pca_1')
# targets = ['seq_two']
# indicesToKeep = finalDf['target'] == ['seq_two']
# pyplot.hist(finalDf.loc[indicesToKeep, 'principal component 2'], bins, alpha=0.1, label='pca_2')
pyplot.hist(finalDf['principal component 2'], bins, color='blue', alpha=0.1, label='pca_2')
pyplot.legend(loc='upper right')
fig.savefig('hist_PCA_values.png')


# grouping data points


# combining points when +- 5% similarity
#https://stackoverflow.com/questions/59490101/combine-near-scatter-points-into-one-and-increase-its-size

#groupedDf = pd.DataFrame()

# similarity range
#sim_range = 5

#max_len = finalDf.shape[0]
#outer_indices = 1
#inner_indices = 2
#containing = 0

#entry = finalDf.loc[0]
#groupedDf = groupedDf.append([entry])

#for outer_indices, outer_row in finalDf.iterrows():
#    max_border1 = outer_row[0] + sim_range * outer_row[0] / 100
#    min_border1 = outer_row[0] - sim_range * outer_row[0] / 100
#    max_border2 = outer_row[1] + sim_range * outer_row[1] / 100
#    min_border2 = outer_row[1] - sim_range * outer_row[1] / 100
#    for inner_indices, inner_row in groupedDf.iterrows():
#        if outer_row[2] == inner_row[2]:
#            if min_border1 < inner_row[0] < max_border1 and min_border2 < inner_row[1] < max_border2:
#                containing = 1


                #entry = finalDf.loc[outer_indices]
                #groupedDf = groupedDf.append([entry])

                #groupedDf = groupedDf.append(finalDf.iloc[[outer_indices]])
                #groupedDf = groupedDf.append(finalDf.iloc[outer_row])

#    if containing != 1:
#        entry = finalDf.loc[outer_indices]
#        groupedDf = groupedDf.append([entry])
#
#    containing = 0


#while outer_indices < max_len:
#    max_border1 = groupedDf.iat[outer_indices, 0] + sim_range * groupedDf.iat[outer_indices, 0] / 100
#    max_border2 = groupedDf.iat[outer_indices, 1] - sim_range * groupedDf.iat[outer_indices, 1] / 100
#    min_border1 = groupedDf.iat[outer_indices, 0] + sim_range * groupedDf.iat[outer_indices, 0] / 100
#    min_border2 = groupedDf.iat[outer_indices, 1] - sim_range * groupedDf.iat[outer_indices, 1] / 100
#    while inner_indices < max_len:
#        if groupedDf.iat[outer_indices, 2] == groupedDf.iat[inner_indices, 2]:
#            if min_border1 < groupedDf.iat[inner_indices, 0] < max_border1 and\
#                    min_border2 < groupedDf.iat[inner_indices, 1] < max_border2:
#                groupedDf = groupedDf.drop(groupedDf.index[[inner_indices]])
#                max_len -= 1
#        else:
#            inner_indices += 1
#    outer_indices += 1

#for outer_indices, outer_row in groupedDf.iterrows():
#    max_border1 = outer_row[0] + sim_range * outer_row[0] / 100
#    max_border2 = outer_row[1] - sim_range * outer_row[1] / 100
#    min_border1 = outer_row[0] + sim_range * outer_row[0] / 100
#    min_border2 = outer_row[1] - sim_range * outer_row[1] / 100
#    for inner_indices, inner_row in groupedDf.iterrows():
#        if outer_row[2] == inner_row[2]:
#            if min_border1 < inner_row[0] < max_border1 and min_border2 < inner_row[1] < max_border2:
#                groupedDf = groupedDf.drop(groupedDf.index[[inner_indices]])


#print("shape: ", finalDf.shape)
#print("shape: ", groupedDf.shape)
#print(groupedDf.head())
#
#fig = plt.figure(figsize=(12, 12))
#ax = fig.add_subplot(1, 1, 1)
#ax.set_xlabel('Principal Component 1', fontsize=15)
#ax.set_ylabel('Principal Component 2', fontsize=15)
#ax.set_title('2 component PCA', fontsize=20)
#targets = ['seq_one', 'seq_two']
#colors = ['r', 'b']
#for target, color in zip(targets, colors):
#    indicesToKeep = groupedDf['target'] == target
#    ax.scatter(groupedDf.loc[indicesToKeep, 'principal component 1']
#               , groupedDf.loc[indicesToKeep, 'principal component 2']
#               , c=color
#               , s=10
#               , alpha=0.2)
#ax.legend(targets)
#ax.grid()
#
#fig.savefig('plot_less_points.png')




#finalDf.sort_values(by=['target', 'principal component 1', 'principal component 2'], inplace=True)

#print("________________________")
#print(finalDf.head())
#print(finalDf.tail())
#print("________________________")

#df = df.drop(df.index [ [ 0,2 ] ])    delete rows 1 and 3,
#df = df.drop('Harry Porter')     delete row with entry

# grouping df entries by removing them, if to similar to surrounding values
# deleting by 'principal component 1' comparison



# deleting by 'principal component 2' comparison
#finalDf.sort_values(by=['target', 'principal component 2', 'principal component 1'], inplace=True)

