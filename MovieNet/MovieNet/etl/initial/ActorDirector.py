'''
Created on Apr 22, 2013

@author: Owner
'''

import csv
import json

def getValidJson(index_file, name_file, model_name):
    id_to_movies = {}
    reader = csv.reader(index_file)
    reader.next()
    for line in reader:
        name_id = int(line[1])
        movie_id = int(line[2])
        if name_id not in id_to_movies:
            id_to_movies[name_id] = []
        id_to_movies[name_id].append(movie_id)
    json_struct = []
    reader = csv.reader(name_file)
    reader.next()
    for line in reader:
        if int(line[0]) in id_to_movies:
            movies = id_to_movies[int(line[0])]
        else:
            movies = []
        json_struct.append({'pk':int(line[0]), 'model':model_name, 'fields': {
                    'name':unicode(line[1]), 'movies':movies}})
    return json_struct

if __name__ == '__main__':
    with open("./sources/director_index.csv", 'r') as index_file:
        with open("../sources/directors.csv", 'r') as csvfile:
            directors = getValidJson(index_file, csvfile, 'movieapp.director')
    with open("../../../movieapp/fixtures/director.json", 'w') as director_file:
        director_file.write(json.dumps(directors, indent=4))
        
    with open("./sources/actor_index.csv", 'r') as index_file:
        with open("../sources/actors.csv", 'r') as csvfile:
            actors = getValidJson(index_file, csvfile, 'movieapp.actor')
    with open("../../../movieapp/fixtures/actor.json", 'w') as director_file:
        director_file.write(json.dumps(actors, indent=4))