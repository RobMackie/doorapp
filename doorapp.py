import cherrypy
from mako.template import Template
from mako.lookup import TemplateLookup
from users import Users
import argparse
from doorIO import DoorGPIO;

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
    def admin(self, username=None, password=None):
        if self.users.verify_password(username, password):
            users = self.users.get_users();
            return self.template("admin.html", uname = username, users=users, error = "")
        return self.show_mainpage("Incorrect user/password combination");
    @cherrypy.expose
    def log(self):
        with open('doorapp.log', 'r') as f:
           return self.template("log.html", error = "", logFile = f)
    @cherrypy.expose
    def unlock(self,username=None,password=None):
        if self.users.verify_password(username, password):
            if password == self.users.get_mac(username):
                return "Must change password from default before unlocking"
            self.door.unlock(username);
            return "";
        else:
            return "Incorrect user/password combination"
    @cherrypy.expose
    def changePass(self,username=None,oldpass=None,newpass=None):
        print username + "***"
        print oldpass + "***"
        print newpass
        if self.users.verify_password(username, oldpass):
            self.users.change_password(username, newpass);
            return "";
        else:
            return "Incorrect user/password combination"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="TFI Door Unlocker")
    parser.add_argument('conf')
    args = parser.parse_args()

    cherrypy.quickstart(DoorApp(),'', args.conf)
