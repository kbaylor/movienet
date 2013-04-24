'''
Created on Apr 22, 2013

@author: Owner
'''

import csv
import json

if __name__ == '__main__':
    NAME_INDEX = 0
    YEAR_INDEX = 8
    GENRE_INDEX = 9
    ID_INDEX = 13
    ILLEGAL_YEAR_VALUES = ['UNK', 'VAR', '']
    
    movie_json = []
    movie_genre_json = []
    with open("./sources/dvd_data.csv", 'r') as movie_file:
        reader = csv.reader(movie_file)
        reader.next()
        auto_increment = 1
        for line in reader:
            movie_id = int(line[ID_INDEX])
            movie_name = unicode(line[NAME_INDEX])
            genre = [unicode(line[GENRE_INDEX])]
            year = line[YEAR_INDEX]
            if year in ILLEGAL_YEAR_VALUES:
                year = 'NULL'
            else:
                year = int(year)
            movie_json.append({'pk':movie_id, 'model':'movieapp.movie', 'fields': {'name':movie_name, 'year':year}})
            movie_genre_json.append({'pk':auto_increment, 'model':'movieapp.moviegenre', 'fields': {
                            'movie':movie_id, 'genre':genre}})
            auto_increment += 1
    with open("../../../movieapp/fixtures/movie.json", 'w') as movie_fixture:
        movie_fixture.write(json.dumps(movie_json, indent=4))
    with open("../../../movieapp/fixtures/moviegenre.json", 'w') as movie_fixture:
        movie_fixture.write(json.dumps(movie_genre_json, indent=4))
    
        