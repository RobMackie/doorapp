import cherrypy
from mako.template import Template
from mako.lookup import TemplateLookup
from users import Users
import argparse
import os
from doorIO import DoorGPIO;

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
        return value
    def delete(self):
        cherrypy.session.pop(self.name, None)

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
        Cookie('username').delete()
        return self.show_mainpage()
    @cherrypy.expose
    def admin(self, username=None, password=None):
        username_sess = Cookie('username').get('')
        if username_sess:
            username = username_sess
        if username_sess or self.users.verify_password(username, password):
            username = Cookie('username').set(self.users.get(username))
            return self.template("admin.html", uname = username, users=self.users.get_users(), error = "")
        return self.show_mainpage("Incorrect user/password combination");
    @cherrypy.expose
    def log(self):
        f = os.popen('tail -n 100 doorapp.log')
        return self.template("log.html", error = "", logFile = f)
    @cherrypy.expose
    def addUser(self,uname=None, mac=None, admin=None):
        if Cookie('username').get(''):
            if self.users.get(uname):
                return "Already a user with that name"
            else:
               self.users.add(uname, mac, mac[-5:])
               return ""
        return "An admin is not currently logged in";
    @cherrypy.expose
    def editUser(self,uname=None, mac=None, admin=None):
        if Cookie('username').get(''):
            if self.users.get(uname):
                self.users.edit(uname, mac, admin)
                return ""
            else:
               return "No user with that name"
        return "An admin is not currently logged in";
    @cherrypy.expose
    def add(self):
        if Cookie('username').get(''):
            return self.template("user.html", edit=False, uname='', mac='', admin=False)
        return self.show_mainpage("An admin is not currently logged in");
    @cherrypy.expose
    def edit(self,uname=None):
        if Cookie('username').get(''):
            return self.template("user.html", edit=True, uname=uname, mac=self.users.get_mac(uname), admin=self.users.get_admin(uname))
        return self.show_mainpage("An admin is not currently logged in");
    @cherrypy.expose
    def delete(self,uname=None):
        if Cookie('username').get(''):
            self.users.remove(uname);
            return "";
        return self.show_mainpage("An admin is not currently logged in");
    @cherrypy.expose
    def resetPass(self,uname=None):
        if Cookie('username').get(''):
            self.users.change_password(uname, self.users.get_mac(uname)[-5:]);
            return "";
        return self.show_mainpage("An admin is not currently logged in");

    @cherrypy.expose
    def unlock(self,username=None,password=None):
        if self.users.verify_password(username, password):
            if password == self.users.get_mac(username)[-5:]:
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
