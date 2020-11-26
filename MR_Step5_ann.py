#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from MR_Step3 import *
import os 
import earthpy as et 
import trimesh as tm
import pyrender as pr
import pandas as pd
import pandas as pd
from annoy import AnnoyIndex

home_dict = et.io.HOME
desktop = os.path.join(et.io.HOME, 'Desktop')
target_dir = os.path.join(desktop, 'MR_Project')

#Check whether the directory exists 
if os.path.exists(target_dir) : 
    pass
else:
    print("Target directory does not exists, be sure where MR_Project file does exist")
    

def ann(mesh_name):
   
    
    class_list = list()
    mesh_list = list()
    dist = list()
    
    df = pd.read_csv(target_dir + '/Ready_outputs/all_features.csv')
    base_mesh = df.loc[df['Mesh'] == mesh_name]
    base_mesh_class = base_mesh.iloc[0,1]
    base_mesh = base_mesh.reset_index()
    
    base_mesh.drop('index', axis='columns', inplace=True)
    base_vector = base_mesh.iloc[0, 2:64].values.tolist()
    
    df = df.drop(df.loc[df['Mesh'] == base_mesh['Mesh'][0]].index, inplace= False)
    df = df.reset_index(drop=True)

    
    t = AnnoyIndex(62, 'euclidean')

    for row in df.index.values:
        vector = df.iloc[row, 2:64].values.tolist()
        t.add_item(row,vector) #a.add_item(i, v) adds item i (any nonnegative integer) with vector v. Note that it will allocate memory for max(i)+1 items.

    
    t.build(19)
    t.save('test.ann')
    
    u = AnnoyIndex(62, 'euclidean')
    u.load('test.ann')
    indices = u.get_nns_by_vector( base_vector, n =10, search_k = -1, include_distances= True)
    
    for index in indices[0]: 
        class_list.append(df.loc[index]['Class'])
        mesh_list.append(df.loc[index]['Mesh'])
    for distance in indices[1]: 
        dist.append(distance) 
    

    mesh_df = pd.DataFrame(mesh_list, columns = ['Mesh'])
    class_df = pd.DataFrame(class_list, columns = ['Class'])
    dist_df = pd.DataFrame(dist, columns =['Distance'])
    
    distance_df = mesh_features_merge(mesh_df, class_df)
    final_df = mesh_features_merge(distance_df, dist_df)
        
    return base_mesh_class, final_df


def ann_upload(mesh_features):
    import pandas as pd
    from annoy import AnnoyIndex
    
    class_list = list()
    mesh_list = list()
    dist = list()
    
    df = pd.read_csv(target_dir + '/Ready_outputs/all_features.csv')
    # base_mesh = df.loc[df['Mesh'] == mesh]
    # base_mesh = base_mesh.reset_index()
    # base_mesh.drop('index', axis='columns', inplace=True)
    # base_vector = base_mesh.iloc[0, 2:64].values.tolist()
    # df = df.drop(df.loc[df['Mesh'] == base_mesh['Mesh'][0]].index, inplace= False)
    # df = df.reset_index(drop=True)

    base_vector = mesh_features.values.tolist()
    
    t = AnnoyIndex(62, 'euclidean')

    for row in df.index.values:
        vector = df.iloc[row, 2:64].values.tolist()
        t.add_item(row,vector) #a.add_item(i, v) adds item i (any nonnegative integer) with vector v. Note that it will allocate memory for max(i)+1 items.

    
    t.build(19)
    t.save('test.ann')
    
    u = AnnoyIndex(62, 'euclidean')
    u.load('test.ann')
    indices = u.get_nns_by_vector( base_vector, n =10, search_k = -1, include_distances= True)
    
    for index in indices[0]: 
        class_list.append(df.loc[index]['Class'])
        mesh_list.append(df.loc[index]['Mesh'])
    for distance in indices[1]: 
        dist.append(distance) 
    

    mesh_df = pd.DataFrame(mesh_list, columns = ['Mesh'])
    class_df = pd.DataFrame(class_list, columns = ['Class'])
    dist_df = pd.DataFrame(dist, columns =['Distance'])
    
    distance_df = mesh_features_merge(mesh_df, class_df)
    final_df = mesh_features_merge(distance_df, dist_df)
        
         
    return final_df


'''
AnnoyIndex(f, metric) returns a new index that's read-write and stores vector of f dimensions. 
Metric can be "angular", "euclidean", "manhattan", "hamming", or "dot".
a.add_item(i, v) adds item i (any nonnegative integer) with vector v. 
Note that it will allocate memory for max(i)+1 items.
a.build(n_trees, n_jobs=-1) builds a forest of n_trees trees. More trees gives higher precision when querying. 
After calling build, no more items can be added. n_jobs specifies the number of threads 
used to build the trees. n_jobs=-1 uses all available CPU cores.
a.save(fn, prefault=False) saves the index to disk and loads it (see next function). 
After saving, no more items can be added.
a.load(fn, prefault=False) loads (mmaps) an index from disk. If prefault is set to True, 
it will pre-read the entire file into memory (using mmap with MAP_POPULATE). Default is False.
a.unload() unloads.
a.get_nns_by_item(i, n, search_k=-1, include_distances=False) returns the n closest items. 
During the query it will inspect up to search_k nodes which defaults to n_trees * n if not provided. 
search_k gives you a run-time tradeoff between better accuracy and speed. If you 
set include_distances to True, it will return a 2 element tuple with two lists in it: 
    the second one containing all corresponding distances.
a.get_nns_by_vector(v, n, search_k=-1, include_distances=False) same but query by vector v.
a.get_item_vector(i) returns the vector for item i that was previously added.
a.get_distance(i, j) returns the distance between items i and j. NOTE: this used 
to return the squared distance, but has been changed as of Aug 2016.
a.get_n_items() returns the number of items in the index.
a.get_n_trees() returns the number of trees in the index.
a.on_disk_build(fn) prepares annoy to build the index in the specified file instead 
of RAM (execute before adding items, no need to save after build)
a.set_seed(seed) will initialize the random number generator with the given seed. 
Only used for building up the tree, i. e. only necessary to pass this before adding 
the items. Will have no effect after calling a.build(n_trees) or a.load(fn).

'''




