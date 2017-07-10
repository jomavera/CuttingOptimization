#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  9 18:00:17 2017

@author: josemanuel
"""

from cuttingOpt import *
modelo=Model()
modelo.config_sheet(10,8)
modelo.add_item([[4,6,1]])
modelo.add_item([[4,4,2]])
modelo.add_item([[8,3,3]])
modelo.add_item([[4,3,4]])
modelo.add_item([[4,3,5]])
modelo.add_item([[4,3,6]])
modelo.add_item([[1,3,7]])
modelo.add_item([[6,2,8]])
modelo.add_item([[2,2,9]])
modelo.add_item([[9,2,10]])
modelo.add_item([[9,2,11]])
modelo.add_item([[3,1,12]])
planchas=modelo.find_minsheets()
print(modelo.items)
modelo.draw_solution()