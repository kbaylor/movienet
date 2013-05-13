'''
Created on Apr 22, 2013

@author: Owner
'''

import json
import re
import random
import datetime

def getValidJson(num_ratings, num_users):
    json_struct = []
    
    
    for r in range(0,num_ratings):
        for x in range(1,num_users+1):
            userid = int(x)
            json_struct.append({'pk':x*num_ratings+r, 'model':'movieapp.rated', 'fields': {
                        'user':userid, 'movie':r+5000,'rating': random.randint(1,10),
                        'date_rated':"2013-03-16T17:41:28+00:00"}})
    return json_struct

if __name__ == '__main__':
    ratings = getValidJson(10, 100)
    with open("registration/fixtures/ratings.json", 'w') as ratings_file:
        ratings_file.write(json.dumps(ratings, indent=4))