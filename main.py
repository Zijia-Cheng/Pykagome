#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 22:05:27 2020

@author: zijiacheng
"""

from pymatgen.ext.matproj import MPRester
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
from checkkagome import checkkagome


# =============================================================================
with MPRester("xfzRTieDSOyvnZgq") as m:
   #import data:
       
   results_hexagonal = m.query(criteria={'spacegroup.crystal_system': {"$in": ["trigonal", "hexagonal"]}},properties=['material_id','structure','elements'])
   file = open("/Users/zijiacheng/Desktop/Princeton/python/kagome","w")

for i in range(0,len(results_hexagonal)):
    
    elements = results_hexagonal[i]["elements"]
    materials_id = results_hexagonal[i]["material_id"]
        # get convential unit cell
    structure = SpacegroupAnalyzer(results_hexagonal[i]["structure"]).get_conventional_standard_structure()
    
        #Now for searching Kagome lattice, we can first check whether at certain z there are at least
    if("Te" in  elements):
        signal = checkkagome(structure)
        if(signal == 1):
            file.write (materials_id + "\t"+ structure.formula + "\n")
        
    if(i%1000 == 0):
        print(i)
    
    
    
    
file.close()
    
    
    
        
    
