# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 12:21:53 2020

@author: Sebastian Molina-Obando
"""

#import numpy as np

def read_data_txt (filename, CF, deltat, radius):
    
    """Calculates the rotational, translational, lateral and forward velocities.
    
    Parameters
    ==========
    filaname : txt file
        Indices are sample points and column names are the different variables
    CF: conversion factor dot/cm. A numpy.ndarray length=2. One value for each sensor
    
    deltat: 1/sampling rate
    radiur: radius of the ball in cm
    
    Returns
    =======
    data: pandas data frame with calculated velocities and pattern ids
    """         
    import pandas as pd
    import numpy as np
    Table = pd.read_table(filename) # explore T= np.loadtxt(filename)
    v1 = np.array([Table['firstvely'], Table['firstvelx']])*CF[0]/deltat    # seb: in Mainz x and y are flipped. This gives cm/
    v2 = np.array([Table['secondvely'], Table['secondvelx']])*CF[1]/deltat  # seb: in Mainz x and y are flipped. This gives cm/s
    # So "firstvely = x1" and  "firstvelx = y1". Consider this in the formulas below.
    
    # here we assume a fixed absolute angle of 45 degrees between heading direction and horizontal axis of the sensors
    phi = np.pi/4; # This is in radians units and corresponds to 45 degrees.
    vfwd = -(v1[1]+v2[1]*np.cos(phi))       #  -(y1+y2)* cos(phi)
    vlat = -(v1[1]-v2[1]*np.sin(phi))       #  -(y1-y2)* sin(phi)
    vrot = -(v1[0]+v2[0])/(2*radius);       #  -(x1+x2)/ 2*radius  % "*radius" turns linear velocity into angular velocity 
    vtras = np.sqrt(np.power(vfwd,2) + np.power(vlat,2)); 
    stim = Table['pattern_id']
    
    all_ = (np.vstack((vfwd, vlat, vrot,vtras,stim)).T)
        
    data = pd.DataFrame(all_,columns=['vfwd', 'vlat', 'vrot','vtras','stim'])
    
    return data



def sort_data (data, cut_points):
    
    """Cuts the data according to the start of each stimulus repetition and sorts the data acoodring to the stimulus id
    
    Parameters
    ==========
    data : list of pandas data frames
        each raw contains a dataframe
    
    cut_points: time points (in seconds) where to cut each variable in the dataframe
    
    Returns
    =======
    data_sorted: a list that contains a nested dictionary for each file 
        each nested dictionary contains data sorted by stimulus ID
        inside each stimlus ID, there are all the calculated variables 
        each variable is an 2D array containing all trials (iterations of the stimulus)
    
    """         
    
    import numpy as np
    var = data[0].columns
    cut_points = cut_points.astype(int)
    file_number = 0
    data_sorted =[]
    
    for d in data:
        file_number = file_number + 1
        stimon = np.asarray(np.where(np.diff(d.stim) > 0)) + 1 # find stimulus start points (stimon)
        stimon = stimon[0][1:-1] # discarding the first and last points (it helps removing inconsistencies between files)
        stimID = d.stim[stimon]
        stim_code = np.unique(stimID)
        dict_stimcode ={}
        
        for sc in stim_code:
            stimon_id= stimon[stimID==sc] # start points for one specific stimulus
            dict_variables = {}
            
            for v in var:
                var_temp = d[v]
                array_temp = np.zeros([1,sum(cut_points)])
                
                
                for sid in stimon_id:
                    cut1= sid-cut_points[0]
                    cut2= sid+cut_points[1]
                    temp = np.array(var_temp.iloc[cut1:cut2]) # Cutting one sitmulus iteration here
                    temp = np.reshape(temp, (1,len(temp)))
                    array_temp = np.concatenate((array_temp,temp), axis=0) # Pulling all iterations (rows) together
    
                array_temp = array_temp[1:,:]
                dict_variables[v]= array_temp
            
            sc_str = sc.astype('str')
            dict_stimcode[sc_str] = dict_variables # We created a nested dictionary with all stimulus type
    
        data_sorted.append(dict_stimcode)
        print('Sorted file number: ', file_number)
    
    return data_sorted


def quantify_data(data):
    
    """Quantifies statistics in the data for each file
    
    Parameters
    ==========
    data : list of nested dictionaries
        each raw contains a dictionary with data sorted by stimulus ID
        each stimulus ID dictionary contains all calculated variables in 2D arrays
    
    
    Returns
    =======
    data_statistics: a list that contains a nested dictionary for each file 
        each nested dictionary contains data sorted by stimulus ID
        inside each stimlus ID, there are all the calculated statistics
    
    """
    
    import numpy as np
    
    data_statistics =[]
    for d in data:
        
        dict_stimcode = {}
        
        for sc in d:
            dict_temp = d.get(sc)
            dict_statistics = {}
            
            for var in dict_temp:
                trials = dict_temp.get(var)
                mean =np.mean(trials, axis=0)
                std = np.std(trials, axis =0)
                sem = std/np.sqrt(np.size(trials,1))
                dict_statistics[var] = [mean, std, sem, trials]
                # Keep adding anything you would like to quantify!
            
            dict_stimcode[sc] = dict_statistics
            
        data_statistics.append(dict_stimcode)
    
    return data_statistics
