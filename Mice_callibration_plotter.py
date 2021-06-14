# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 10:48:35 2019

@author: Administrator

Scrip to read any txt file organized in columns

"""
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#%% Load the dataset 
# The user choose the txt file 
# Quality control passed data in TPM (Transcripts per Million)
#data_file = r'C:\MATLAB_FOLDER\Light Display\Exp_data\161207mk_calibration20.txt'


data_file = r'C:\MATLAB_FOLDER\Light Display\Exp_data\191217seb_TestManualBallRotation_turns_during_2min_3min_recording_acw_27.txt'
dataset = pd.read_csv(data_file,sep='\t',header=0, index_col =None)

#%% Fixed Parameters
ball_radius = 3 # (in mm)
ball_circumference = 2 * math.pi * ball_radius

#%% User Parameters
#variable = dataset.firstposy
variable = dataset.secondposy
derivative = np.gradient(variable)
number_of_pauses = 1 # Change this number accordingly
number_of_rotations = 53 # Change this number accordingly
turning_time = 120 #in seconds

#%% Variable Parameters
maximum_distance = np.amax(variable)
distance_per_rotation = maximum_distance/(number_of_rotations * number_of_pauses)
convertion_factor = ball_circumference/distance_per_rotation
first_data_point = variable[4400:].loc[variable[4400:] != 0].index[0]
last_data_point = variable.loc[variable == maximum_distance].index[0]
duration_turnings = last_data_point - first_data_point
sampling_rate = duration_turnings/turning_time

print('FIRST data point at frame number: ', first_data_point)
print('LAST data point at frame number: ', last_data_point)
print('DURATION of recording in frames: ', duration_turnings)
print('SAMPLING RATE was: ', sampling_rate)
print('Maximum distance: ', maximum_distance)
print('Conversion factor: ', convertion_factor)


#%% Plotting 
plt.figure()
plt.plot(derivative)
plt.plot(variable)
plt.show()

#%% Variability calculation for triades
a = 0.2466
b = 0.2953
c = 0.2553
my_list = [a,b,c]

#d = 0.2523
#e = 0.2470
#f = 0.2314
#g = 0.2257
#h = 0.2261
#i = 0.2559
#my_list = [a,b,c,d,e,f,g,h,i]

np.mean(my_list)
np.std(my_list)
percentatge_of_variation_to_max = ((np.amax(my_list)-np.mean(my_list)) * 100) /np.mean(my_list)
percentatge_of_variation_to_min = (((np.amin(my_list)-np.mean(my_list)) * 100) /np.mean(my_list))*-1
print('----------------------------------------------------------------------------------------------')
print('The mean+- std is: ',np.mean(my_list), '+/-',np.std(my_list))
print('The % to the max: ',percentatge_of_variation_to_max)
print('The % to the min: ',percentatge_of_variation_to_min)