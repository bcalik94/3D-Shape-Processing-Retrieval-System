# -*- coding: utf-8 -*-

from tkinter import *
import tkinter as tk
from MR_Step2 import *
from MR_Step3 import *
from mesh_widget import *
from MR_Step4_distance_calculation import *
from mesh_upload_distances_for_gui import *
from tkinter import filedialog
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


#main gui 
root = Tk()
root.title("3D Mesh Search")
root.geometry('300x500')
lbl = Message(root, text = "Would you like to choose mesh from the library or upload your own mesh?",
              width=300)
lbl.pack()

def render_wind():
    global lbl1, lbl2, lbl3, calc, stats, shapeviz, compare
    # top = Toplevel()
    # top.title("Mesh Rendering")
    # top.geometry('500x300')
    # lbl = Label(top, text="Please choose the mesh from the database:").pack()
    
    root.filename = filedialog.askopenfilename(initialdir=target_dir + '/Ready_outputs/Normalized_OFFiles',
                                          title="select an OFF file",
                                          filetypes=(("off files", "*.off"), ("all files", "*.*")))
    
    filename = os.path.basename(root.filename)
    class_name = filename.split("_")[0]
    mesh_name = filename.split("_")[1]
    lbl1 = Label(root, text="Chosen mesh:")
    lbl1.pack()
    lbl2 = Label(root, text=mesh_name+', '+class_name+ " class")  
    lbl2.pack()
    
    mesh = tm.load(root.filename)
    meshu = pr.Mesh.from_trimesh(mesh)   
    scene = pr.Scene(ambient_light=True)
    scene.add(meshu)
    pr.Viewer(scene, use_raymond_lighting=True)
    
    def distances():
        global stats, lbl3, distance_l, shapeviz, compare

        distance_l = avg_dist(mesh_name)
        result = distance_l.iloc[0:10,[0,1,8]].to_string(index=False)
        lbl3 = Label(root, text="The most similar meshes found: ")
        lbl3.pack()
        stats = Message(root, text = result)
        stats.pack() 
        
        def createNewWindow1():
        #newWindow.title("Query Shape and Retrieved Similar Shapes") 
            q_mesh = tm.load(target_dir + '/Ready_outputs/Normalized_OFFiles/'+ class_name + '_'+ mesh_name)
            mesh_1 = tm.load(target_dir + '/Ready_outputs/Normalized_OFFiles/'+ distance_l.iloc[0,1] + '_'+ distance_l.iloc[0,0])
            mesh_2 = tm.load(target_dir + '/Ready_outputs/Normalized_OFFiles/'+ distance_l.iloc[1,1] + '_'+ distance_l.iloc[1,0])
            mesh_3 = tm.load(target_dir + '/Ready_outputs/Normalized_OFFiles/'+ distance_l.iloc[2,1] + '_'+ distance_l.iloc[2,0])
            mesh_4 = tm.load(target_dir + '/Ready_outputs/Normalized_OFFiles/'+ distance_l.iloc[3,1] + '_'+ distance_l.iloc[3,0])
            mesh_5 = tm.load(target_dir + '/Ready_outputs/Normalized_OFFiles/'+ distance_l.iloc[4,1] + '_'+ distance_l.iloc[4,0])

            main(q_mesh, mesh_1, mesh_2, mesh_3, mesh_4, mesh_5)
            
        shapeviz = Button(root, text="See shapes", command = lambda: createNewWindow1())
        shapeviz.pack()
        
        def seefeatures():
            df = pd.read_csv(target_dir + '/Ready_outputs/all_features.csv')
            base_mesh = df.loc[df['Mesh'] == mesh_name]
            base_mesh = base_mesh.reset_index()
            base_mesh.drop('index', axis='columns', inplace=True)
            
            mesh_1 = df.loc[df['Mesh'] == distance_l.iloc[0,0]]
            mesh_1 = mesh_1.reset_index()
            mesh_1.drop('index', axis='columns', inplace=True)
            
            mesh_2 = df.loc[df['Mesh'] == distance_l.iloc[1,0]]
            mesh_2 = mesh_2.reset_index()
            mesh_2.drop('index', axis='columns', inplace=True)
            
            mesh_3 = df.loc[df['Mesh'] == distance_l.iloc[2,0]]
            mesh_3 = mesh_3.reset_index()
            mesh_3.drop('index', axis='columns', inplace=True)
            
            mesh_4 = df.loc[df['Mesh'] == distance_l.iloc[3,0]]
            mesh_4 = mesh_4.reset_index()
            mesh_4.drop('index', axis='columns', inplace=True)
            
            mesh_5 = df.loc[df['Mesh'] == distance_l.iloc[4,0]]
            mesh_5 = mesh_5.reset_index()
            mesh_5.drop('index', axis='columns', inplace=True)
            
            all_features = pd.concat([base_mesh, mesh_1, mesh_2, mesh_3, mesh_4, mesh_5],
                                     axis=0)
            p = target_dir + '/New_outputs'
            all_features.to_csv(Path(p, 'uploaded_shape_features.csv'))
            
        compare = Button(root, text="export features", command = lambda: seefeatures())
        compare.pack()    
        
    calc = Button(root, height=1, width=10, text="Calculate", 
                command = distances)
    calc.pack()

def upload_wind():
    global lbl1, lbl2, lbl3, calc, stats, shapeviz, compare
    target_dir = os.path.join(desktop, 'MR_Project')
    
    root.filename2 = filedialog.askopenfilename(initialdir= target_dir + '/non-db_meshes_for-gui',
                                          title="select a file",
                                          filetypes=(("off files", "*.off"), 
                                                     ("all files", "*.*")))
    mesh = tm.load(root.filename2)

    filename2 = os.path.basename(root.filename2)
    #will return the path of the preprocessed mesh
    pre_mesh = preprocess(mesh, filename2, root.filename2)
    #will return the normalized mesh itself
    norm_mesh = normalize(pre_mesh)
    
    #feature extraction of the mesh
    glob_f = mesh_globals(norm_mesh)
    
    if glob_f[1] != '':
        message = messagebox.showwarning("Warning", glob_f[1])
    else:
        pass
    local_f = mesh_locals(norm_mesh)
    
    #concatination of the mesh features
    features = mesh_features_merge(glob_f[0], local_f)
    
    filename2 = os.path.basename(root.filename2)
    lbl1 = Label(root, text="Chosen mesh:")
    lbl1.pack()
    lbl2 = Label(root, text=filename2)  
    lbl2.pack()
    

    meshu = pr.Mesh.from_trimesh(norm_mesh)   
    scene = pr.Scene(ambient_light=True)
    scene.add(meshu)
    pr.Viewer(scene, use_raymond_lighting=True)
    
    def distances():
        global stats, lbl3, shapeviz, compare
    
        distances = avg_mesh_dist(features)
        result = distances.iloc[0:10,[0,1,8]].to_string(index=False)
        lbl3 = Label(root, text="The most similar meshes found: ")
        lbl3.pack()
        stats = Message(root, text = result)
        stats.pack()
      
        def createNewWindow2():
            q_mesh = norm_mesh
            mesh_1 = tm.load(target_dir + '/Ready_outputs/Normalized_OFFiles/'+ distances.iloc[0,1] + '_'+ distances.iloc[0,0])
            mesh_2 = tm.load(target_dir + '/Ready_outputs/Normalized_OFFiles/'+ distances.iloc[1,1] + '_'+ distances.iloc[1,0])
            mesh_3 = tm.load(target_dir + '/Ready_outputs/Normalized_OFFiles/'+ distances.iloc[2,1] + '_'+ distances.iloc[2,0])
            mesh_4 = tm.load(target_dir + '/Ready_outputs/Normalized_OFFiles/'+ distances.iloc[3,1] + '_'+ distances.iloc[3,0])
            mesh_5 = tm.load(target_dir + '/Ready_outputs/Normalized_OFFiles/'+ distances.iloc[4,1] + '_'+ distances.iloc[4,0])

            main(q_mesh, mesh_1, mesh_2, mesh_3, mesh_4, mesh_5)
        shapeviz = Button(root, text="See shapes", command = lambda: createNewWindow2())
        shapeviz.pack()
        
        def seefeatures():
            df = pd.read_csv(target_dir + '/Ready_outputs/all_features.csv')
            base_mesh = features
            
            mesh_1 = df.loc[df['Mesh'] == distances.iloc[0,0]]
            mesh_1 = mesh_1.reset_index()
            mesh_1.drop('index', axis='columns', inplace=True)
            
            mesh_2 = df.loc[df['Mesh'] == distances.iloc[1,0]]
            mesh_2 = mesh_2.reset_index()
            mesh_2.drop('index', axis='columns', inplace=True)
            
            mesh_3 = df.loc[df['Mesh'] == distances.iloc[2,0]]
            mesh_3 = mesh_3.reset_index()
            mesh_3.drop('index', axis='columns', inplace=True)
            
            mesh_4 = df.loc[df['Mesh'] == distances.iloc[3,0]]
            mesh_4 = mesh_4.reset_index()
            mesh_4.drop('index', axis='columns', inplace=True)
            
            mesh_5 = df.loc[df['Mesh'] == distances.iloc[4,0]]
            mesh_5 = mesh_5.reset_index()
            mesh_5.drop('index', axis='columns', inplace=True)
            
            all_features = pd.concat([base_mesh, mesh_1, mesh_2, mesh_3, mesh_4, mesh_5],
                                     axis=0)
            p = target_dir + '/New_outputs'
            all_features.to_csv(Path(p, 'uploaded_shape_features.csv'))
            
        compare = Button(root, text="Export features", command = lambda: seefeatures())
        compare.pack()    
    
   
    calc = Button(root, height=1, width=10, text="Calculate", 
                command=distances)
    calc.pack()
    
btn1 = Button(root, text="Choose", command=render_wind)
btn2 = Button(root, text="Upload", command=upload_wind)

    
def clearTextInput():
    lbl1.pack_forget()
    lbl2.pack_forget()
    lbl3.pack_forget()
    stats.pack_forget()
    calc.destroy() 
    shapeviz.destroy()
    compare.destroy()
    
btnDel=tk.Button(root, height=1, width=10, text="Clear", 
                 command=clearTextInput)

btn1.pack()
btn2.pack()
btnDel.pack()

mainloop()
