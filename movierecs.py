#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  2 20:56:26 2023

@author: victor
"""

# Imports
import os
import pandas as pd
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# concatenate the two dataframes into a single dataframe
#concatenated = pd.concat([dataRef, data])

# compute the cosine similarity between the columns of the concatenated dataframe
#similarity_matrix = cosine_similarity(concatenated.T)

# find the indices of the rows in df2 that are most similar to df1
#most_similar_indices = similarity_matrix[len(ref):].argmax(axis=0)

# create a new dataframe containing the most similar rows from df2
#most_similar_df = df.iloc[most_similar_indices, :]
#print(most_similar_df)

def rec(user, k = 10):
    df = pd.read_csv(os.getcwd() + '/' + user + '/' + user + 'data.csv')
    i = random.randint(0, len(df) - 1)
    cosSim = cosine_similarity(vector(df))
    similar_items = cosSim[i].argsort()[::-1][1:k+1]
    print('\nThese are the ' + str(k) + ' movies most similar to ' + df['Title'][i] + ' that ' + user.title() + ' has watched:\n')
    for j in similar_items:
        print(df['Title'][j])
        
def rec2(user, k = 10):
    df = pd.read_csv(os.getcwd() + '/' + user + '/' + user + 'data.csv')
    ref = pd.read_csv(os.getcwd() + '/joseph/josephdata.csv')
    '''# create a boolean mask for the rows in df that match ref
    mask = df['Title'].isin(ref['Title'])

    # filter out the matching rows from df
    filtered_df = df[~mask]
    
    # concatenate the two dataframes into a single dataframe
    concatenated = pd.concat([ref, filtered_df], axis = 0)
    concatenated = concatenated.drop('Unnamed: 0', axis = 1)
    print(concatenated)'''
    
    concatenated = pd.concat([ref, df], ignore_index = True).drop('Unnamed: 0', axis = 1)
    concatenated = concatenated.groupby(['Title', 'Genres', 'Country of Origin'], as_index=False).mean()
    concatenated.to_csv('concat.csv', index = 'False')
    
    dataframe = vector(concatenated)

    # compute the cosine similarity between the columns of the concatenated dataframe
    similarity_matrix = cosine_similarity(dataframe)

    # find the indices of the rows in df2 that are most similar to df1
    most_similar_indices = similarity_matrix[len(ref):].argmax(axis=0)

    # create a new dataframe containing the most similar rows from df2
    most_similar_df = df.iloc[most_similar_indices[:5]]
    return most_similar_df['Title']
        
def vector(dataframe):
    # Extract the string columns and convert them to a list of strings
    stringCols = ['Genres', 'Country of Origin']
    stringData = dataframe[stringCols].apply(lambda x: ' '.join(x), axis=1).tolist()

    # Extract the numeric columns as a numpy array
    numericCols = ['User Rating', 'Letterboxd Rating', 'Letterboxd Rating Count']
    numericData = dataframe[numericCols].values
    
    # Vectorize the string data using TF-IDF
    vectorizer = TfidfVectorizer().fit(stringData)
    string_data_vec = vectorizer.transform(stringData)
    
    data = pd.concat([pd.DataFrame(string_data_vec.toarray()), pd.DataFrame(numericData)], axis=1).values
    return data
        
#Print the top k similar items
#print(f'Top {k} similar items to item {i}: {similar_items}')
