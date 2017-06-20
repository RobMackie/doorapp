import os
import json
import argparse
from passlib.apps import custom_app_context as pwd_context

class Users(object):
    def __init__(self):
        self.users = {};
        self.path = 'users.json'
        try:
            with open(self.path, 'r') as user_file:
                self.users = json.loads(user_file.read())         
        except:
            pass
    def __str__(self):
        result = ''
        for user in self.users:
            result +=  user + '\n'
        return result
    def save(self):
        with open(self.path, 'w') as user_file:
               json.dump(self.users, user_file)
        
# if username already exists, this overwrites it.   So be careful upon calling it!
    def add(self, username, password):
        self.users[username] = {}
        self.users[username]['password'] = pwd_context.hash(password)
        self.save();
    def remove(self, username):
        uname = self.get(username);
        if uname:
            del self.users[uname];
            self.save()
            
    def change_password(self, username, newpass):
        self.users[username]['password'] = pwd_context.hash(newpass)
        self.save();
    def get(self, username):   # this will return the case version that is in the users list
        if not username:
            return ''  # not found
        lower_username = username.lower()
        for key in self.users:
            if key.lower() == lower_username:
                return key
        return ''   # not found        
    def verify_password(self, username_in,password):
        username = self.get(username_in)
        if username:
            return pwd_context.verify(password, self.users[username]['password'])
        else:
            return False;

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--add', nargs=2, dest='user_add', default=[], help='add user <username> <pass>')
    parser.add_argument('--del', nargs=1, dest='user_del', default=[], help='del user <username>')
    results = parser.parse_args()
    
    users = Users();
    if results.user_add:
       users.add(results.user_add[0], results.user_add[1])
    if results.user_del:
        users.remove(results.user_del[0])

    print "User list"
    print "========="
    print users