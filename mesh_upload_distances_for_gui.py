# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from scipy.stats import wasserstein_distance
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import *
from MR_Step3 import *


'''All these distance calculation functions are for GUI to calculate the distance 
between a single user-uploaded mesh and all the meshes' features in the db'''

def global_m_dist(mesh):
    
    df = pd.read_csv('C:/Users/hatta/Desktop/UU/Courses/Multimedia_Retrieval/step3/all_features.csv')

    dist_list = list()
    mesh_list = list()
    class_list = list()
    
    #transform the mesh to np array
    bmesh = np.asarray(mesh)
    bmesh = np.squeeze(bmesh)
    
    for row in df.values:
         dist = pairwise_distances(np.asarray(bmesh[0:12]).reshape(1,-1),
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

def a3_m_dist(mesh):
    
    df = pd.read_csv('C:/Users/hatta/Desktop/UU/Courses/Multimedia_Retrieval/step3/all_features.csv')
    
    #transform the mesh to np array
    bmesh = np.asarray(mesh)
    bmesh = np.squeeze(bmesh)
    
    distances = list()
    mesh_list = list()
    class_list = list()

    for row in df.values:
        #compare = df.iloc[0,14:25]
        comp = np.asarray(row)
        comp = np.squeeze(comp)
        dist = wasserstein_distance(bmesh[12:22], comp[14:24])
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

def d1_m_dist(mesh):
    
    df = pd.read_csv('C:/Users/hatta/Desktop/UU/Courses/Multimedia_Retrieval/step3/all_features.csv')

    #transform base mesh to np array
    bmesh = np.asarray(mesh)
    bmesh = np.squeeze(bmesh)
    
    distances = list()
    mesh_list = list()
    class_list = list()
    
    for row in df.values:
        #compare = df.iloc[0,14:25]
        comp = np.asarray(row)
        comp = np.squeeze(comp)
        dist = wasserstein_distance(bmesh[22:32], comp[24:34])
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

def d2_m_dist(mesh):
    
    df = pd.read_csv('C:/Users/hatta/Desktop/UU/Courses/Multimedia_Retrieval/step3/all_features.csv')
  
    #transform base mesh to np array
    bmesh = np.asarray(mesh)
    bmesh = np.squeeze(bmesh)
    
    distances = list()
    mesh_list = list()
    class_list = list()
    
    for row in df.values:
        #compare = df.iloc[0,14:25]
        comp = np.asarray(row)
        comp = np.squeeze(comp)
        dist = wasserstein_distance(bmesh[32:42], comp[34:44])
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

def d3_m_dist(mesh):
    
    df = pd.read_csv('C:/Users/hatta/Desktop/UU/Courses/Multimedia_Retrieval/step3/all_features.csv')

    #transform base mesh to np array
    bmesh = np.asarray(mesh)
    bmesh = np.squeeze(bmesh)
    
    distances = list()
    mesh_list = list()
    class_list = list()
    
    for row in df.values:
        #compare = df.iloc[0,14:25]
        comp = np.asarray(row)
        comp = np.squeeze(comp)
        dist = wasserstein_distance(bmesh[42:52], comp[44:54])
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

def d4_m_dist(mesh):
    
    df = pd.read_csv('C:/Users/hatta/Desktop/UU/Courses/Multimedia_Retrieval/step3/all_features.csv')
    
    #transform base mesh to np array
    bmesh = np.asarray(mesh)
    bmesh = np.squeeze(bmesh)
    
    distances = list()
    mesh_list = list()
    class_list = list()
    
    for row in df.values:
        #compare = df.iloc[0,14:25]
        comp = np.asarray(row)
        comp = np.squeeze(comp)
        dist = wasserstein_distance(bmesh[52:62], comp[54:64])
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


def avg_mesh_dist(mesh):
    
    glb = global_m_dist(mesh)
    a3 = a3_m_dist(mesh)
    d1 = d1_m_dist(mesh)
    d2 = d2_m_dist(mesh)
    d3 = d3_m_dist(mesh)
    d4 = d4_m_dist(mesh)
    
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
