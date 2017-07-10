#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  8 20:04:31 2017

@author: josemanuel
"""
import pandas as pd
import numpy as np
import time

class Model(object):
    
    def __init__(self,W=0,H=0,n_sheets=0):
        
        self.sheets=pd.DataFrame(columns=['Width','Height','x','y','lx','ly','items','checked_item'])
        self.items=pd.DataFrame(columns=['Width','Height','id','sheet','x','y'])
        self.W=W
        self.H=H
        self.n_sheets=n_sheets
        
    def config_sheet(self, W, H):
        self.W=W
        self.H=H

            
    def set_sheets_df(self, W, H, n_sheets):
        self.W=W
        self.H=H
        self.n_sheets=n_sheets
        #self.sheets=pd.DataFrame(columns=['Width','Height','x','y','lx','ly','items'])
        for x in range(int(n_sheets)):
            sheet_pd=pd.DataFrame([[self.W,self.H,0,0,0,0,[],[],x+1]],columns=['Width','Height','x','y','lx','ly','items','checked_item','index'])
            sheet_new=sheet_pd.set_index(keys='index')
            self.sheets=self.sheets.append(sheet_new)
    
    def get_info_sheets(self):
        print("# of sheets: %d" % self.n_sheets)
        print("Sheet dimension: Width - %d ; Height - %d" % (self.W,self.H))
        
    def get_info_items(self):
        print(self.items)
    
    def add_item(self,element):
        
        """Input: list of the shape - (Width, Height, id) """
        
        index=self.items.shape[0]+1
        sheet=0
        starting_point=0
        element[0].append(sheet)
        element[0].append(starting_point)
        element[0].append(starting_point)
        element[0].append(index)
        element_pd=pd.DataFrame(element, columns=['Width','Height','id','sheet','x','y','index'])
        element_new=element_pd.set_index(keys='index')
        self.items=self.items.append(element_new)
        
    def add_sheet(self,n):
        
        sheet_pd=pd.DataFrame([[self.W,self.H,0,0,0,0,[],[],n+1]],columns=['Width','Height','x','y','lx','ly','items','checked_item','index'])
        sheet_new=sheet_pd.set_index(keys='index')
        self.sheets=self.sheets.append(sheet_new)
        
    def sort_items(self):
        #self.items['WidthxHeight']=self.items['Width']*self.items['Height']
        self.items=self.items.sort_values('Height',ascending=False)
    
    def compute_lb(self):
        self.items['WidthxHeight']=self.items['Width']*self.items['Height']
        return round(self.items['WidthxHeight'].sum()/(self.W*self.H),0)
    
    def find_minsheets(self):
        self.sort_items()
        n_used_sheets=self.compute_lb()
        self.set_sheets_df(self.W, self.H, n_used_sheets)
        items_not_stored=self.items.shape[0]
        items_pd = self.items.copy()
        items_to_delete=[]
        self.closed_sheets=pd.DataFrame(columns=['Width','Height','x','y','lx','ly','items','checked_item'])
        while items_not_stored > 0:
            n_fail=0
            while items_not_stored>0 and n_fail<20 :
                items_pd = self.items.copy()
                items_pd = items_pd[~items_pd['id'].isin(items_to_delete)]
                for index_sheets, sheet in self.sheets.iterrows():
                    for index_items, item in items_pd.iterrows():      
                        
                        if item['Width'] <= sheet['Width'] and item['Height'] <= sheet['Height']:
                            items_not_stored = items_not_stored - 1
                            items_to_delete.append(item['id'])
                            self.items['x'][index_items] = sheet['x']
                            self.items['y'][index_items] = sheet['y']
                            self.items['sheet'][index_items] = index_sheets
                            self.sheets['Width'][index_sheets]= sheet['Width'] - item ['Width']
                            self.sheets['x'][index_sheets]= sheet['x'] + item['Width']
                            self.sheets['items'][index_sheets].append(item['id'])
                    #print(~items_pd['id'].isin(items_to_delete))
                    items_pd = items_pd[~items_pd['id'].isin(items_to_delete)]
                
                #print(self.items)
                #print(self.sheets)
                for index_sheets, sheet in self.sheets.iterrows():
                    pd_temp=self.items[self.items['id'].isin(self.sheets['items'][index_sheets])]
                    pd_temp['total_height']=pd_temp['y']+pd_temp['Height']
                    pd_temp=pd_temp[~pd_temp['id'].isin(sheet['checked_item'])]
                    #print(pd_temp)
                    if all(x == pd_temp['total_height'].iloc[0] for x in pd_temp['total_height']) and pd_temp.shape[0] > 1:
                        for index_checked_items, row in pd_temp.iterrows():
                            self.sheets['checked_item'][index_sheets].append(row['id'])
                        ly=min(pd_temp['total_height'])
                        if ly>=self.H:
                            self.closed_sheets=self.closed_sheets.append(self.sheets.loc[[index_sheets]])
                            self.sheets=self.sheets.drop([index_sheets])
                        else:
                            self.sheets['ly'][index_sheets]=ly
                            self.sheets['y'][index_sheets]=self.sheets['ly'][index_sheets]
                            self.sheets['Height'][index_sheets]=self.H-self.sheets['y'][index_sheets]
                            if self.sheets['Height'][index_sheets]==0:
                                self.sheets['lx'][index_sheets]=0
                                self.sheets['Width'][index_sheets]=0
                            else:
                                self.sheets['lx'][index_sheets]=0
                                self.sheets['x'][index_sheets]=0
                                self.sheets['Width'][index_sheets]=self.W
                            
                        
                    elif pd_temp.shape[0] > 0:
                        ly=min(pd_temp['total_height'])
                        self.sheets['checked_item'][index_sheets].append(pd_temp['id'][pd_temp['total_height'].argmin()])
                        item_id=pd_temp['id'][pd_temp['total_height'].argmin()]
                        lx=pd_temp['Width'][pd_temp['id']==item_id].values[0]
                        if ly>=self.H or self.sheets['Width'][index_sheets]+lx > self.W:
                            self.closed_sheets=self.closed_sheets.append(self.sheets.loc[[index_sheets]])
                            self.sheets=self.sheets.drop([index_sheets])
                            
                        else:
                            self.sheets['ly'][index_sheets]=ly
                            self.sheets['lx'][index_sheets]=lx
                            self.sheets['x'][index_sheets]=self.sheets['x'][index_sheets]-lx
                            self.sheets['y'][index_sheets]=self.sheets['ly'][index_sheets]
                            self.sheets['Width'][index_sheets]=self.sheets['Width'][index_sheets]+lx
                            self.sheets['Height'][index_sheets]=self.H-self.sheets['y'][index_sheets]
                n_fail=n_fail+1
                #print('fails',n_fail)
                #print('items left',items_not_stored)
                #print(self.items)
                #print(self.sheets)
                #input("Press Enter to continue...")
            #print(items_not_stored)
            if items_not_stored != 0 :
                    self.add_sheet(n_used_sheets)
                    n_used_sheets=n_used_sheets+1
            print(self.sheets.shape[0])

        return n_used_sheets        
    
    
        