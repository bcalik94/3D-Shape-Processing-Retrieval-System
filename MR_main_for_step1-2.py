# -*- coding: utf-8 -*-

from MR_Step2 import *
from MR_Step3 import *
import trimesh as tm
import pyrender as pr
import pandas as pd
import earthpy as et 

home_dict = et.io.HOME
desktop = os.path.join(et.io.HOME, 'Desktop')
target_dir = os.path.join(desktop, 'MR_Project')

#the main program
while True:
    c1 = input("Would you like to  your own 3D image or render from the database?(upload/render):")
    if c1 == "upload":
        inp = input("please enter the absolute directory path of the mesh with '/' :")
        directory = inp
        loaded_trimesh = tm.load(directory)
        mesh = pr.Mesh.from_trimesh(loaded_trimesh, smooth = True)
        
        #calcation of preprocessing, normalization & feature extraction
        print(f"The properties of this 3D image is: {loaded_trimesh.vertices.shape[0]} vertices, {loaded_trimesh.faces.shape[0]} faces, ")
        print(f"area is {loaded_trimesh.area}, volume is {loaded_trimesh.volume}, ")
        print(f"average area per face is {loaded_trimesh.area/loaded_trimesh.faces.shape[0]}, and ")
        print(f"Length of AABB: {loaded_trimesh.extents[0]}, Width of AABB: {loaded_trimesh.extents[1]},Height of AABB: {loaded_trimesh.extents[2]}.")
        upload_mesh(mesh)
        
        #msimilarity function & results
        #render_mesh(mesh)
        
        ans = input("would you like to continue to another image?(y/n):")
        if ans == "y":
            continue
        else:
            break
        
    elif c1 == "render": 
        #instead of getting input, change it to final features csv
        csv = target_dir + '/Ready_outputs/Normalized_Meshes_Info.csv'
        df = pd.read_csv(csv)
        print("Some information about the mesh database:")
        mesh_stats = mesh_info(df)
        
        #instead, ask for the file name that they are interested
        c2 = target_dir + '/Ready_outputs/Normalized_OFFiles'
        meshes = mesh_import(c2)     
        
        
        choice = input(f"There are {len(meshes[0])} 3D images in the directory. Which 3D shape would you like to visualize?(Please specify an index number.):")
        print(f"The properties of this 3D image is: {df.loc[int(choice)]}")
        
        chosen_mesh = meshes[1][int(choice)]
        
        render_mesh(chosen_mesh)
    
        ans = input("would you like to continue to another image?(y/n):")
        if ans == "y":
            continue
        else:
            break
    
    else:
        print("Not recognized answer. Please try again.")
