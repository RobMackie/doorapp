import cherrypy
from mako.template import Template
from mako.lookup import TemplateLookup
from users import Users
import argparse
import time

logFile = open("doorapp.log", "a+", 0)   # 0 is unbuffered

## For running on Raspberry Pi
try:
   import RPi.GPIO as GPIO 
   TEST_ONLY = False
except:
   TEST_ONLY = True

class DoorGPIO(object):
    def __init__(self):
        if not TEST_ONLY:
           print "GPIO Version: " + GPIO.VERSION
           GPIO.setmode(GPIO.BOARD)
           self.pin = 11   # This is the header pin, NOT the GPIO pin
           GPIO.setup(self.pin, GPIO.OUT)
        else:
           print "---- NO GPIO WORKING!!! ---- "
    def unlock(self, user):
        logStr = time.asctime() + ": " + user + " unlocking door"
        print logStr
        logFile.write(logStr)
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
    def show_mainpage(self, error=''):
        return self.template("mainpage.html", error = error)
    
    @cherrypy.expose
    def index(self):
        return self.show_mainpage()

    @cherrypy.expose
    def unlock(self,username=None,password=None):
        if self.users.verify_password(username, password):
            self.door.unlock(username);
            return "";
        else:
            return "Incorrect user/password combination"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="TFI Door Unlocker")
    parser.add_argument('conf')
    args = parser.parse_args()   
        
    cherrypy.quickstart(DoorApp(),'', args.conf)
