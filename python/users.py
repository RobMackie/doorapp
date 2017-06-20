import os
import json
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
    users = Users();
    users.add('test1', 'testpass');
    if users.verify_password('test1','testpass'):
        print 'Password verify positive works'
    else:
        print 'Password verify positive FAIL'
    if users.verify_password('test1','wrongpass'):
        print 'Wrong password negative FAIL'
    else:
        print 'Wrong password negative works'
    users.remove('test1')