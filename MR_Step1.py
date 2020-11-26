# -*- coding: utf-8 -*-

import trimesh as tm
import pyrender as pr
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

#to open the files from a folder, read them as "mesh" and append them to a list
#m1 and m2 are off, m3 and m4 are ply files
m_1 = tm.load(target_dir + '/LabeledDB_new/Ant/81.off')
m_2 = tm.load(target_dir + '/LabeledDB_new/Airplane/62.off')
m_3 = tm.load(target_dir + '/non-db_meshes_for-gui/sphere.ply')
m_4 = tm.load(target_dir + '/non-db_meshes_for-gui//airplane.ply')

'''The Mesh.from_trimesh() method has a few additional optional parameters. If you want to render the mesh
without interpolating face normals, which can be useful for meshes that are supposed to be angular (e.g. a cube), you
can specify smooth=False.'''

#this 3d visualization can read both binary and ascii ply files!
#if the ofject is a trimesh, then first convert it to acpyrender mesh object
def render_mesh(loaded_trimesh):
    mesh = pr.Mesh.from_trimesh(loaded_trimesh, smooth = True)
    scene_u = pr.Scene(ambient_light=True)
    scene_u.add(mesh)
    pr.Viewer(scene_u, use_raymond_lighting=True)

#visualization using pyrender (they will appear in order as you close one window)
render_mesh(m_1)
render_mesh(m_2)
render_mesh(m_3)
render_mesh(m_4)



    
