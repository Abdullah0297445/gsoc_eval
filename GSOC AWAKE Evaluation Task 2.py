# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 22:32:15 2019

@author: abdul
"""

import glob
import h5py
import pandas as pd


class fileTraversal:
    def __init__(self):
        
        self.awake = {}
        #Read groups, datasets, size, shape, dtype info from .h5 file and write into
        #this dictionary.
        #Later we will write this dictionary into a csv file.
    
    def helperFunc(self,item, key, datatype, counter, Ds=True):
        '''
        Some repetitive utility tasks i.e. operations on our class dictionary 'awake'. So
        I put them into this seperate function rather writing same thing again and again in 
        'traverse' function.
        '''
        
        if Ds == True:
            #This node is a dataset and these operations will be performed on 'awake' dict.
            
            self.awake['Dataset'].append(key)                   #Name of dataset.
            self.awake['Size'].append(str(item[key].size))      #Size of dataset.
            self.awake['Shape'].append(str(item[key].shape))    #Shape of dataset.
            self.awake['DataType'].append(datatype)             #Type of dataset.
        
            for i in range(len([key for key, value in self.awake.items() if key.startswith("GroupLevel_")])):
                self.awake['GroupLevel_' + str(i)].append(' ')
                #Since all the lists in 'awake' dictionary should be of same length we are appending
                #empty elements into 'group' list because this node is a dataset. 
                #The length of all lists should be same because we have to convert this 
                #dictionary into a pandas dataframe and for that conversion to be successful 
                #we need to keep the length same.
                
        else:
            #This node is a group and these operations will be performed on 'awake' dict.  
            
            if 'Dataset' not in self.awake:
                self.awake['Dataset'] = []
            if 'GroupLevel_' + str(counter) not in self.awake:
                self.awake['GroupLevel_' + str(counter)] = []
                for i in range(len(self.awake['Dataset'])):
                    self.awake['GroupLevel_' + str(counter)].append(' ')
            
            if 'Size' not in self.awake:
                self.awake['Size'] = []
            if 'Shape' not in self.awake:
                self.awake['Shape'] = []
            if 'DataType' not in self.awake:
                self.awake['DataType'] = []
            #Our Dictionary is empty initially that is why we should check first whether a key 
            #exists or not. That is why these 'if' statements are for.
            #If a key does not exist we add it into our dictionary.
            
            
            for i in range(len([key for key, value in self.awake.items() if key.startswith("GroupLevel_")])):
                if i != counter:
                    self.awake['GroupLevel_' + str(i)].append(' ')
                    
            self.awake['GroupLevel_' + str(counter)].append(key)
            #Name of the group.
            
            self.awake['Dataset'].append(' ')
            self.awake['Size'].append(' ')
            self.awake['Shape'].append(' ')
            self.awake['DataType'].append(' ')
            #Similarly we are appending empty elements into 'Dataset', 'Size', 'Shape',
            #'Datatype' lists because this node is a group and groups do not have these properties. 
    
    def traverse(self, item, counter):
        '''
        This function goes to every node in h5 file and retrieve 
        node's name, size, shape, datatype if node is a dataset or just name if node is a group
        and write this information into our class variable 'awake' which is a dictionary.
        '''
        try:
            for key in item:
                
                if isinstance(item[key], h5py.Dataset):
                    
                    try:
                        datatype = item[key].dtype
                        #Get the datatype of this node.
                        self.helperFunc(item, key, datatype, counter, True)
                        counter = 0
                        
                    except TypeError as err:
    
                        datatype = 'Custom Datatype'
                        self.helperFunc(item, key, datatype, counter, True)
                        counter = 0
                    
                else:
    
                    self.helperFunc(item, key, ' ', counter, False)
                    self.traverse(item[key], counter+1)
                    #Recursive call to function itself due of heirarcial structure of file.
        except :
            pass
        
        self.keysArranged = [key for key, value in self.awake.items() if key.startswith("GroupLevel_")] + [key for key, value in self.awake.items() if not key.startswith("GroupLevel_")]
        #Our dictionary keys were unarranged intially because keys were added dynamically in random
        #order as our code proceeds to execute.
        #Why do we need sorting/arranging? Because we have to write this dict into a csv file 
        #so its columns should be in this order :
        #GROUP  Dataset  Size  Shape  Datatype  
        
        self.awake = dict((k, self.awake[k]) for k in tuple(self.keysArranged))
        #Replaing the old 'awake' with another dictionary which has 
        #ordered keys as our requirement.
         
        self.df = pd.DataFrame(self.awake, columns = self.keysArranged)
        #Finally convert this dict into a pandas dataframe.

           
if __name__ == "__main__":
    ft = fileTraversal()
    with h5py.File(glob.glob("1541962108935000000_167_838.h5")[0],'r') as f:
        #print(filename)
        ft.traverse(f, 0)
        ft.df.to_csv (r'C:\Users\abdul\Desktop\\' + str(f.filename.split('.')[0]) + '.csv', index = None, header=True) 
