import argparse
import os
import cherrypy
from mako.lookup import TemplateLookup
from users_new import Users
from doorIO import DoorGPIO


class Cookie(object):
    def __init__(self, name):
        self.name = name

    def get(self, default=''):
        result = default
        try:
            result = cherrypy.session.get(self.name)
            if not result:
                self.set(default)
                result = default
        except:
            self.set(default)
        return result

    def set(self, value):
        cherrypy.session[self.name] = value
        return value

    def delete(self):
        cherrypy.session.pop(self.name, None)


class DoorApp(object):
    def __init__(self):
        self.users = Users()
        self.lookup = TemplateLookup(
            directories=['HTMLTemplates'], default_filters=['h'])
        self.door = DoorGPIO()

    def template(self, name, **kwargs):
        return self.lookup.get_template(name).render(**kwargs)

    def show_mainpage(self, error=''):
        return self.template("mainpage.html", error=error)

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
            username = Cookie('username').set(self.users.get(username)['user'])
            return self.template("admin.html", uname=username, users=self.users.users, error="")
        return self.show_mainpage("Incorrect user/password combination")

    @cherrypy.expose
    def log(self):
        f = os.popen('tail -n 100 doorapp.log')
        return self.template("log.html", error="", logFile=f)
 
    @cherrypy.expose
    def unlock(self, username=None, password=None):
        if self.users.verify_password(username, password):
            self.door.unlock(username)
            self.users.sendUnlock(self.users.get(username))
            return ""
        else:
            return "Incorrect user/password combination"
    
    @cherrypy.expose
    def update(self):
        self.users.getUpdatedAccounts()
        return self.index()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="TFI Door Unlocker")
    parser.add_argument('conf')
    args = parser.parse_args()
    cherrypy.quickstart(DoorApp(), '', args.conf)
