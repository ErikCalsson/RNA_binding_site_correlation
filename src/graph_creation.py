# imports extern
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import scale
from sklearn import model_selection
from sklearn.model_selection import RepeatedKFold
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# imports intern
import sequence_pre_calculation as pre_calc

# add dict values for best row and column value to data_frame
#pd_first_values = pd.DataFrame(
#    [pre_calc.dict_best_one[elem]] for elem in pre_calc.dict_best_one
#)
#pd_first_values.columns = ["first values"]
#pd_second_values = pd.DataFrame(
#    [pre_calc.dict_best_two[elem]] for elem in pre_calc.dict_best_two
#)
#pd_second_values.columns = ["second values"]

# TODO
# 1. PCA = Principal Components Analysis


#pre_calc.kmer_matrix
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

fig = plt.figure(figsize=(8, 8))
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
               , s=50)
ax.legend(targets)
ax.grid()

fig.savefig('plot.png')


#print("first________________________________")
#print(kmer_dataset.head())
#print("________________________________")
#print(kmer_dataset.tail())
#print("first________________________________")
#
# TODO perform PCA from here on
# https://www.datacamp.com/community/tutorials/principal-component-analysis-in-python
## normalize values
##x = StandardScaler().fit_transform(pre_calc.kmer_matrix)
#x = StandardScaler().fit_transform(pre_calc.list_all_kmer_counts)
#
#seq_cols = [pre_calc.kmer_list[i] for i in range(x.shape[1])]
#seq_cols = [pre_calc.list_all_kmer_counts[i] for i in range(x.shape[1])]
#normalised_kmers = pd.DataFrame(x, columns=seq_cols)
#print("demo____________________")
#print(normalised_kmers.head())
#print("demo____________________")
##!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
##label fehlt für image
##normalised_kmers = normalised_kmers.assign(label=['seq_one', 'seq_two'])
#normalised_kmers = normalised_kmers.assign(label='seqs')
#
#pca_kmers = PCA(n_components=2)
#principalComponents_kmers = pca_kmers.fit_transform(x)
#print(principalComponents_kmers)
#
## create a DataFrame for PCA values
#principal_kmers_Df = pd.DataFrame(data=principalComponents_kmers
#             ,columns=['principal component 1', 'principal component 2'])
#
#print("-----------------df")
#print(principal_kmers_Df.head())
#print("-----------------df")
#
## make figure
#fig = plt.figure()
#plt.figure(figsize=(10, 10))
#plt.xticks(fontsize=12)
#plt.yticks(fontsize=14)
#plt.xlabel('Principal Component - 1', fontsize=20)
#plt.ylabel('Principal Component - 2', fontsize=20)
#plt.title("Principal Component Analysis of kmer counts", fontsize=20)
#targets = ['seq_one', 'seq_two']
##targets = [principalComponents_kmers[0], principalComponents_kmers[1]]
#colors = ['r', 'g']
#for target, color in zip(targets, colors):
#    indicesToKeep = normalised_kmers['label'] == target
#    plt.scatter(principal_kmers_Df.loc[indicesToKeep, 'principal component 1']
#               , principal_kmers_Df.loc[indicesToKeep, 'principal component 2'], c=color, s=50)
#
#plt.legend(targets, prop={'size': 15})
#
## TODO output figure
#fig.savefig('plot.png')

