#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  9 16:31:46 2017

@author: josemanuel
"""
import pandas as pd

sheets=pd.DataFrame([[20,10,0,0,0,0,[]],[20,10,0,0,0,0,[]],[20,10,0,0,0,0,[]]],columns=['W','H','x','y','lx','ly','elements'])
#sheets['elements'] = ''
#sheets['elements'] = sheets['elements'].apply(list)
items=pd.DataFrame([[15,5,0,0,1],[15,3,0,0,2],[15,2,0,0,3]],columns=['W','H','x','y','id'])
items['y'][0]=5
items['y'][2]=3
sheets['elements'][0].append(items['id'][0])
sheets['elements'][0].append(items['id'][2])
#ly=min(items['y'].iloc(items['id']==sheets['elements'][0]))
pd_temp=items[items['id'].isin(sheets['elements'][0])]
ly=min(pd_temp['H'])
item_id=pd_temp['id'][pd_temp['H'].argmin()]
lx=pd_temp['W'][pd_temp['id']==item_id].values