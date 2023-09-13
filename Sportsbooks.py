# -*- coding: utf-8 -*-
"""
Created on Sun Aug  6 19:21:30 2023

@author: danie
"""
import requests
import pandas as pd



def get_initial(stats):
    x = 0
    #function to get the initial subcategory integer
    while True:
        try:
            stats['eventGroup']['offerCategories'][x]['offerSubcategoryDescriptors']
            break
        except KeyError:
            x += 1
            
    return x

def get_next(stats, first):
    x = 0
    while True:
        try:
            stats['eventGroup']['offerCategories'][first]['offerSubcategoryDescriptors'][x]['offerSubcategory']
            break
        except KeyError:
            x += 1
    return x

def get_xmax(stats, first, second):
    x = 0
    while True:
        try:
            stats['eventGroup']['offerCategories'][first]['offerSubcategoryDescriptors'][second]['offerSubcategory']['offers'][x][0]['outcomes']
            x += 1
            
            #parse through the table while increasing x each time. Use while loop to iterate
        except IndexError:
            #when error arises, stop while loop, decrease x by 1, and return x
            break
    x -= 1
    return x
    
    
    
def get_ymax(stats, first, second):
    y = 0
    #same steps as above function but increasing y each time
    while True:
        try:
            stats['eventGroup']['offerCategories'][first]['offerSubcategoryDescriptors'][second]['offerSubcategory']['offers'][0][y]['outcomes']
            y += 1
        except IndexError:
            break
    y -= 1
    return y


def create_frame(stats,frame,first, second, xmax, ymax):
    #create a dataframe and seed the data through the maximum values of x and y
    for i in range(xmax + 1):
        for b in range(ymax + 1):
            try:
                player = stats['eventGroup']['offerCategories'][first]['offerSubcategoryDescriptors'][second]['offerSubcategory']['offers'][i][b]['outcomes'][0]['participant']
                stat = stats['eventGroup']['offerCategories'][first]['offerSubcategoryDescriptors'][second]['name']
                label = stats['eventGroup']['offerCategories'][first]['offerSubcategoryDescriptors'][second]['offerSubcategory']['offers'][i][b]['outcomes'][0]['label']
                line = stats['eventGroup']['offerCategories'][first]['offerSubcategoryDescriptors'][second]['offerSubcategory']['offers'][i][b]['outcomes'][0]['line']
                odds = stats['eventGroup']['offerCategories'][first]['offerSubcategoryDescriptors'][second]['offerSubcategory']['offers'][i][b]['outcomes'][0]['oddsAmerican']
                label2 = stats['eventGroup']['offerCategories'][first]['offerSubcategoryDescriptors'][second]['offerSubcategory']['offers'][i][b]['outcomes'][1]['label']
                line2 = stats['eventGroup']['offerCategories'][first]['offerSubcategoryDescriptors'][second]['offerSubcategory']['offers'][i][b]['outcomes'][1]['line']
                odds2 = stats['eventGroup']['offerCategories'][first]['offerSubcategoryDescriptors'][second]['offerSubcategory']['offers'][i][b]['outcomes'][1]['oddsAmerican']
                frame.loc[len(frame.index)] = [player, stat, label, line, odds] 
                frame.loc[len(frame.index)] = [player, stat, label2, line2, odds2]
            except IndexError:
                break
    return frame

def main():
    odds_df = pd.DataFrame(columns = ['Player Name', 'Stat', 'O/U', 'line', 'odds'])
    for sub in ['12149','6607','7979']:
        stat_url = 'https://sportsbook.draftkings.com/sites/US-SB/api/v5/eventgroups/84240/categories/743/subcategories/'+sub+'?format=json'
        data = requests.get(url = stat_url).json()
        first = get_initial(data)
        second = get_next(data, first)
        xmax = get_xmax(data, first, second)
        ymax = get_ymax(data, first, second)
        odds_df = create_frame(data,odds_df, first, second, xmax, ymax)
    return odds_df
    
odds_df = main()
odds_df = odds_df.sort_values(by = ['Stat', 'odds'], ascending = [True, False])
print(odds_df)
odds_df.to_csv('HRR.csv', index = False)


 
        
        
        
  