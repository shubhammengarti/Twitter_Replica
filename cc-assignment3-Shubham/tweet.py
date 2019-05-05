import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
from myuser import Myuser
import datetime
from mytweet import Mytweet
from google.appengine.ext import blobstore
from uploadhandler import UploadHandler
from uploadhandler import ViewPhotoHandler
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)
class Tweet(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type']= 'text/html'
        template_values= { }
        template=JINJA_ENVIRONMENT.get_template('tweet.html')
        self.response.write(template.render(template_values))
    def post(self):
        self.response.headers['Content-Type']= 'text/html'
        user = users.get_current_user()
        current_time = datetime.datetime.now()
        email=user.email()
        a=""
        name=""
        count=""
        if self.request.get("button")=="submit":
            #Below code used to add the tweets in myuser and mytweet datastore
            dict={}
            myuser_key=ndb.Key('Myuser',user.email())
            myuser=myuser_key.get()
            myuser.tweet_list.append(self.request.get("tweet"))
            myuser.count+=1
            myuser.put()
            mytweet=ndb.Key('Mytweet','default')
            mytweet=mytweet.get()
            if mytweet==None:
                mytweet=Mytweet(id="default")
                mytweet.put()
                mytweet=Mytweet(id=str(myuser.name)+" "+str(myuser.count))
                mytweet.email=user.email()
                mytweet.tweet=self.request.get("tweet")
                mytweet.time=datetime.datetime.now()
                mytweet.count=myuser.count
                mytweet.name=myuser.name
                mytweet.put()
            else:
                mytweet=Mytweet(id=str(myuser.name)+" "+str(myuser.count))
                mytweet.email=user.email()
                mytweet.tweet=self.request.get("tweet")
                mytweet.time=datetime.datetime.now()
                mytweet.count=myuser.count
                mytweet.name=myuser.name
                mytweet.put()
                a="Tweet Saved "
        if self.request.get("button")=="cancel":
            self.redirect("/")
        template_values= {'a':a,'upload_url' : blobstore.create_upload_url('/upload'),'email':email}
        template=JINJA_ENVIRONMENT.get_template('tweet.html')
        self.response.write(template.render(template_values))
