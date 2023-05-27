#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 19:01:47 2023

@author: victor
"""

# Imports
import matplotlib.pyplot as plt
import os
import pandas as pd

# Functions
def stats(user):
    ''' Takes as input a user's name, and creates a CSV file with the mean and 
        standard deviation of their user ratings, Letterboxd ratings, and Letterboxd
        rating count. This CSV file also stores the variation between user and
        Letterboxd rating. '''
    
    # customize the path variable with the local path to your data file
    path = os.getcwd() + '/' + user + '/' + user
    
    dataframe = readData(path + 'data.csv', user)
    
    path = os.getcwd() + '/' + user + '/' + user + 'stats.csv'
    dataframe.to_csv(path, index = 'False') # converts statistics to CSV
    
def readData(path, user):
    ''' Takes as input a path to the user's data.csv file, and returns a dataframe with
        the following statistics: mean and standard deviation of their user ratings, 
        Letterboxd ratings, and Letterboxd rating count, and variation between user 
        and Letterboxd rating. '''
    
    data = pd.read_csv(path, index_col = None, encoding = 'latin-1', encoding_errors = 'ignore')
   
    # creates histogram distributions of the movie data and saves them as pdfs
    path = os.getcwd() + '/' + user + '/' + user
    data.hist(column = 'User Rating', grid = False)
    plt.savefig(path + 'UR.pdf')
    data.hist(column = 'Letterboxd Rating', grid = False)
    plt.savefig(path + 'LR.pdf')
    data.hist(column = 'Letterboxd Rating Count', grid = False)
    plt.savefig(path + 'LRC.pdf')
    
    statistics = {
        'Statistic': ['Mean', 'Standard Deviation', 'Variation'],
        'User Rating': [data['User Rating'].mean(), data['User Rating'].std(), data['User Rating'].mean() - data['Letterboxd Rating'].mean()],
        'Letterboxd Rating': [data['Letterboxd Rating'].mean(), data['Letterboxd Rating'].std(), data['Letterboxd Rating'].mean() - data['User Rating'].mean()],
        'Letterboxd Rating Count': [data['Letterboxd Rating Count'].mean(), data['Letterboxd Rating Count'].std(), 'N/A']
        }
    columns = ['Statistic', 'User Rating', 'Letterboxd Rating', 'Letterboxd Rating Count']
    
    
    df = pd.DataFrame(statistics, columns = columns) # creates the dataframe
    return df