'''
Created on Feb 25, 2013

@author: yoav
'''

import json
import nltk
import math
import urllib
import os, sys
### Trainer extracts a relevant dictionary from the training set, and creates the occurunce matrix of the words in the movie plot

def get_training_set(): #extracts the training set from file into a python list
    data = []
    dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
    path=os.path.join(dirname, "movies_train.json")
    with open(path) as f:
        for line in f:
            data.append(json.loads(line))
    return data

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
    #get unique categories
    genre_dist = nltk.FreqDist(all_generes)
    return genre_dist.keys()

#gets the indexes of the movies in genre c
def get_genre_indexes(c,dictionary,genre_dictionary): 
    selected_movie_genre=genre_dictionary[c]
    genre_indexes=[] 
    for index,movie in enumerate(data):
        movie_generes=movie["genres"]
        for genre in movie_generes:
            if genre==selected_movie_genre:
                genre_indexes.append(index) 
    return genre_indexes   
#the distribution of genres in train corpus, as probability
def get_genre_probability(c,dictionary,genre_dictionary):
    return float(len(get_genre_indexes(c,dictionary,genre_dictionary)))/float(len(data))
#helper function for aithmetic
def Nic(i,c,dictionary,genre_dictionary):
    Nic=0
    indexes = get_genre_indexes(c,dictionary,genre_dictionary)
    for j in range(len(indexes)):
        if dictionary[i] in plots[indexes[j]]:
            Nic+=1
    return Nic
#helper function for aithmetic

def Nc(c,dictionary,genre_dictionary):
    number_of_movies_in_genre=len(get_genre_indexes(c,dictionary,genre_dictionary))
    return number_of_movies_in_genre
#helper function for aithmetic

def Tetaic(i,c,dictionary,genre_dictionary):
    teta=float(Nic(i,c,dictionary,genre_dictionary)+1)/float(Nc(c,dictionary,genre_dictionary)+2)
    return teta
#calculates teta matrix with helper function 
def getTeta(dictionary,genre_dictionary):
    teta=[]
    for c in range(len(genre_dictionary)):
        teta_c=[] 
        for i in range(len(dictionary)):
            teta_c.append(Tetaic(i,c,dictionary,genre_dictionary))
        teta.append(teta_c)
    return teta

data=get_training_set() 
#sets inital data as global params
results=get_dictionary(data)
plots=results[0]
tokens=results[1]
dictionary=results[2]
genre_dictionary=get_genre_dictionary(data)

#produces the teta matrix and passes params to classifier
def main():
    genre_probability=[]
    for index in range(len(genre_dictionary)):   
        genre_probability.append(get_genre_probability(index,dictionary,genre_dictionary))
    teta=getTeta(dictionary,genre_dictionary)
    return (teta,dictionary,genre_dictionary,genre_probability)

if __name__ == "__main__":
    main()



            

