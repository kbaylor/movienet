'''
Created on Apr 22, 2013

@author: Owner
'''

import json
import re
import datetime

def getValidJson(num_users):
    json_struct = []

    for x in range(1,num_users+1):
        id = int(x)
        json_struct.append({'pk':id, 'model':'registration.movienetuser', 'fields': {
                    'password':'password', 'last_login':"2013-03-16T17:41:28+00:00", 'is_superuser':'True',
                    'username':'user'+`x`, 'first_name':'first'+`x`,
                    'last_name':'last'+`x`, 'email':'user'+`x`+'@email.com',
                    'is_staff':'True','is_active':'True','date_joined':"2013-03-16T17:41:28+00:00",
                    'sex':'M', 'date_of_birth':"2013-03-16"}})
    return json_struct

if __name__ == '__main__':
    users = getValidJson(100);
    with open("registration/fixtures/user.json", 'w') as user_file:
        user_file.write(json.dumps(users, indent=4))