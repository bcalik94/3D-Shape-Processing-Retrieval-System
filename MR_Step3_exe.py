# -*- coding: utf-8 -*-


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

#STEP 3 FEATURE EXTRACTION EXE FILE

csv1 = global_features(target_dir + '/Ready_outputs/Normalized_OFFiles',target_dir + '/New_outputs')

csv2 = local_extract(target_dir + '/Ready_outputs/Normalized_OFFiles', target_dir + '/New_outputs')

csv_merge('csv1','csv2',target_dir + '/New_outputs')
