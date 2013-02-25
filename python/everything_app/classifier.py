'''
Created on Feb 25, 2013

@author: yoav
'''
import trainer
import json
import nltk
import math
import os, sys

#sets initial data as global params
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
#denominator of posterior
def den(x,c):
    return math.exp(calculate_probability_in_genre_c(x,c)+math.log(genre_probability[c]))
#nominator of posterior
def nom(x,c):
    a=0
    for c in range(len(genre_dictionary)):
        a+=den(x,c)
    return a

def get_test_set(): #extracts the training set from file into a python list
    data = []
    dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
    path=os.path.join(dirname, "movies_test.json")
    with open(path) as f:
        for line in f:
            data.append(json.loads(line))
    return data 
#gives the posterior probability for movie x and genre c
def get_probability_of_test_in_genre(x,c):
    
    probability_of_test_in_genre=(float(den(x,c)/float(nom(x,c))))
    return(probability_of_test_in_genre)


 
def main():   
    test=get_test_set()
    probability_of_test_set=[]
    #runs on all movies to produce X binary vector
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
 #prints the results of probabilities   
    for i in range(len(test)):
        for j in range(len(genre_dictionary)):
            if probability_of_test_set[i][j]>0.03:
                print('Title: '+test[i]["name"]+','+genre_dictionary[j]+': '+"{:.0%}".format(probability_of_test_set[i][j])) 
  #calculates recall, precision, and accuracy              
    recall=[]
    precision=[]
    accuracy=[]
    #seperately for each genre (classifier)
    for j in range(len(genre_dictionary)):     
        TP=0
        FP=0
        FN=0
        TN=0
        #decided False positive (FP), false negative(FN), true positive (TP) and true negative (TN)
        for i in range(len(test)):
            movie_generes=[]
            movie_generes_list=test[i]["genres"]
            for genre in movie_generes_list:
                movie_generes.append(genre)
            if probability_of_test_set[i][j]>0.3:
                classifier_result=1
                if genre_dictionary[j] in movie_generes:
                    TP+=1
                else:
                    FP+=1
            else:
                classifier_result=0
                if genre_dictionary[j] in movie_generes:
                    FN+=1
                else:
                    TN+=1

        #to prevent rare cases of undefined
        if TP+FN!=0:
            recall.append(float(TP)/float(TP+FN))
        else:
            recall.append(-0.01)
        if TP+FP!=0:
            precision.append(float(TP)/float(TP+FP))
        else:
            precision.append(-0.01)
        accuracy.append(float(TP+TN)/float(TP+TN+FP+FN))
    #print results
    for j in range(len(genre_dictionary)):        
        print('Genre: '+genre_dictionary[j]+', '+'Recall: '       
        +"{:.0%}".format(recall[j]) +', '+'Precision: '       
        +"{:.0%}".format(precision[j]) +', '+'Accuracy: '       
        +"{:.0%}".format(accuracy[j]))               

if __name__ == "__main__":
    main()



