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
class Followed(webapp2.RequestHandler):
    def get(self):
        #Below code used to send the followedby  list of users to front end
        self.response.headers['Content-Type']= 'text/html'
        user = users.get_current_user()
        myuser_key=ndb.Key('Myuser',user.email())
        myuser=myuser_key.get()
        l=myuser.followedby_list
        dict={}
        dict1={}
        list=[]
        dict2={}
        mytweet=ndb.Key('Mytweet','default')
        mytweet=mytweet.get()
        available=""
        Bool=False
        if len(l)>0:
            list=l
        else:
            available="No followers available for this user"
            Bool=True
        template_values= {'list':list,'a':available,'Bool':Bool}
        template=JINJA_ENVIRONMENT.get_template('follower.html')
        self.response.write(template.render(template_values))
