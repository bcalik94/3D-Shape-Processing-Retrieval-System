# -*- coding: utf-8 -*-

from __future__ import print_function
import time
from sklearn.manifold import TSNE
import pandas as pd
import matplotlib.pyplot as plt
import os 
import earthpy as et 

home_dict = et.io.HOME
desktop = os.path.join(et.io.HOME, 'Desktop')
target_dir = os.path.join(desktop, 'MR_Project')

#Check whether the directory exists 
if os.path.exists(target_dir) : 
    print('True')
else:
    print("Target directory does not exist, be sure where MR_Project file does exist")

#t-SNE function to calculate and visualize the shape dataset in 2D
def t_sne():
    df = pd.read_csv(target_dir + '/Ready_outputs/all_features.csv')
    x = df.iloc[:, 2:]
    y = df.iloc[:, 1]
    time_start = time.time()
    tsne = TSNE(n_components=2, verbose=1, perplexity=7, learning_rate=100, n_iter=5000)
    tsne_results = tsne.fit_transform(x)
    print('t-SNE done! Time elapsed: {} seconds'.format(time.time()-time_start))
    
    fig, ax = plt.subplots()
    colors = ['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99', '#e31a1c', 
              '#fdbf6f', '#ff7f00', '#cab2d6', '#6a3d9a', '#ffff99', '#543005',
              '#35978f', '#bf812d', '#000000', '#808080', '#d9d9d9', '#fccde5', 
              '#b41f35', '#fce803']
    groups = pd.DataFrame(tsne_results, columns=['x', 'y']).assign(category=y).groupby('category')
    
    ax.set_prop_cycle('color', colors)
    for name, points in groups:
        ax.scatter(points.x, points.y, label=name, )
    
    ax.legend()
    
t_sne()
