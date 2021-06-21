# imports extern
import matplotlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
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
print("make PCA")

# projecting n-dimensional matrix to 2D
pca_SD_values = PCA(n_components=2)
pca_matrix_values = pca_SD_values.fit_transform(pre_calc.SD_matrix)

PCA_Df = pd.DataFrame(data=pca_matrix_values,
                      columns=['pca 1', 'pca 2'])

print('pca variation: {}'.format(pca_SD_values.explained_variance_ratio_))

# plot results for visualization
#plt.figure()
#plt.figure(figsize=(10, 10))
#plt.xticks(fontsize=12)
#plt.yticks(fontsize=14)
#plt.xlabel('pca comp 1', fontsize=20)
#plt.ylabel('pca comp 2', fontsize=20)
#plt.title("PCA of both datasets", fontsize=20)


