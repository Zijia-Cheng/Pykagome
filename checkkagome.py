#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 15:17:33 2020

@author: zijiacheng
"""

import pymatgen
import numpy as np


def checkkagome(structure):
    """This is used for checking whether a material has a kagome lattice perpendicular to z direction,structure should be belongs to type: pymatgen.core.structure.Structure"""
    
    
    
    #Here with convention, we just take c axis to be z axis, which is the stacking axis.
    
    
    
    if not (type(structure) == pymatgen.core.structure.Structure):
        
        raise TypeError("input type is wrong")
        
    #Different species    
    species_set = set(structure.species)
    
    
    signal = 0 #index to judge whether it is kagome or not
    
    if(len(species_set)<4):#abandon the system which has more than three different elements
        
        for species in species_set:
            coordinate_list = structure.indices_from_symbol(species.value)#indices of the species in the structure list
            if (len(coordinate_list) < 3 or len(coordinate_list) > 6):
                continue ## test whether there are at least three same elements in the conventional unit cell. At the same time ,we don't want too many atoms in the unit cell
            # Now choose atoms with same z value
            zcord = np.empty(len(coordinate_list))
            for i in range(0,len(coordinate_list)):
                zcord[i] = structure.sites[coordinate_list[i]].frac_coords[2]
            
            #sort the z values of sites
            zcord_sort, index, occurnumber = np.unique(zcord,return_index=True,return_counts=True)
            #Now choose z value such that occurnumber is 3
            for i in range(0,len(occurnumber)):
                if(occurnumber[i] == 3):
                    #check there is no other elements in this plane(More strict!!!)。 FeSn doesn't satify this requirement
                    # plane_valid = 0
                    # for sites in structure.sites:
                        
                    #     if(sites.frac_coords[2] == zcord[index[i]] and sites.species.elements[0] != species):
                    #         plane_valid = 1
                    #         break 
                    
                    # if (plane_valid == 1):
                    #     break                        
                    zvalue = zcord[index[i]] 

                     #Check in this plane whether the neareaset neirghor is 4
                    basic_lattice = np.empty((3,3))
                    s = 0 
                    for j in range(0,len(coordinate_list)):
                        if (zcord[j] == zvalue):
                            basic_lattice[s] = structure.sites[coordinate_list[j]].coords
                            s = s+1
                    
                    
                    expand_lattice =  np.empty((27,3))
                    s = 0
                    
                    for m in range(0,3):
                        for i in range(-1,2):
                            for j in range(-1,2):
                                expand_lattice[s] =basic_lattice[m]+i*structure.lattice.matrix[0]+j*structure.lattice.matrix[1]
                                s = s+1
                   
                    
                    for i in range(0,3):
                        distance = np.zeros(27)
                        near_neighbor = 0
                        for j in range(0,27):
                            distance[j] = np.linalg.norm(basic_lattice[i] - expand_lattice[j])
                        
                        distance_sort = np.sort(distance)
                        for m in range(1,27):
                            # the tolerance ratio right now is 10%, so if you need breathing kagomes, may need to expand this
                            if(np.absolute((distance_sort[m] - distance_sort[1])/distance_sort[1] < 0.01)):
                                near_neighbor = near_neighbor+1
                            else:
                                break
                        if(near_neighbor ==4 and np.absolute((distance_sort[5] - distance_sort[1]))/distance_sort[1] > 0.6):
                            signal = 1
                        else:
                            signal = 0
                            break
                if signal == 1:
                    break
            if signal == 1:
                break
    
    return signal
                
                    
                        
                    
                
                    
                
                
                         
        
       
        

        
        




            
      
        
        
            
            
        
        
        
    
    
    
    
    
    
   
    
    
        
    