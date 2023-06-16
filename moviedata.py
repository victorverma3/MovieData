#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 13:53:49 2023

@author: victor
"""

# Imports
from bs4 import BeautifulSoup
import concurrent.futures
import json
from movierecs import *
from moviestats import *
import os
import pandas as pd
import requests as requests
import time

# Data Corrections
''' If a new ratings.csv is downloaded, optionally fix the spelling of these titles:
    - WALL-E
    - Les Miserables
    - Leon: The Professional
    - Once Upon a Time... in Hollywood
    - Star Wars: Episode II - Attack of the Clones
    - Star Wars: Episode III - Revenge of the Sith
    - Any title with Pokemon in it
'''

# Functions
def gatherData(user):
    ''' Takes as input a user's name, and returns a list of movies with incomplete
        data available on Letterboxd. A CSV is created that contains the title,
        user rating, Letterboxd rating, Letterboxd rating count, genres, and country 
        of origin of all of the user's movies. It also creates a CSV of the 
        summary statistics of the movie data. '''
        
    start = time.perf_counter() # starts timer for program
   
    # customize the path variable with the local path to your Letterboxd ratings file
    path = f'./data/{user}ratings.csv'
    
    r = readRatings(path)
    
    errors = [] # stores any movie titles that don't have the necessary data available
    
    titles = []
    userRatings = []
    avgRatings = []
    ratingsCount = []
    genres = []
    countries = []
    
    # uses multithreading to efficiently gather movie data
    with concurrent.futures.ThreadPoolExecutor(max_workers = None) as executor:
        futures = {executor.submit(getInfo, movie): movie for movie in r}
        for future in concurrent.futures.as_completed(futures):
            info = futures[future]
            info = future.result()
            try:
                if len(info) == 1:
                    errors += [info[0]]
                    continue
                titles += [info[0]]
                userRatings += [info[1]]
                avgRatings += [info[2]]
                ratingsCount += [info[3]]
                genres += [info[4]]
                countries += [info[5]]
            except Exception as exc:
                print(f'{info} movie generated an exception: {exc}')
    
    # creates a dictionary storing all of the data
    data = {
        'Title': titles,
        'User Rating': userRatings,
        'Letterboxd Rating': avgRatings,
        'Letterboxd Rating Count': ratingsCount,
        'Genres': genres,
        'Country of Origin': countries
        }
    
    # converts the data dictionary into a dataframe
    df = pd.DataFrame(data, columns = ['Title', 
                                       'User Rating', 
                                       'Letterboxd Rating', 
                                       'Letterboxd Rating Count', 
                                       'Genres', 
                                       'Country of Origin'])
    
    # converts the dataframe into a csv
    path = f'./{user}/{user}data.csv'
    df.to_csv(path, index = 'False')
    
    stats(user) # creates a csv of summary statistics of the movie data
    
    finish = time.perf_counter() # ends timer for program
    
    print('\nThe program took ' + str(finish - start) + ' seconds to complete') # prints the time it took for compilation of data
    print('\nThe user data is stored in <user>data.csv, and the user statistics are stored in <user>statstest.csv')
    print('\nMovies that are missing necessary data:\n' + str(errors))
    print('\nHistograms displaying user rating, Letterboxd rating, and Letterboxd rating count:')
    return
    
def readRatings(path):
    ''' Takes as input the path to the user's ratings.csv file, and returns a 
        list. Each element in the list corresponds to a movie, and contains the
        movie's title, Letterboxd URI, and user rating. '''
    df = pd.read_csv(path, index_col = None, encoding = 'latin-1', encoding_errors = 'ignore')
    r = []
    row = 0
    
    # iterates through all movies in the user's Letterboxd ratings file
    while row < len(df):
        r += [[df['Name'][row], df['Letterboxd URI'][row], df['Rating'][row]]]
        row += 1
    return r

def getInfo(movie):
    ''' Takes as input a list with the movie's name, Letterboxd URI, and user 
        rating, and returns a list containing the movie's name, user rating, 
        Letterboxd rating, Letterboxd rating count, genres, and country of origin 
        If there is an error, a list containing just the movie title is returned. '''
    
    print(movie[0]) # movies are printed so user can track compilation progress
    page = requests.get(str(movie[1]))
    soup = BeautifulSoup(page.text, 'html.parser')
    script = str(soup.find('script', {'type': 'application/ld+json'}))
    
    script = script[52:-20] # html is trimmed to just json data
    data = json.loads(script)
    
    r = []
    try:
        r += [movie[0],
              movie[2],
              data['aggregateRating']['ratingValue'], 
              data['aggregateRating']['ratingCount'], 
              data['genre'], 
              data['countryOfOrigin'][0]['name']]
    except:
        print(str(movie[0]) + ' caused an error') # movies with missing data are printed to output
        return [movie[0]]
    return r