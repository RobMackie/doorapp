import cherrypy
from mako.template import Template
from mako.lookup import TemplateLookup
from users import Users
import argparse
import time
import threading

logFile = open("doorapp.log", "a+", 0)   # 0 is unbuffered

## For running on Raspberry Pi
try:
   import RPi.GPIO as GPIO
   TEST_ONLY = False
except:
   TEST_ONLY = True

def unlockIO(pin):
   if TEST_ONLY:
      print "Unlock test"
   elif GPIO.input(pin) != GPIO.HIGH:
      GPIO.output(pin, GPIO.HIGH)
      time.sleep(5)
      GPIO.output(pin, not GPIO.input(self.pin))


class DoorGPIO(object):
    def __init__(self):
        self.pin = 11;
        if not TEST_ONLY:
           print "GPIO Version: " + GPIO.VERSION
           GPIO.setmode(GPIO.BOARD)
           GPIO.setup(self.pin, GPIO.OUT)
        else:
           print "---- NO GPIO WORKING!!! ---- "

    def unlock(self, user):
        logStr = time.asctime() + ": " + user + " unlocking door" + "\n"
        print "--- " + logStr
        logFile.write(logStr)
        t = threading.Thread(target=unlockIO,args=(self.pin,))
        t.start()

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
    # TEMPORARY!!!!!
    @cherrypy.expose
    def admin(self):
        users = self.users.get_users();
        return self.template("admin.html", uname = "alan", users=users, error = "")
    # end of TEMPORARY
    @cherrypy.expose
    def log(self):
        with open('doorapp.log', 'r') as f:
           return self.template("log.html", error = "", logFile = f)
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
