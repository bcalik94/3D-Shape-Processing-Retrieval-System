# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from MR_Step3 import *
from sklearn.metrics import *
from MR_Step4_distance_calculation import *
from matplotlib import pyplot as plt
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


def quality_metrics():
    
    df = pd.read_csv(target_dir + '/Ready_outputs/all_features.csv')
   
    accuracies = []
    sensitivities = []
    specificities = []
    precisions = []
    res_df = pd.DataFrame(columns = ['Query length', 'Class', 'Accuracy', 'Specificity', 
                                     'Sensitivity', 'Precision'])
    grand_df = pd.DataFrame(columns = ['Query length', 'Accuracy', 'Specificity', 
                                     'Sensitivity', 'Precision'])
    
    d = []
    retrievals = []
    
#1 - get all the query results for each shape in the DB (Q size 20)
#query length = j, class size = cs, counter for the shape base size = i
    cs = 19
    for j in range(1,20):
        collect_df = pd.DataFrame(columns = ['Query length', 'Class', 'Accuracy', 'Specificity', 
                                     'Sensitivity', 'Precision'])
        print(j)
        for i in range(len(df)):
            s_class = df.iloc[i,1]
            print(s_class)
            # print(i)
            res = avg_dist(df.iloc[i,0]).iloc[0:j,1]
            
            counter = 0
            for k in res:
                if k == s_class:
                    counter +=1
                    # print(k, "is in result")
            
            tp = counter
            print("tp:", tp)
            fp = j - tp
            print("fp:", fp)
            fn = cs - tp
            print("fn:", fn)
            tn = 380 - cs - fp
            print("tn:", tn)
        
    #2 - calculate its accuracy, sensitivity and specificity for each shape
            accuracy = (tp + tn)/380
            specificity = tn/(tn + fp)
            sensitivity = tp/(tp + fn)
            precision = tp/(tp + fp)
            #print("acc:", accuracy, "spec:", specificity, "sens:", sensitivity, "prec:", precision)
            
    #3 - add these results into an object which will become class-avg later
            accuracies.append(accuracy)
            specificities.append(specificity)
            sensitivities.append(sensitivity)       
            precisions.append(precision)    
        
    #4 - average these results for the given class, proceed to the next class        
            if i < 379:
                if (df.iloc[i,1] == df.iloc[i+1, 1]):
                    continue           
                else:
                    accr = sum(accuracies)/len(accuracies)
                    spec = sum(specificities)/len(specificities)
                    sens = sum(sensitivities)/len(sensitivities)
                    prec = sum(precisions)/len(precisions)
                    d.append({"Query length": j, "Class": s_class, "Accuracy": accr, 
                              "Specificity": spec, "Sensitivity": sens,
                              "Precision": prec})
                    dummy_df = pd.DataFrame(d)
                    collect_df = collect_df.append(dummy_df)
                    res_df = res_df.append(dummy_df)
                    
                    d = []
                    accuracies = []
                    sensitivities = []
                    specificities = []
                    precisions = []
                    del(dummy_df)
                    
            else:
                accr = sum(accuracies)/len(accuracies)
                spec = sum(specificities)/len(specificities)
                sens = sum(sensitivities)/len(sensitivities)
                d.append({"Query length": j,"Class": s_class, "Accuracy": accr, 
                          "Specificity": spec, "Sensitivity": sens,
                          "Precision": prec})
                dummy_df = pd.DataFrame(d)
                collect_df = collect_df.append(dummy_df)
                res_df =  res_df.append(dummy_df)
                

               
    #5 - Average each quality metrics to obtain a grand avg for the whole system
                d2 = []
                d2.append({"Query length": j, 
                          "Accuracy": collect_df["Accuracy"].mean(axis = 0), 
                          "Specificity": collect_df["Specificity"].mean(axis = 0), 
                          "Sensitivity": collect_df["Sensitivity"].mean(axis = 0),
                          "Precision": collect_df["Precision"].mean(axis = 0)})
                dummy_df2 = pd.DataFrame(d2)
                grand_df =  grand_df.append(dummy_df2)
                d = []
                accuracies = []
                sensitivities = []
                specificities = []
                precisions = []
                del(dummy_df)
                d2 = []
                del(collect_df)
        
        p = Path(target_dir + '/New_outputs')
        res_df.to_csv(Path(p, "Class Quality metrics.csv"), index = False)
        grand_df.to_csv(Path(p, "Grand Quality metrics.csv"), index = False)

    return res_df, grand_df

class_metrics, total_metrics  = quality_metrics()

#6 - Draw a ROC (using TPR, FPR & threshold vals.) and calculate the AUC score 
# tpr = total_metrics.iloc[:,3]
# fpr = 1 - total_metrics.iloc[:,2]


# # plt.figure()
# lw = 2
# plt.plot(fpr, tpr, color='darkorange', lw=lw,
#           label='ROC curve (area = %0.2f)' % roc_auc)
# plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
# plt.xlim([0.0, 1.0])
# plt.ylim([0.0, 1.0])
# plt.xlabel('False Positive Rate')
# plt.ylabel('True Positive Rate')
# plt.title('ROC Curve of the Shape Retrieval System')
# plt.legend(loc="lower right")
# plt.show()
