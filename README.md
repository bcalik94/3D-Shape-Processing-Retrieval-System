# 3D_ShapeImageProcessing

First of all, when you open the unzipped file, you will see two folders: '_MACOSX' and 'MR_Project'.PLEASE ignore '_MACOSX' and place the unzipped MR_Project folder on your Desktop. 
Be sure that only the MR_Project folder inside the zip file is on the Desktop. The codes will not run if the path is going to be '...\Desktop\MR_Project\MR_Project\...' 
Unfortunately zipping creates a wrapper folder with the same name on the top of the actual project folder, so you must move the MR_Project folder inside the unzipped folder to the Desktop!!! 
The correct path will be '...\Desktop\MR_Project\py_codes\... .py' for successfull executions. Otherwise directory conflicts will occur while trying to execute the .py files.

In order to run this project, there are several external libraries you should install. 
These libraries can be downloaded with (please execute commands one by one):

NOTE: This project is coded and tested in Spyder, which is one of the interactive Python environments provided by Anaconda

pip install trimesh
pip install open3d
pip install pyrender
pip install numpy
pip install pandas
pip install matplotlib
pip install scipy
pip install scikit-learn
pip install annoy
pip install glooey
pip install pyglet
pip install autoprop
pip install earthpy NOTE: for this library, there is another dependency library (if does not exist in the system already): pip install geopandas 

The other libraries should be built-in in your system with python but be sure that the following libraries also exist:
os.path, pathlib, random, math, time, __future__

------------------------------The Input Database and all Related Folders of the Project------------------------------------------

-The shape database is in the folder "LabeledDB_New" in MR_Project.

-All the files which are the outputs from pre-execution of all steps, some of which are also input files for some parts of the system are added in the "Ready_outputs" folder. 
The system will automatically use these files in wherever and whenever it needs (exp: for GUI execution).

-When you execute any of the steps, the resulting outputs will be written to the "New_outputs" folder, so that the previous calculated files will not get mixed of cause any conflict.

-! ALL of the codes of this project are located in the "py_files" folder.

-----------------------------The Execution of Each Step of the Project----------------------------------------------------------

-To see the execution of Step 1: please run "MR_Step1.py" file

-To see the execution of Step 2: please run "MR_Step2_exe.py" file. It will export several statistics (# of vertices,faces, AABB sizes etc.) in csv files, before and after pre-processing. 
It will also output a new shape database folder, which contains decimated/remeshed off files. Note that it takes approximately an hour to execute this file.

-To see the interactive minimal application built on both step 1&2, please run "MR_main_for_step1-2.py" file. In this minimal app, you can choose a shape from the shape database or upload your own mesh with an absolute path,
visualize the shape you chose in a new window, and after exiting that window, you can see several statistics regarding the database (if you chose render) and the shape itself (if you chose either render or upload).
You can use the shapes in the folder "sample_meshes_for_step1" if you would like to test the upload option in this app.

-To see the execution of step 3: please run "MR_Step3_exe.py" file. You will get 3 csv files as outputs, which contain global features, local features, and a final joined all features csv. 
Note that the execution of this step takes roughly 8 hours.

-To see the execution of step 4: please run "MR_Step4_gui.py" file. It is our graphical user interface which does the distance calculation on-the-fly. If you prefer uploading a shape which does not exist in the shape database,
the non-db shape folder will automatically be shown when you click "upload" button. Then, all features are going to be calculated on-the-fly too, which may take between 20 and 40 seconds.

-To see the execution results of step 5: please run "MR_Step5_ann_exe.py" file to see the ANN results, and run "MR_Step5_bonus_t-sne.py" file to see the t-SNE results with the respective plot.

-Finally to see execution results of step 6: please run "MR_Step6.py" to see the output csv files of evaluation results. One csv contains overall metrics for each query length (Grand Quality metrics.csv),
the other csv contains the results for each class per query length (Class Quality metrics.csv). Note that it takes around 1.5 hours to execute this file.


!- All the other py files in this project (MR_Step2.py, MR_Step3.py, MR_Step4_distance_calculation.py, mesh_upload_distances_for_gui.py, MR_Step5_ann.py, and mesh_widget.py) 
contain only the function definitions which are used in the other files mentioned above. The files "ann_rendering(for report).py" and "MR_Step3_plotting_features.py" are the files used to visualize different results of the project,
which are used in our project report.


