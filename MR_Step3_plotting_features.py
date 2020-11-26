# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#multiplotting
'''NOTE: PLEASE RUN THE PLOTS ONE BY ONE'''

#5 df for local features, 6th is an extra for global features
df = pd.read_csv('C:/Users/hatta/Desktop/UU/Courses/Multimedia_Retrieval/step3/all_features.csv')

airplane = df.loc[df['Class'] == 'Airplane']
human = df.loc[df['Class'] == 'Human']
table = df.loc[df['Class'] == 'Table']
plier = df.loc[df['Class'] == 'Plier']
vase = df.loc[df['Class'] == 'Vase']
chair = df.loc[df['Class'] == 'Chair']

#local features multiplot
x = np.linspace(0, 10, 10)
fig, axs = plt.subplots(5, 5, sharex='col', 
                        sharey='row')

#airplane
#a3
aa3 = airplane.iloc[:,14:24].T
axs[0, 0].plot(x, aa3)
axs[0, 0].set_title('Class:Airplane, Feature:A3')
#d1
ad1 = airplane.iloc[:,24:34].T
axs[0, 1].plot(x, ad1)
axs[0, 1].set_title('Class:Airplane, Feature:D1')
#d2
ad2 = airplane.iloc[:,34:44].T
axs[0, 2].plot(x, ad2)
axs[0, 2].set_title('Class:Airplane, Feature:D2')
#d3
ad3 = airplane.iloc[:,44:54].T
axs[0, 3].plot(x, ad3)
axs[0, 3].set_title('Class:Airplane, Feature:D3')
#d4
ad4 = airplane.iloc[:,54:64].T
axs[0, 4].plot(x, ad4)
axs[0, 4].set_title('Class:Airplane, Feature:D4')

#human
#a3
ha3 = human.iloc[:,14:24].T
axs[1, 0].plot(x, ha3)
axs[1, 0].set_title('Class:Human, Feature:A3')
#d1
hd1 = human.iloc[:,24:34].T
axs[1, 1].plot(x, hd1)
axs[1, 1].set_title('Class:Human, Feature:D1')
#d2
hd2 = human.iloc[:,34:44].T
axs[1, 2].plot(x, hd2)
axs[1, 2].set_title('Class:Human, Feature:D2')
#d3
hd3 = human.iloc[:,44:54].T
axs[1, 3].plot(x, hd3)
axs[1, 3].set_title('Class:Human, Feature:D3')
#d4
hd4 = human.iloc[:,54:64].T
axs[1, 4].plot(x, hd4)
axs[1, 4].set_title('Class:Human, Feature:D4')

#table
#a3
ta3 = table.iloc[:,14:24].T
axs[2, 0].plot(x, ta3)
axs[2, 0].set_title('Class:Table, Feature:A3')
#d1
td1 = table.iloc[:,24:34].T
axs[2, 1].plot(x, td1)
axs[2, 1].set_title('Class:Table, Feature:D1')
#d2
td2 = table.iloc[:,34:44].T
axs[2, 2].plot(x, td2)
axs[2, 2].set_title('Class:Table, Feature:D2')
#d3
td3 = table.iloc[:,44:54].T
axs[2, 3].plot(x, td3)
axs[2, 3].set_title('Class:Table, Feature:D3')
#d4
td4 = table.iloc[:,54:64].T
axs[2, 4].plot(x, td4)
axs[2, 4].set_title('Class:Table, Feature:D4')

#plier
#a3
pa3 = plier.iloc[:,14:24].T
axs[3, 0].plot(x, pa3)
axs[3, 0].set_title('Class:Plier, Feature:A3')
#d1
pd1 = plier.iloc[:,24:34].T
axs[3, 1].plot(x, pd1)
axs[3, 1].set_title('Class:Plier, Feature:D1')
#d2
pd2 = plier.iloc[:,34:44].T
axs[3, 2].plot(x, pd2)
axs[3, 2].set_title('Class:Plier, Feature:D2')
#d3
pd3 = plier.iloc[:,44:54].T
axs[3, 3].plot(x, pd3)
axs[3, 3].set_title('Class:Plier, Feature:D3')
#d4
pd4 = plier.iloc[:,54:64].T
axs[3, 4].plot(x, pd4)
axs[3, 4].set_title('Class:Plier, Feature:D4')

#vase
#a3
pa3 = vase.iloc[:,14:24].T
axs[4, 0].plot(x, pa3)
axs[4, 0].set_title('Class:Vase, Feature:A3')
#d1
pd1 = vase.iloc[:,24:34].T
axs[4, 1].plot(x, pd1)
axs[4, 1].set_title('Class:Vase, Feature:D1')
#d2
pd2 = vase.iloc[:,34:44].T
axs[4, 2].plot(x, pd2)
axs[4, 2].set_title('Class:Vase, Feature:D2')
#d3
pd3 = vase.iloc[:,44:54].T
axs[4, 3].plot(x, pd3)
axs[4, 3].set_title('Class:Vase, Feature:D3')
#d4
pd4 = vase.iloc[:,54:64].T
axs[4, 4].plot(x, pd4)
axs[4, 4].set_title('Class:Vase, Feature:D4')


# Hide x labels and tick labels for top plots and y ticks for right plots.
for ax in axs.flat:
    ax.label_outer()


#-----------------------------------------------------------------------------------

#multiplot for global features
#in order to obtain different global measire plots, the column id should be changed!


fig, axs = plt.subplots(2, 3, sharex='all', sharey='all')

#airplane
aa3 = airplane.iloc[:, 7].T
axs[0, 0].hist(aa3, color = "skyblue")
axs[0, 0].set_title('Class: Airplane')

#human
ha3 = human.iloc[:, 7].T
axs[0, 1].hist(ha3, color = "orange")
axs[0, 1].set_title('Class: Human')

#table
ta3 = table.iloc[:, 7].T
axs[0, 2].hist(ta3, color = "brown")
axs[0, 2].set_title('Class: Table')

#plier
pa3 = plier.iloc[:, 7].T
axs[1, 0].hist(pa3, color = "black")
axs[1, 0].set_title('Class: Plier')

#vase
ka3 = vase.iloc[:, 7].T
axs[1, 1].hist(ka3, color = "red")
axs[1, 1].set_title('Class: Vase')

#chair
ca3 = chair.iloc[:, 7].T
axs[1, 2].hist(ca3, color = "magenta")
axs[1, 2].set_title('Class: Chair')

# Hide x labels and tick labels for top plots and y ticks for right plots.
for ax in axs.flat:
    ax.label_outer()
