'''
Created on Feb 25, 2013

@author: yoav
'''

import json
import nltk
import math
import urllib
### Trainer extracts a relevant dictionary from the training set, and 

#url_training='https://s3.amazonaws.com/doat/assignment/movies_train.json.bz2'
#urllib.urlopen(url)
#file_name = url.split('/')[-1]
#u = urllib2.urlopen(url)
#f = open(file_name, 'wb')
#gets the data from the file in the form of a list
data = []
with open('/home/yoav/python/everything_app/movies_test.json') as f:
    for line in f:
        data.append(json.loads(line))
data=data[:1000]
        
#gets all the plots as one string

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
