# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from scipy.stats import wasserstein_distance
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import *
from MR_Step3 import *
import os 
import earthpy as et 

home_dict = et.io.HOME
desktop = os.path.join(et.io.HOME, 'Desktop')
target_dir = os.path.join(desktop, 'MR_Project')

#Check whether the directory exists 
if os.path.exists(target_dir) : 
    print('True')
else:
    print("Target directory does not exists, be sure where MR_Project file does exist")

# df = pd.read_csv('C:/Users/hatta/Desktop/UU/Courses/Multimedia_Retrieval/step3/all_features.csv')
# mesh = pd.DataFrame(df.iloc[0,:]).T

#to display the results on gui window:
#final_df.iloc[0:21,:].to_string(index=False)


def global_dist(mesh):
    
    df = pd.read_csv(target_dir + '/Ready_outputs/all_features.csv')
    base_mesh = df.loc[df['Mesh'] == mesh]
    base_mesh = base_mesh.reset_index()
    base_mesh.drop('index', axis='columns', inplace=True)
    df.drop(df.loc[df['Mesh'] == base_mesh['Mesh'][0]].index, inplace=True)

    dist_list = list()
    mesh_list = list()
    class_list = list()
    for row in df.values:
         dist = pairwise_distances(np.asarray(base_mesh.iloc[0, 2:14]).reshape(1,-1),
                                   np.asarray(row[2:14]).reshape(1,-1),
                                   metric='euclidean')   
         dist = np.squeeze(dist) 
         dist = dist.tolist()
         dist_list.append(dist)
         mesh_list.append(row[0])
         class_list.append(row[1])
         
    scaler = StandardScaler()
    scaled_distances = scaler.fit_transform(np.asarray(dist_list).reshape(-1, 1))
        
    dist_df = pd.DataFrame(scaled_distances, columns =['glb_Distance'])
    mesh_df = pd.DataFrame(mesh_list, columns = ['Mesh'])
    class_df = pd.DataFrame(class_list, columns = ['Class'])
    
    distance_df = mesh_features_merge(mesh_df, class_df)
    final_df = mesh_features_merge(distance_df, dist_df)
    #final_df.sort_values('glb_Distance', inplace = True)
    
    return final_df

def a3_dist(mesh):
    
    df = pd.read_csv(target_dir + '/Ready_outputs/all_features.csv')
    base_mesh = df.loc[df['Mesh'] == mesh]
    base_mesh = base_mesh.reset_index()
    base_mesh.drop('index', axis='columns', inplace=True)
    df.drop(df.loc[df['Mesh'] == base_mesh['Mesh'][0]].index, inplace=True)
    
    #transform base mesh to np array
    bmesh = np.asarray(base_mesh)
    bmesh = np.squeeze(bmesh)
    
    distances = list()
    mesh_list = list()
    class_list = list()

    for row in df.values:
        #compare = df.iloc[0,14:25]
        comp = np.asarray(row)
        comp = np.squeeze(comp)
        dist = wasserstein_distance(bmesh[14:24], comp[14:24])
        distances.append(dist)
        mesh_list.append(comp[0])
        class_list.append(row[1])
        
    scaler = StandardScaler()
    scaled_distances = scaler.fit_transform(np.asarray(distances).reshape(-1, 1))
    
    dist_df = pd.DataFrame(scaled_distances, columns =['a3_Distance'])
    mesh_df = pd.DataFrame(mesh_list, columns = ['Mesh'])
    class_df = pd.DataFrame(class_list, columns = ['Class'])
    
    distance_df = mesh_features_merge(mesh_df, class_df)
    final_df = mesh_features_merge(distance_df, dist_df)
    #final_df.sort_values('a3_Distance', inplace = True)
    return final_df

def d1_dist(mesh):
    
    df = pd.read_csv(target_dir + '/Ready_outputs/all_features.csv')
    base_mesh = df.loc[df['Mesh'] == mesh]
    base_mesh = base_mesh.reset_index()
    base_mesh.drop('index', axis='columns', inplace=True)
    df.drop(df.loc[df['Mesh'] == base_mesh['Mesh'][0]].index, inplace=True)
    
    #transform base mesh to np array
    bmesh = np.asarray(base_mesh)
    bmesh = np.squeeze(bmesh)
    
    distances = list()
    mesh_list = list()
    class_list = list()
    
    for row in df.values:
        #compare = df.iloc[0,14:25]
        comp = np.asarray(row)
        comp = np.squeeze(comp)
        dist = wasserstein_distance(bmesh[24:34], comp[24:34])
        distances.append(dist)
        mesh_list.append(comp[0])
        class_list.append(row[1])
        
    scaler = StandardScaler()
    scaled_distances = scaler.fit_transform(np.asarray(distances).reshape(-1, 1))
    
    dist_df = pd.DataFrame(scaled_distances, columns =['d1_Distance'])
    mesh_df = pd.DataFrame(mesh_list, columns = ['Mesh'])
    class_df = pd.DataFrame(class_list, columns = ['Class'])
    
    distance_df = mesh_features_merge(mesh_df, class_df)
    final_df = mesh_features_merge(distance_df, dist_df)
    #final_df.sort_values('d1_Distance', inplace = True)
    return final_df

def d2_dist(mesh):
    
    df = pd.read_csv(target_dir + '/Ready_outputs/all_features.csv')
    base_mesh = df.loc[df['Mesh'] == mesh]
    base_mesh = base_mesh.reset_index()
    base_mesh.drop('index', axis='columns', inplace=True)
    df.drop(df.loc[df['Mesh'] == base_mesh['Mesh'][0]].index, inplace=True)
    
    #transform base mesh to np array
    bmesh = np.asarray(base_mesh)
    bmesh = np.squeeze(bmesh)
    
    distances = list()
    mesh_list = list()
    class_list = list()
    
    for row in df.values:
        #compare = df.iloc[0,14:25]
        comp = np.asarray(row)
        comp = np.squeeze(comp)
        dist = wasserstein_distance(bmesh[34:44], comp[34:44])
        distances.append(dist)
        mesh_list.append(comp[0])
        class_list.append(row[1])
        
    scaler = StandardScaler()
    scaled_distances = scaler.fit_transform(np.asarray(distances).reshape(-1, 1))
    
    dist_df = pd.DataFrame(scaled_distances, columns =['d2_Distance'])
    mesh_df = pd.DataFrame(mesh_list, columns = ['Mesh'])
    class_df = pd.DataFrame(class_list, columns = ['Class'])
    
    distance_df = mesh_features_merge(mesh_df, class_df)
    final_df = mesh_features_merge(distance_df, dist_df)
    #final_df.sort_values('d2_Distance', inplace = True)
    return final_df

def d3_dist(mesh):
    
    df = pd.read_csv(target_dir + '/Ready_outputs/all_features.csv')
    base_mesh = df.loc[df['Mesh'] == mesh]
    base_mesh = base_mesh.reset_index()
    base_mesh.drop('index', axis='columns', inplace=True)
    df.drop(df.loc[df['Mesh'] == base_mesh['Mesh'][0]].index, inplace=True)
    
    #transform base mesh to np array
    bmesh = np.asarray(base_mesh)
    bmesh = np.squeeze(bmesh)
    
    distances = list()
    mesh_list = list()
    class_list = list()
    
    for row in df.values:
        #compare = df.iloc[0,14:25]
        comp = np.asarray(row)
        comp = np.squeeze(comp)
        dist = wasserstein_distance(bmesh[44:54], comp[44:54])
        distances.append(dist)
        mesh_list.append(comp[0])
        class_list.append(row[1])
        
    scaler = StandardScaler()
    scaled_distances = scaler.fit_transform(np.asarray(distances).reshape(-1, 1))
    
    dist_df = pd.DataFrame(scaled_distances, columns =['d3_Distance'])
    mesh_df = pd.DataFrame(mesh_list, columns = ['Mesh'])
    class_df = pd.DataFrame(class_list, columns = ['Class'])
    
    distance_df = mesh_features_merge(mesh_df, class_df)
    final_df = mesh_features_merge(distance_df, dist_df)
    #final_df.sort_values('d3_Distance', inplace = True)
    return final_df

def d4_dist(mesh):
    
    df = pd.read_csv(target_dir + '/Ready_outputs/all_features.csv')
    base_mesh = df.loc[df['Mesh'] == mesh]
    base_mesh = base_mesh.reset_index()
    base_mesh.drop('index', axis='columns', inplace=True)
    df.drop(df.loc[df['Mesh'] == base_mesh['Mesh'][0]].index, inplace=True)
    
    #transform base mesh to np array
    bmesh = np.asarray(base_mesh)
    bmesh = np.squeeze(bmesh)
    
    distances = list()
    mesh_list = list()
    class_list = list()
    
    for row in df.values:
        #compare = df.iloc[0,14:25]
        comp = np.asarray(row)
        comp = np.squeeze(comp)
        dist = wasserstein_distance(bmesh[54:64], comp[54:64])
        distances.append(dist)
        mesh_list.append(comp[0])
        class_list.append(row[1])
        
    scaler = StandardScaler()
    scaled_distances = scaler.fit_transform(np.asarray(distances).reshape(-1, 1))
    
    dist_df = pd.DataFrame(scaled_distances, columns =['d4_Distance'])
    mesh_df = pd.DataFrame(mesh_list, columns = ['Mesh'])
    class_df = pd.DataFrame(class_list, columns = ['Class'])
    
    distance_df = mesh_features_merge(mesh_df, class_df)
    final_df = mesh_features_merge(distance_df, dist_df)
    #final_df.sort_values('d4_Distance', inplace = True)
    return final_df


def avg_dist(mesh):
    
    glb = global_dist(mesh)
    a3 = a3_dist(mesh)
    d1 = d1_dist(mesh)
    d2 = d2_dist(mesh)
    d3 = d3_dist(mesh)
    d4 = d4_dist(mesh)
    
    df = pd.DataFrame()
    

    df ['Mesh'] = glb["Mesh"].values
    df['Class'] = glb['Class'].values
    df['glb_Distance'] = glb['glb_Distance'].values
    df['a3_Distance'] = a3['a3_Distance'].values
    df['d1_Distance'] = d1['d1_Distance'].values
    df['d2_Distance'] = d2['d2_Distance'].values
    df['d3_Distance'] = d3['d3_Distance'].values
    df['d4_Distance'] = d4['d4_Distance'].values

    df['avg_Distance'] = df.mean(axis = 1)
    df.sort_values('avg_Distance', inplace = True) 
    return df
