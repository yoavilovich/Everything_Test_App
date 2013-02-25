'''
Created on Feb 25, 2013

@author: yoav
'''

import json
import nltk
import math
import urllib
### Trainer extracts a relevant dictionary from the training set, and creates the occurunce matrix of the words in the movie plot

def get_training_set(): #extracts the training set from file into a python list
    data = []
    with open('/home/yoav/python/everything_app/movies_test.json') as f:
        for line in f:
            data.append(json.loads(line))
    return data[:1000]  #1000 is to minimize training set for speedier results

def get_dictionary(data): 
#    finds the most common words from combining all plots together, 
#    and creates a dictionary. Returns a list of all plots in training
#    set and a list of all words (tokens) in all the plots
    plots=[]
    tokens=[]
    for movie in data:
        plots.append(movie["plot"])  
        #tokenized_movie_plot=nltk.word_tokenize(movie["plot"])
    tokens=nltk.word_tokenize("".join(plots))
    for t in tokens:
            t=t.lower()
    #tokens.append(tokenized_movie_plot)
    token_dist = nltk.FreqDist(tokens)
    dictionary = token_dist.keys()[50:500]
    #dictionary_values = token_dist.values()[50:500]    
    return (plots,tokens,dictionary)

def get_genre_dictionary (data): #return a genre dictionary, i.e, all the possible genres

    all_generes=[]
    for movie in data:
        movie_generes=movie["genres"]
        for genre in movie_generes:
           all_generes.append(genre)
    
    genre_dist = nltk.FreqDist(all_generes)
    return genre_dist.keys()
    #genre_dicitonary_values = genre_dist.values()

def get_genre_indexes(c): 
    selected_movie_genre=genre_dictionary[c]
    genre_indexes=[] 
    for index,movie in enumerate(data):
        movie_generes=movie["genres"]
        for genre in movie_generes:
            if genre==selected_movie_genre:
                genre_indexes.append(index) 
    return genre_indexes   

def get_genre_probability(c):
    return float(len(get_genre_indexes(c)))/float(len(data))

def Nic(i,c):
    Nic=0
    indexes = get_genre_indexes(c)
    for j in range(len(indexes)):
        if dictionary[i] in plots[indexes[j]]:
            Nic+=1
    return Nic

def Nc(c):
    number_of_movies_in_genre=len(get_genre_indexes(c))
    return number_of_movies_in_genre

def Tetaic(i,c):
    teta=float(Nic(i,c)+1)/float(Nc(c)+2)
    return teta

def getTeta():
    teta=[]
    for c in range(len(genre_dictionary)):
        teta_c=[] 
        for i in range(len(dictionary)):
            teta_c.append(Tetaic(i,c))
        teta.append(teta_c)
    return teta

if __name__ == "__main__":

    data=get_training_set() 

    results=get_dictionary(data)
    plots=results[0]
    tokens=results[1]
    dictionary=results[2]

    genre_dictionary=get_genre_dictionary(data)

    teta=getTeta()
    print(teta[1][3])
            

