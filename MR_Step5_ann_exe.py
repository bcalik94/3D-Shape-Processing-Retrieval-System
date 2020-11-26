#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from MR_Step5_ann import *


#the main ann program
while True:
    c1 = input("Would you like to see ANN retrieval results of 3D image  from a directory? (y/n)" )
    if c1 == "y":
        inp = input("please enter off file name (e.g. 61.off):")
        mesh_name = inp
    
        mesh_class, ann_results = ann(mesh_name)
        print("Queried mesh is a shape of ", mesh_class,)
        print(" Results of ANN retrieval ")
        print(ann_results)
        
        #msimilarity function & results
        #render_mesh(mesh)
        
        ans = input("would you like to continue to another image?(y/n):")
        if ans == "y":
            continue
        else:
            break    
