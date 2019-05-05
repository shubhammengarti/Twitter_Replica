import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
from myuser import Myuser
from tweet import Tweet
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)
class Edit(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type']= 'text/html'
        user = users.get_current_user()
        myuser_key=ndb.Key('Myuser',user.email())
        myuser=myuser_key.get()
        l=""
        l1=""
        button=self.request.get("button")
        Bool=True
        if myuser!=None:
            myuser=myuser.query()
            if button!="edit":
                Bool=True
                for i in myuser:
                    if i.email==user.email():
                        l=(i.name)
                        l1=(i.description)
            elif button=="edit":
                Bool=False
                for i in myuser:
                    if i.email==user.email():
                        l=(i.name)
                        l1=(i.description)
        template_values= {'l':l,'l1':l1,'Bool':Bool}
        template=JINJA_ENVIRONMENT.get_template('edit.html')
        self.response.write(template.render(template_values))
    def post(self):
        #Below code is used for updating user profiles
        self.response.headers['Content-Type']= 'text/html'
        user = users.get_current_user()
        a=""
        if self.request.get("button")=="update":
            myuser_key=ndb.Key('Myuser',user.email())
            myuser=myuser_key.get()
            myuser.description=self.request.get("description")
            myuser.put()
            a="User Accounts Updated"
        if self.request.get("button")=="Cancel":
            a="Updation Cancelled"
        template_values= {'a':a}
        template=JINJA_ENVIRONMENT.get_template('create.html')
        self.response.write(template.render(template_values))
