'''
Created on Feb 25, 2013

@author: yoav
'''
import trainer
import json
import nltk
import math


results=trainer.main()
teta=results[0]

dictionary=results[1]
genre_dictionary=results[2]
genre_probability=results[3]

def calculate_probability_in_genre_c(x,c): #logp(x|y=c)
    a=0
    for i in range(len(dictionary)):
        a+=x[i]*math.log(teta[c][i])+(1-x[i])*math.log(1-teta[c][i])
    return a

def den(x,c):
    return math.exp(calculate_probability_in_genre_c(x,c)+math.log(genre_probability[c]))

def nom(x,c):
    a=0
    for c in range(len(genre_dictionary)):
        a+=den(x,c)
    return a

def get_test_set(): #extracts the training set from file into a python list
    data = []
    with open('/home/yoav/python/everything_app/movies_test.json') as f:
        for line in f:
            data.append(json.loads(line))
    return data 

def get_probability_of_test_in_genre(x,c):
    
    probability_of_test_in_genre=(float(den(x,c)/float(nom(x,c))))
    return(probability_of_test_in_genre)


 
def main():   
    test=get_test_set()
    probability_of_test_set=[]
 
    for i in range(len(test)):
        probability_of_movie_in_set=[]
        x=[]
        movie_plot = test[i]["plot"]
        tokenized_movie_plot=nltk.word_tokenize(movie_plot)
        for j in range(len(dictionary)):
            if dictionary[j] in tokenized_movie_plot:
                x.append(1)
            else:
                x.append(0)
        
        for c in range(len(genre_dictionary)):
            probability_of_movie_in_set.append(get_probability_of_test_in_genre(x,c))        
        
        probability_of_test_set.append(probability_of_movie_in_set)

    
    for i in range(len(test)):
        for j in range(len(genre_dictionary)):
            if probability_of_test_set[i][j]>0.03:
                print('Title: '+test[i]["name"]+','+genre_dictionary[j]+': '+"{:.0%}".format(probability_of_test_set[i][j])) 

if __name__ == "__main__":
    main()



