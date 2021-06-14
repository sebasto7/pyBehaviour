# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 09:12:42 2020

@author: Sebastian Molina-Obando
"""

##Analysis walking behavior

import glob
import numpy as np
from core_functions_behavioral_analysis import read_data_txt
from core_functions_behavioral_analysis import sort_data
from core_functions_behavioral_analysis import quantify_data

#Spyder is clearing all variables after every execution. Settings: > Tools > Preferences > Run

# data folder, in the current configuration is in the same directory as this scrips

dirPath = 'C:\\MATLAB_FOLDER\\Behavioral data analysis\\Exp_Data\\Example_data\\cylinders\\'

# here give a string identifier of the set of files you want to analyze

files = glob.glob(dirPath + '*mk*.txt')
N = len(files)

#% some parameters
deltat = 1/120 # 120hz of adquisition rate frequency. The inverse is the period in sec>> keep in mind that the exact deltat are variable
CF = np.array([0.063 , 0.063])/10 # this is cm/dot
radius = 0.3; # in cm
cut_points = np.array([0.2 ,2.25])   #these two numbers are used to cut the stimulus epochs 
                    #First # says how much earlier (in seconds) than the pattern onset
                    #Second # says how much later. 
                    #The total length cut out for each epoch is first # + second 
                    
# opening all files and quantifing behavior 
data_list = list()                   
for fname in files:
    data = read_data_txt(fname, CF, deltat, radius)
    data_list.append(data)
    
print('Total number of files analyzed:', len(data_list))

# sorting all data in stimulus and variable type
data_sorted = sort_data(data_list, np.around(cut_points/deltat))

# quantifying some stadistics in the data
data_statistics = quantify_data (data_sorted)



    