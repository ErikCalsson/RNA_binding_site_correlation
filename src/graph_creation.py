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

# TODO perform PCA from here on
# https://www.datacamp.com/community/tutorials/principal-component-analysis-in-python
# normalize values
x = StandardScaler().fit_transform(pre_calc.kmer_matrix)

seq_cols = [pre_calc.kmer_list[i] for i in range(x.shape[1])]
normalised_kmers = pd.DataFrame(x, columns=seq_cols)
normalised_kmers = normalised_kmers.assign(label=['seq_one', 'seq_two'])
print(normalised_kmers.tail())

pca_kmers = PCA(n_components=2)
principalComponents_kmers = pca_kmers.fit_transform(x)
print(principalComponents_kmers)

# create a DataFrame for PCA values
principal_kmers_Df = pd.DataFrame(data=principalComponents_kmers
             ,columns=['principal component 1', 'principal component 2'])

# make figure
fig = plt.figure()
plt.figure(figsize=(10, 10))
plt.xticks(fontsize=12)
plt.yticks(fontsize=14)
plt.xlabel('Principal Component - 1', fontsize=20)
plt.ylabel('Principal Component - 2', fontsize=20)
plt.title("Principal Component Analysis of kmer counts", fontsize=20)
targets = ['seq_one', 'seq_two']
#targets = [principalComponents_kmers[0], principalComponents_kmers[1]]
colors = ['r', 'g']
for target, color in zip(targets, colors):
    indicesToKeep = normalised_kmers['label'] == target
    plt.scatter(principal_kmers_Df.loc[indicesToKeep, 'principal component 1']
               , principal_kmers_Df.loc[indicesToKeep, 'principal component 2'], c=color, s=50)

plt.legend(targets, prop={'size': 15})

# TODO output figure
fig.savefig('plot.png')

print("end")
