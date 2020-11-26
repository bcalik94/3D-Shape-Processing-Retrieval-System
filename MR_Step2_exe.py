# -*- coding: utf-8 -*-

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

#--------------------------------------------------------------------
#STEP 2 EXECUTION FILE

#collecting the initial statistics of the raw mesh database
mesh_import_export( target_dir + '/LabeledDB_new',  target_dir + '/New_outputs')

#preprocess the meshes (decimation or remeshing)

mesh_preprocess(target_dir + '/LabeledDB_new',  target_dir + '/New_outputs')

#collecting the statistics of the new preprocessed mesh database
csv_extract(target_dir + '/Ready_outputs/Updated_Offiles',
            target_dir + '/New_outputs',
            'Updated_Meshes_Info.csv')

#running the normalization step, accepts the preprocessed meshes
normalization(target_dir + '/New_outputs/Updated_Offiles', target_dir + '/New_outputs')


#collecting the statistics of the normalized mesh database
csv_extract(target_dir + '/Ready_outputs/Normalized_OFFiles',
            target_dir + '/New_outputs',
            'Normalized_Meshes_Info.csv')
