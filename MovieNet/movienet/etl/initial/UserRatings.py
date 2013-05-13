'''
Created on Apr 22, 2013

@author: Owner
'''

import json
import re
import random
import csv
import datetime

def getValidJson(num_ratings, num_users):
    json_struct = []
    movieid_list=[]
   # with open("MovieNet/etl/initial/sources/dvd_data.csv", 'r') as movie_file:
    with open("./sources/dvd_data.csv", 'r') as movie_file:
        reader = csv.reader(movie_file)
        reader.next()
        for line in reader:
            movieid_list.append(int(line[13]))
    
    for x in range(1,num_users+1):
        userid = int(x)
        movies_rated=[]
        for r in range(0,num_ratings):
            month = random.randint(3,5);
            movie_to_rate = random.randint(0,len(movieid_list)-1)
            while movie_to_rate in movies_rated:
                movie_to_rate = random.randint(0,len(movieid_list)-1)

            movies_rated.append(movie_to_rate)
            json_struct.append({'pk':x*num_ratings+r, 'model':'movieapp.rated', 'fields': {
                        'user':userid, 'movie':movieid_list[movie_to_rate],'rating': random.randint(1,10),
                        'date_rated':"2013-0"+`month`+"-12T17:41:28+00:00"}})
    return json_struct

if __name__ == '__main__':
    ratings = getValidJson(1000, 100)
    #with open("registration/fixtures/ratings_3.json", 'w') as ratings_file:
    with open("../../../registration/fixtures/ratings_3.json", 'w') as ratings_file:
        ratings_file.write(json.dumps(ratings, indent=4))