# imports extern
import matplotlib
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

# TODO
# 1. PCA = Principal Components Analysis

# projecting n-dimensional matrix to 2D
#pca_SD_values = PCA(n_components=2)
#pca_matrix_values = pca_SD_values.fit_transform(pre_calc.SD_matrix)

#PCA_Df = pd.DataFrame(data=pca_matrix_values,
#                      columns=['pca 1', 'pca 2'])

#print('pca variation: {}'.format(pca_SD_values.explained_variance_ratio_))

# plot results for visualization
#plt.figure()
#plt.figure(figsize=(10, 10))
#plt.xticks(fontsize=12)
#plt.yticks(fontsize=14)
#plt.xlabel('pca comp 1', fontsize=20)
#plt.ylabel('pca comp 2', fontsize=20)
#plt.title("PCA of both datasets", fontsize=20)


# add dict values for best row and column value to data_frame
pd_first_values = pd.DataFrame(
    [pre_calc.dict_best_one[elem]] for elem in pre_calc.dict_best_one
)
pd_first_values.columns = ["first values"]
pd_second_values = pd.DataFrame(
    [pre_calc.dict_best_two[elem]] for elem in pre_calc.dict_best_two
)
pd_second_values.columns = ["second values"]


#print("converted to df")
#print(pd_first_values.head())
#print("second")
#print(pd_second_values.head())


pca_dataset = pd.concat([pd_first_values, pd_second_values], axis=1, join='inner')
#pd.DataFrame(columns=["first values", "second values"])

#print("made df")
#print(pca_dataset.head())



# TODO perform PCA from here on
# https://www.datacamp.com/community/tutorials/principal-component-analysis-in-python
# normalize values
#x = pca_dataset.loc[:, features].values
#x = StandardScaler().fit_transform(x) # normalizing the features
#x = StandardScaler().fit_transform(pca_dataset)  # normalizing the features
#x = [float(i)/max(pca_dataset[i][0]) for i in pca_dataset]
x = []
#normalized_values = pd.DataFrame(x)
for elem in range(0, len(pca_dataset)):
    #x.append([elem[0]/100, elem[1]])
    x.append(pca_dataset[elem]/100)


pca_values = PCA(n_components=2)
# reshape single feature array
#x = np.array reshape(x, (-1, 1))
x = np.array(x).reshape(int(len(x)/2), 2)
print(x.shape)
principalComponents_values = pca_values.fit_transform(x)

principal_values_Df = pd.DataFrame(data=principalComponents_values[0],
                                   columns=['principal component 1', 'principal component 2'])
print(principal_values_Df.tail())


print("end")
