# -*- coding: utf-8 -*-

#Feature Extraction Functions
from scipy.spatial.distance import pdist
from matplotlib import pyplot as plt
from pathlib import Path
import os.path
import math as m
import numpy as np
import trimesh as tm
import pandas as pd
import random
import math
from sklearn.preprocessing import StandardScaler
from MR_Step2 import *
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


#GLOBAL DESCRIPTORS
#non-standardized global features in the database
def original_global_features(in_dir, out_dir):
    csv = pd.read_csv(target_dir + '/Ready_outputs/3DImageInfo_before.csv')
    d = []
    
    for filename in os.listdir(in_dir):
        current_dir = in_dir + '/' + filename        
        split_string = filename.split("_")
        class_name = split_string[0] 
        file_name = split_string[1] 
        mesh = tm.load(current_dir) 
        
        #volume
        V = csv.loc[csv['Image File'] == file_name, 'Volume'].values[0]
         
        #area
        S = csv.loc[csv['Image File'] == file_name, 'Area'].values[0]
        
        #mesh bounding box volume
        Vbb = mesh.bounding_box.volume

        #diameter
        A = np.array(mesh.vertices)
        D = pdist(A)
        #D = squareform(D)
        diam = np.nanmax(D)

        #compactness
        c = (S**3) / (36*m.pi*(V**2))
        
        #sphericity
        sph = 1/c
        
        #eccentricity
        cov_m, eig_vals, eig_vecs = coveigen(mesh)
        ecc = max(eig_vals)/min(eig_vals)
        
        #rectangularity
        rect = V/Vbb
        
        #hull_descriptor
        hull_area = mesh.convex_hull.area
  
        hull_volume = mesh.convex_hull.volume

        hull_v_s_ratio = hull_volume/hull_area
        
        hull_num_of_facets = len(mesh.convex_hull.facets)
        
        hull_comp = (hull_area**3) / (36*m.pi*(hull_volume**2))
        
        
        d.append({'Mesh': file_name, 'Class': class_name, 'Area': S, 'Volume': V, 
                  'Compactness': c,'Diameter': diam, 
                    'Sphericity': sph, 'Eccentricity': ecc, 'Rectangularity': rect,
                    'Convex Hull area': hull_area, 'Convex Hull volume': hull_volume, 
                    'Convex Hull V/S ratio': hull_v_s_ratio, 'Hull Facets num': hull_num_of_facets,
                    'Convex Hull compactness': hull_comp})
        
    df = pd.DataFrame(d)
    # r_df = pd.concat([df.iloc[:, 0:2], scaled_df], axis=1)
    # r_df.rename(columns={0: 'Area', 1: 'Volume', 2: 'Compactness', 3: 'Diameter',
    #                      4: 'Sphericity', 5: 'Eccentricity', 6: 'Rectangularity', 
    #                      7: 'Convex Hull area', 8: 'Convex Hull volume', 9: 'Convex Hull V/S ratio',
    #                      10: 'Hull Facets num', 11: 'Convex Hull compactness'}, inplace=True)
    
    name = 'global_features(non_norm).csv'
    p = Path(out_dir)
    df.to_csv(Path(p, name), index = False)
    print("The csv is created successfully.")


#extracting the standardized global features of meshes in a directory and exporting them to csv
def global_features(in_dir, out_dir):
    csv = pd.read_csv(target_dir + '/Ready_outputs/3DImageInfo_before.csv')
    d = []
    
    for filename in os.listdir(in_dir):
        current_dir = in_dir + '/' + filename        
        split_string = filename.split("_")
        class_name = split_string[0] 
        file_name = split_string[1] 
        mesh = tm.load(current_dir) 
        
        #volume
        V = csv.loc[csv['Image File'] == file_name, 'Volume'].values[0]
         
        #area
        S = csv.loc[csv['Image File'] == file_name, 'Area'].values[0]
        
        #mesh bounding box volume
        Vbb = mesh.bounding_box.volume

        #diameter
        A = np.array(mesh.vertices)
        D = pdist(A)
        #D = squareform(D)
        diam = np.nanmax(D)

        #compactness
        c = (S**3) / (36*m.pi*(V**2))
        
        #sphericity
        sph = 1/c
        
        #eccentricity
        cov_m, eig_vals, eig_vecs = coveigen(mesh)
        ecc = max(eig_vals)/min(eig_vals)
        
        #rectangularity
        rect = V/Vbb
        
        #hull_descriptor
        hull_area = mesh.convex_hull.area
  
        hull_volume = mesh.convex_hull.volume

        hull_v_s_ratio = hull_volume/hull_area
        
        hull_num_of_facets = len(mesh.convex_hull.facets)
        
        hull_comp = (hull_area**3) / (36*m.pi*(hull_volume**2))
        
        
        d.append({'Mesh': file_name, 'Class': class_name, 'Area': S, 'Volume': V, 
                  'Compactness': c,'Diameter': diam, 
                    'Sphericity': sph, 'Eccentricity': ecc, 'Rectangularity': rect,
                    'Convex Hull area': hull_area, 'Convex Hull volume': hull_volume, 
                    'Convex Hull V/S ratio': hull_v_s_ratio, 'Hull Facets num': hull_num_of_facets,
                    'Convex Hull compactness': hull_comp})
        
    df = pd.DataFrame(d)
    scaler = StandardScaler()
    scaled_df = pd.DataFrame(scaler.fit_transform(df.iloc[:, 2:14]))
    r_df = pd.concat([df.iloc[:, 0:2], scaled_df], axis=1)
    r_df.rename(columns={0: 'Area', 1: 'Volume', 2: 'Compactness', 3: 'Diameter',
                         4: 'Sphericity', 5: 'Eccentricity', 6: 'Rectangularity', 
                         7: 'Convex Hull area', 8: 'Convex Hull volume', 9: 'Convex Hull V/S ratio',
                         10: 'Hull Facets num', 11: 'Convex Hull compactness'}, inplace=True)
    
    name = 'global_features.csv'
    p = Path(out_dir)
    r_df.to_csv(Path(p, name), index = False)
    print("The csv is created successfully.")


#calculating the global features of a single mesh (for GUI)
def mesh_globals(mesh):
    d = []
    org_features = pd.read_csv(target_dir + '/Ready_outputs/global_features(non_norm).csv')
    
    #volume
    V = mesh.volume
     
    #area
    S = mesh.area
    
    #mesh bounding box volume
    Vbb = mesh.bounding_box.volume

    #diameter
    A = np.array(mesh.vertices)
    D = pdist(A)
    #D = squareform(D)
    diam = np.nanmax(D)

    #compactness
    c = (S**3) / (36*m.pi*(V**2))
    
    #sphericity
    sph = 1/c
    
    #eccentricity
    cov_m, eig_vals, eig_vecs = coveigen(mesh)
    ecc = max(eig_vals)/min(eig_vals)
    
    #rectangularity
    rect = V/Vbb
    
    #hull_descriptor
    hull_area = mesh.convex_hull.area
  
    hull_volume = mesh.convex_hull.volume

    hull_v_s_ratio = hull_volume/hull_area
    
    hull_num_of_facets = len(mesh.convex_hull.facets)
    
    hull_comp = (hull_area**3) / (36*m.pi*(hull_volume**2))
    
    
    d.append({'Area': S, 'Volume': V, 'Compactness': c,'Diameter': diam, 
              'Sphericity': sph, 'Eccentricity': ecc, 'Rectangularity': rect,
              'Convex Hull area': hull_area, 'Convex Hull volume': hull_volume, 
              'Convex Hull V/S ratio': hull_v_s_ratio, 'Hull Facets num': hull_num_of_facets,
              'Convex Hull compactness': hull_comp}) 
    df = pd.DataFrame(d)
    
    count = 0
    #area
    if df.iloc[0,0] < min(org_features.iloc[1:,2]) or df.iloc[0,0] > max(org_features.iloc[1:,2]):
        count+=1
    #vol
    if df.iloc[0,1] < min(org_features.iloc[1:,3]) or df.iloc[0,1] > max(org_features.iloc[1:,3]):
        count+=1
    #comp
    if df.iloc[0,2] < min(org_features.iloc[1:,4]) or df.iloc[0,2] > max(org_features.iloc[1:,4]):
        count+=1
    #diam
    if df.iloc[0,3] < min(org_features.iloc[1:,5]) or df.iloc[0,3] > max(org_features.iloc[1:,5]):
        count+=1
    #sph  
    if df.iloc[0,4] < min(org_features.iloc[1:,6]) or df.iloc[0,4] > max(org_features.iloc[1:,6]):
        count+=1
    #ecc
    if df.iloc[0,5] < min(org_features.iloc[1:,7]) or df.iloc[0,5] > max(org_features.iloc[1:,7]):
        count+=1
    #rect  
    if df.iloc[0,6] < min(org_features.iloc[1:,8]) or df.iloc[0,6] > max(org_features.iloc[1:,8]):
        count+=1
    #h_a
    if df.iloc[0,7] < min(org_features.iloc[1:,9]) or df.iloc[0,7] > max(org_features.iloc[1:,9]):
        count+=1
    #h_v
    if df.iloc[0,8] < min(org_features.iloc[1:,10]) or df.iloc[0,8] > max(org_features.iloc[1:,10]):
        count+=1
    #h_vs_ratio
    if df.iloc[0,9] < min(org_features.iloc[1:,11]) or df.iloc[0,9] > max(org_features.iloc[1:,11]):
        count+=1
    #num_facet
    if df.iloc[0,10] < min(org_features.iloc[1:,12]) or df.iloc[0,10] > max(org_features.iloc[1:,12]):
        count+=1
    #h_comp
    if df.iloc[0,11] < min(org_features.iloc[1:,13]) or df.iloc[0,11] > max(org_features.iloc[1:,13]):
        count+=1
    if count >= 1:
        warn = 'At least 1 feature of the mesh you uploaded is out of database bounds. There may not be logical results.'
    else:
        warn = ''

    x = org_features.iloc[:,2:].values
    scaler = StandardScaler().fit(x)
    scaled = scaler.transform(df)
    df_scaled = pd.DataFrame(scaled)
    
    df_scaled.rename(columns={0: 'Area', 1: 'Volume', 2: 'Compactness', 3: 'Diameter',
                         4: 'Sphericity', 5: 'Eccentricity', 6: 'Rectangularity', 
                         7: 'Convex Hull area', 8: 'Convex Hull volume', 9: 'Convex Hull V/S ratio',
                         10: 'Hull Facets num', 11: 'Convex Hull compactness'}, inplace=True)
    
    
    return df_scaled, warn
    

#LOCAL DESCRIPTORS
#the number of random sampled items
norm_scale = 300.000
#custom written uniqueness check function to work around python's hashing errors
def contains(source, item):
    for i in source:
        if len(i) == len(item):
            result = True
            for x in range(len(i)):
                if item[x] != i[x]:
                    result = False
                    break
            
            if result == True:
                return True
    return False

#A3 Feature
def a3(mesh):

    setx = []
    for vertex in mesh.vertices:
        if not contains(setx, vertex):
            setx.append(vertex)
        
    angle_list = list()    
    for i in range(int(norm_scale)):
        rand_vers = random.sample(setx, 3)  
        v1 = rand_vers[1] - rand_vers[0]
        v2 = rand_vers[2] - rand_vers[0]   
        angle = tm.transformations.angle_between_vectors(v1,v2)   
        angle_list.append(angle)
    
    angle_list = np.asarray(angle_list)
    return angle_list


#D1 Feature
def d1(mesh):

    dist_list = list()
    b_center = mesh.centroid
    
    for i in range(int(norm_scale)):
        
        rand_vers = random.choice(mesh.vertices)
        
        squared_dist = np.sum((rand_vers - b_center)**2, axis=0)
        dist = np.sqrt(squared_dist)
        dist_list.append(dist)
    
    dist_list = np.asarray(dist_list)
    return dist_list


#D2 Feature
def d2(mesh):

    setx = []
    for vertex in mesh.vertices:
        if not contains(setx, vertex):
            setx.append(vertex)
        
    dist_list = list() 
    for i in range(int(norm_scale)):
       
        rand_vers = random.sample(setx, 2)     
        squared_dist = np.sum((rand_vers[0] - rand_vers[1])**2, axis=0)
        dist = np.sqrt(squared_dist)      
        dist_list.append(dist)
   
    dist_list = np.asarray(dist_list)
    return dist_list


def edgelength(vect1, vect2):
    import math
    x1 = vect1[0]
    y1 = vect1[1]
    z1 = vect1[2]
    x2 = vect2[0]
    y2 = vect2[1]
    z2 = vect2[2]
    dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
    return dist


#D3 Feature
def d3(mesh): 
    
    setx = []
    for vertex in mesh.vertices:
        if not contains(setx, vertex):
            setx.append(vertex)  
            
    area_list = list()
    for i in range(int(norm_scale)):
         
        rand_vers = random.sample(setx, 3)
        
        vect1 = edgelength(rand_vers[1], rand_vers[0])
        vect2 = edgelength(rand_vers[2], rand_vers[0])
        
        v1 = rand_vers[1] - rand_vers[0]
        v2 = rand_vers[2] - rand_vers[0]
        
        # v3 = rand_vers[0] - rand_vers[1]
        # v4 = rand_vers[2] - rand_vers[1]
        
        # v5 = rand_vers[0] - rand_vers[2]
        # v6 = rand_vers[1] - rand_vers[2]
   
        angle = tm.transformations.angle_between_vectors(v1,v2)
        # angle2 = tm.transformations.angle_between_vectors(v3,v4)
        # angle3 = tm.transformations.angle_between_vectors(v5,v6)
        
        area = math.sqrt((np.dot(vect1,vect2) * math.sin(angle))/2)
        
        #tot_angles = angle+ angle2 + angle3
        area_list.append(area)
    
    area_list = np.asarray(area_list)
    return area_list 


#D4 Feature
def d4(mesh): 

    setx = []
    for vertex in mesh.vertices:
        if not contains(setx, vertex):
            setx.append(vertex)  
    
    volume_list = list()
    
    for i in range(int(norm_scale)):
        vol = 0 
        rand_vers = random.sample(setx, 3)
        origin = mesh.centroid
        firstvex = rand_vers[0] - origin
        secondvex = rand_vers[1] - origin
        thirdvex = rand_vers[2] - origin 
           
        vol = math.pow(abs(np.dot(np.cross(firstvex, secondvex),thirdvex))/6, 1/3)
        
        volume_list.append(vol)
    volume_list = np.asarray(volume_list)
    return volume_list



#for a3 bins
def angle_bin(angles):
    b1,b2,b3,b4,b5,b6,b7,b8,b9,b10 = 0,0,0,0,0,0,0,0,0,0

    binlist = list()
    normalized_binlist = list()
    max_range = 3.141592653589793
    bin_width = max_range/10
    for value in angles:   
    
        if value >= 0 and value < bin_width:
            b1 += 1
        elif value >= bin_width and value < bin_width*2:
            b2 += 1
        elif value >= bin_width*2 and value < bin_width*3:
            b3 += 1
        elif value >= bin_width*3 and value < bin_width*4:
            b4 += 1
        elif value >= bin_width*4 and value < bin_width*5:
            b5 += 1
        elif value >= bin_width*5 and value < bin_width*6:
            b6 += 1
        elif value >= bin_width*5 and value < bin_width*7:
            b7 += 1
        elif value >= bin_width*7 and value < bin_width*8:
            b8 += 1
        elif value >= bin_width*8 and value < bin_width*9:
            b9 += 1
        elif value >= bin_width*9 and value <= max_range:
            b10 += 1
        else:
            pass
    
    binlist.extend([b1,b2,b3,b4,b5,b6,b7,b8,b9,b10])
    #bin normalization
    for element in binlist:
        new = element/norm_scale
        normalized_binlist.append(new)
    return normalized_binlist


#for d1 bins
def bin_centroid_dist(distances):
    b1,b2,b3,b4,b5,b6,b7,b8,b9,b10 = 0,0,0,0,0,0,0,0,0,0
    
    binlist = list()
    normalized_binlist = list()
    
    for value in distances:   
    
        if value >= 0 and value < 0.1:
            b1 += 1
        elif value >= 0.1 and value < 0.2:
            b2 += 1
        elif value >= 0.2 and value < 0.3:
            b3 += 1
        elif value >= 0.3 and value < 0.4:
            b4 += 1
        elif value >= 0.4 and value < 0.5:
            b5 += 1
        elif value >= 0.5 and value < 0.6:
            b6 += 1
        elif value >= 0.6 and value < 0.7:
            b7 += 1
        elif value >= 0.7 and value < 0.8:
            b8 += 1
        elif value >= 0.8 and value < 0.9:
            b9 += 1
        elif value >= 0.9 and value <= 1.0:
            b10 += 1
        else:
            pass
    
    binlist.extend([b1,b2,b3,b4,b5,b6,b7,b8,b9,b10])
    for element in binlist:
        new = element/norm_scale
        normalized_binlist.append(new)     
    return normalized_binlist


#for d2 bins
#EN BUYUK UZUNLUK KOK 2 OLMALI = 1.41421356
def bin_dist(distances):
    b1,b2,b3,b4,b5,b6,b7,b8,b9,b10 = 0,0,0,0,0,0,0,0,0,0
    
    binlist = []
    normalized_binlist = []
    max_dist = 1.41421356
    dist_int = max_dist/10
    
    for value in distances:   
    
        if value >= 0 and value < dist_int:
            b1 += 1
        elif value >= dist_int   and value < dist_int*2:
            b2 += 1
        elif value >= dist_int *2 and value < dist_int*3:
            b3 += 1
        elif value >= dist_int *3 and value < dist_int*4:
            b4 += 1
        elif value >= dist_int*4 and value < dist_int*5:
            b5 += 1
        elif value >= dist_int*5 and value < dist_int*6:
            b6 += 1
        elif value >= dist_int*6 and value < dist_int*7:
            b7 += 1
        elif value >= dist_int*7 and value < dist_int*8:
            b8 += 1
        elif value >= dist_int*8 and value < dist_int*9:
            b9 += 1
        elif value >= dist_int*9 and value <= dist_int*10:
            b10 += 1
        else:
            pass
    
    binlist.extend([b1,b2,b3,b4,b5,b6,b7,b8,b9,b10])
    for element in binlist:
        new = element/norm_scale
        normalized_binlist.append(new)     
    return normalized_binlist



#for d3 bins
def area_bin(area_dist):
  #0-0.6 face area range   
     #change it up to 4.5 !
    max_area = 0.8
    area_int = max_area/10
    b1,b2,b3,b4,b5,b6,b7,b8,b9,b10 = 0,0,0,0,0,0,0,0,0,0
    binlist = []
    normalized_binlist = []
    
    for value in area_dist:    
         if value >= 0 and value < area_int:
             b1 += 1
         elif value >= area_int   and value < area_int*2:
             b2 += 1
         elif value >= area_int *2 and value < area_int*3:
             b3 += 1
         elif value >= area_int *3 and value < area_int*4:
             b4 += 1
         elif value >= area_int*4 and value < area_int*5:
             b5 += 1
         elif value >= area_int*5 and value < area_int*6:
             b6 += 1
         elif value >= area_int*6 and value < area_int*7:
             b7 += 1
         elif value >= area_int*7 and value < area_int*8:
             b8 += 1
         elif value >= area_int*8 and value < area_int*9:
             b9 += 1
         elif value >= area_int*9 and value <= area_int*10:
             b10 += 1
         else:
             pass    
    binlist.extend([b1,b2,b3,b4,b5,b6,b7,b8,b9,b10])
    for element in binlist:
        new = element/norm_scale
        normalized_binlist.append(new)     
    return normalized_binlist

#bin max is updated to 0.5 from 0.6!! (for the report)
#for d4 bins
def vol_bin(distances):
    max_vol = 0.5
    vol_int = max_vol/10
    b1,b2,b3,b4,b5,b6,b7,b8,b9,b10 = 0,0,0,0,0,0,0,0,0,0
    binlist = []
    normalized_binlist = []
    
    for value in distances:   
    
        if value >= 0 and value < vol_int:
            b1 += 1
        elif value >= vol_int  and value < vol_int*2:
            b2 += 1
        elif value >= vol_int*2 and value < vol_int*3:
            b3 += 1
        elif value >= vol_int*3 and value < vol_int*4:
            b4 += 1
        elif value >= vol_int*4 and value < vol_int*5:
            b5 += 1
        elif value >= vol_int*5 and value < vol_int*6:
            b6 += 1
        elif value >= vol_int*6 and value < vol_int*7:
            b7 += 1
        elif value >=vol_int*7 and value < vol_int*8:
            b8 += 1
        elif value >= vol_int*8 and value < vol_int*9:
            b9 += 1
        elif value >= vol_int*9 and value <= vol_int*10:
            b10 += 1
        else:
            pass
        
    binlist.extend([b1,b2,b3,b4,b5,b6,b7,b8,b9,b10])
    for element in binlist:
        new = element/norm_scale
        normalized_binlist.append(new)     
    return normalized_binlist 



def line_graph(bin1,bin2):
    plt.style.use('seaborn-whitegrid')
    x = np.linspace(0, 1, 10)
    label1 = str(bin1)
    plt.xlabel(label1)
    plt.plot(x, bin1)
    plt.plot(x, bin2)


#calculating the local features of all the meshes in the shape databse
def local_extract(input_dir, output_dir): 

    d = []
    for filename in os.listdir(input_dir):
        current_dir = input_dir + '/' + filename        
        split_string = filename.split("_")
        class_name = split_string[0] 
        file_name = split_string[1] 
        mesh = tm.load(current_dir)
        
        d1_bins = d1(mesh)
        cent_dis = bin_centroid_dist(d1_bins)
        print("d1 done")
        a3_bins = a3(mesh)
        angles = angle_bin(a3_bins)
        print("a3 done")
        d2_bins = d2(mesh)
        dist_two = bin_dist(d2_bins)
        print("d2 done")
        d3_bins = d3(mesh)
        area = area_bin(d3_bins)
        print("d3 done")
        d4_bins = d4(mesh)
        volume = vol_bin(d4_bins)
        print("d4 done")
        d.append({"Mesh name": file_name, "Class name": class_name, "a3_bin1": angles[0],
                  "a3_bin2": angles[1], "a3_bin3": angles[2], "a3_bin4": angles[3],
                  "a3_bin5": angles[4], "a3_bin6": angles[5], "a3_bin7": angles[6],
                 "a3_bin8": angles[7], "a3_bin9": angles[8], "a3_bin10": angles[9],
                  "d1_bin1": cent_dis[0], "d1_bin2": cent_dis[1], "d1_bin3": cent_dis[2], 
                  "d1_bin4": cent_dis[3],
                  "d1_bin5": cent_dis[4], "d1_bin6": cent_dis[5], "d1_bin7": cent_dis[6],
                 "d1_bin8": cent_dis[7], "d1_bin9": cent_dis[8], "d1_bin10": cent_dis[9],
                 "d2_bin1": dist_two[0], "d2_bin2": dist_two[1], "d2_bin3": dist_two[2], 
                 "d2_bin4": dist_two[3], "d2_bin5": dist_two[4], "d2_bin6": dist_two[5], 
                 "d2_bin7": dist_two[6], "d2_bin8": dist_two[7], "d2_bin9": dist_two[8], 
                 "d2_bin10": dist_two[9],  "d3_bin1":area[0], "d3_bin2": area[1], 
                 "d3_bin3": area[2], 
                 "d3_bin4": area[3], "d3_bin5": area[4], "d3_bin6": area[5], 
                 "d3_bin7": area[6], "d3_bin8": area[7], "d3_bin9": area[8], 
                 "d3_bin10": area[9], "d4_bin1":volume[0], "d4_bin2": volume[1], 
                 "d4_bin3": volume[2], 
                 "d4_bin4": volume[3], "d4_bin5": volume[4], "d4_bin6": volume[5], 
                 "d4_bin7": volume[6], "d4_bin8": volume[7], "d4_bin9": volume[8], 
                 "d4_bin10": volume[9]
                 })
       
    name = 'local_features.csv'
    p = Path(output_dir)
    df = pd.DataFrame(d)
    df.to_csv(Path(p, name), index = False)
    print("csv is created.")
    
    
'''a concatenated csv function which will contain global feat., local feat. 
and aab measures'''
def csv_merge(csv1, csv2, output_dir):
    csv1 = pd.read_csv(csv1)
    csv2 = pd.read_csv(csv2)
    merged_df = pd.concat([csv1, csv2.iloc[:, 2:]], axis=1)
    merged_df.to_csv(Path(output_dir, "all_features.csv"), index = False)
    


#calculating the local features of a single mesh (for GUI)
def mesh_locals(mesh):
    d = []
    d1_bins = d1(mesh)
    cent_dis = bin_centroid_dist(d1_bins)

    a3_bins = a3(mesh)
    angles = angle_bin(a3_bins)

    d2_bins = d2(mesh)
    dist_two = bin_dist(d2_bins)

    d3_bins = d3(mesh)
    area = area_bin(d3_bins)

    d4_bins = d4(mesh)
    volume = vol_bin(d4_bins)

    d.append({"a3_bin1": angles[0],
              "a3_bin2": angles[1], "a3_bin3": angles[2], "a3_bin4": angles[3],
              "a3_bin5": angles[4], "a3_bin6": angles[5], "a3_bin7": angles[6],
             "a3_bin8": angles[7], "a3_bin9": angles[8], "a3_bin10": angles[9],
              "d1_bin1": cent_dis[0], "d1_bin2": cent_dis[1], "d1_bin3": cent_dis[2], 
              "d1_bin4": cent_dis[3],
              "d1_bin5": cent_dis[4], "d1_bin6": cent_dis[5], "d1_bin7": cent_dis[6],
             "d1_bin8": cent_dis[7], "d1_bin9": cent_dis[8], "d1_bin10": cent_dis[9],
             "d2_bin1": dist_two[0], "d2_bin2": dist_two[1], "d2_bin3": dist_two[2], 
             "d2_bin4": dist_two[3], "d2_bin5": dist_two[4], "d2_bin6": dist_two[5], 
             "d2_bin7": dist_two[6], "d2_bin8": dist_two[7], "d2_bin9": dist_two[8], 
             "d2_bin10": dist_two[9],  "d3_bin1":area[0], "d3_bin2": area[1], 
             "d3_bin3": area[2], 
             "d3_bin4": area[3], "d3_bin5": area[4], "d3_bin6": area[5], 
             "d3_bin7": area[6], "d3_bin8": area[7], "d3_bin9": area[8], 
             "d3_bin10": area[9], "d4_bin1":volume[0], "d4_bin2": volume[1], 
             "d4_bin3": volume[2], 
             "d4_bin4": volume[3], "d4_bin5": volume[4], "d4_bin6": volume[5], 
             "d4_bin7": volume[6], "d4_bin8": volume[7], "d4_bin9": volume[8], 
             "d4_bin10": volume[9]
             })
    df = pd.DataFrame(d)
    return df


#merging local and global features of a single mesh (for GUI)
def mesh_features_merge(df1, df2):
    merged_df = pd.concat([df1, df2], axis=1)
    return merged_df
