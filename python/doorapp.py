import cherrypy
from mako.template import Template
from mako.lookup import TemplateLookup
from users import Users
import argparse
import time

## For running on Raspberry Pi
try:
   import RPi.GPIO as GPIO 
   TEST_ONLY = False
except:
   TEST_ONLY = True

class Cookie(object):
    def __init__(self, name):
        self.name = name;
    def get(self, default=''):
        result = default
        try:
           result = cherrypy.session.get(self.name)
           if not result:
              self.set(default)
              result = default
        except:
           self.set(default);
        return result;
    def set(self, value):
        cherrypy.session[self.name] = value
    def delete(self):
        cherrypy.session.pop(self.name, None)
        self.set('', 0)  # Way to delete a cookie is to set it with an expiration time of immediate

class DoorGPIO(object):
    def __init__(self):
        if not TEST_ONLY:
           print "GPIO Version: " + GPIO.VERSION
           GPIO.setmode(GPIO.BOARD)
           self.pin = 11   # This is the header pin, NOT the GPIO pin
           GPIO.setup(self.pin, GPIO.OUT)
        else:
           print "---- NO GPIO WORKING!!! ---- "
    def unlock(self):
        print "Unlocking door"
        if not TEST_ONLY:
           GPIO.output(self.pin, GPIO.HIGH)
           time.sleep(5)
           GPIO.output(self.pin, not GPIO.input(self.pin))
        

class DoorApp(object):
    def __init__(self):
        self.users = Users();
        self.lookup = TemplateLookup(directories=['HTMLTemplates'],default_filters=['h'])
        self.door = DoorGPIO()

    def template(self, name, **kwargs):
        return self.lookup.get_template(name).render(**kwargs);
    def show_mainpage(self, username,error=''):
        return self.template("mainpage.html", username= username, error = error)
    def show_loginpage(self, error=''):
        return self.template("login.html", error = error)
    
    @cherrypy.expose
    def index(self):
        username = Cookie('username').get()
        if not username:
            return self.show_loginpage()
        return self.show_mainpage(username)

    @cherrypy.expose
    def login(self,username=None,password=None):
        if self.users.verify_password(username, password):
            Cookie('username').set(self.users.get(username))
            return self.show_mainpage(username);
        else:
            return self.show_loginpage("Username and password don't match")

    @cherrypy.expose
    def logout(self):
        cherrypy.lib.sessions.expire()
        return self.show_loginpage('')

    @cherrypy.expose
    def unlock(self):
# Check for being removed from access list or not logged in
        username = self.users.get(Cookie('username').get())
        if not username:
            return self.show_loginpage()
        self.door.unlock()    
        return self.show_mainpage(username)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="TFI Door Unlocker")
    parser.add_argument('conf')
    args = parser.parse_args()   
        
    cherrypy.quickstart(DoorApp(),'', args.conf)
