'''
Created on Feb 25, 2013

@author: yoav
'''
#! /usr/bin/env python

import json
import nltk
import math




#gets the data from the file in the form of a list
data = []
with open('/home/yoav/python/everything_app/movies_train.json') as f:
    for line in f:
        data.append(json.loads(line))
print(len(data))
data=data[:1000]
        
#gets all the plots as one string
stopwords=[',','the','and','a','to','of',]

plots=[]
for movie in data:
    plots.append(movie["plot"])  
tokens=nltk.word_tokenize("".join(plots))
for t in tokens:
    t=t.lower()


token_dist = nltk.FreqDist(tokens)
dictionary = token_dist.keys()[50:500]
dictionary_values = token_dist.values()[50:500]

for i in range(len(dictionary)):
    print(dictionary[i],dictionary_values[i])

all_generes=[]
for movie in data:
    movie_generes=movie["genres"]
    for genre in movie_generes:
        all_generes.append(genre)
    
genre_dist = nltk.FreqDist(all_generes)
genre_dictionary = genre_dist.keys()
genre_dicitonary_values = genre_dist.values()

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
            
teta=[]
for c in range(len(genre_dictionary)):
    teta_c=[] 
    for i in range(len(dictionary)):
        teta_c.append(Tetaic(i,c))
    teta.append(teta_c)

def calculate_probability_in_genre_c(x,c): #logp(x|y=c)
    a=0
    for i in range(len(dictionary)):
        a+=x[i]*math.log(teta[c][i])+(1-x[i])*math.log(1-teta[c][i])
    return a

def den(x,c):
    return math.exp(calculate_probability_in_genre_c(x,c)+math.log(get_genre_probability(c)))

def nom(x,c):
    a=0
    for c in range(len(genre_dictionary)):
        a+=den(x,c)
    return a

test = []
with open('/home/yoav/python/everything_app/movies_test.json') as f:
    for line in f:
        test.append(json.loads(line))
test=test[1001:1050]
probability_of_test_in_genre=[]
for i in range(len(test)):
    movie_plot = test[i]["plot"]
    tokenized_movie_plot=nltk.word_tokenize(movie_plot)
    x=[]
    for j in range(len(dictionary)):
        if dictionary[j] in tokenized_movie_plot:
            x.append(1)
        else:
            x.append(0)
    probability_of_test_in_genre.append(float(den(x,1)/float(nom(x,1))))
print(probability_of_test_in_genre)



    


