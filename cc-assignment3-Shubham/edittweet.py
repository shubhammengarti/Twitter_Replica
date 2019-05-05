import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
from myuser import Myuser
from tweet import Tweet
import datetime
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)
class Edittweet(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type']= 'text/html'
        user = users.get_current_user()
        myuser_key=ndb.Key('Myuser',user.email())
        myuser=myuser_key.get()
        l=[]
        dict={}
        dict1={}
        lists1=[]
        dict2={}
        dict3={}
        tweet=""
        Bool=True
        if self.request.get("button")!="edit":
            #Below code used to display the user details with readonly option
            Bool=False
            if myuser!=None:
                mytweet=ndb.Key('Mytweet','default')
                mytweet=mytweet.get()
                for i in mytweet.query():
                    if i.name==myuser.name:
                            twe=i.tweet
                            dict[i.time]=twe
                            dict1[i.time]=i.name
                            lists1.append(i.time)
                            dict2[i.time]=((i.time).strftime("%b %d %Y %H:%M:%S"))
                            dict3[i.time]=i.blobs
                template_values= {'lists1':lists1,'dict':dict,'dict1':dict1,'dict2':dict2,'tweet':tweet,'Bool':Bool,'dict3':dict3}
                template=JINJA_ENVIRONMENT.get_template('edittweet.html')
                self.response.write(template.render(template_values))
            else:
                template_values= {}
                template=JINJA_ENVIRONMENT.get_template('edittweet.html')
                self.response.write(template.render(template_values))
        if self.request.get("button")=="edit":
            #Below code will updated the edited tweets
            tweet=self.request.get("twe")
            Bool=True
            template_values= {'lists1':lists1,'dict':dict,'dict1':dict1,'dict2':dict2,'tweet':tweet,'Bool':Bool}
            template=JINJA_ENVIRONMENT.get_template('edittweet.html')
            self.response.write(template.render(template_values))
    def post(self):
        self.response.headers['Content-Type']= 'text/html'
        user = users.get_current_user()
        current_time = datetime.datetime.now()
        a=""
        count=None
        if self.request.get("button")=="Update":
            #Below code used to update the edited tweets in myuser and mytweet folder
            dict={}
            myuser_key=ndb.Key('Myuser',user.email())
            myuser=myuser_key.get()
            t=self.request.get("t")
            if t in myuser.tweet_list:
                myuser.tweet_list.remove(self.request.get("t"))
            if t not in myuser.tweet_list:
                myuser.tweet_list.append(self.request.get("tweet1"))
            else:
                a="Already exist"
            myuser.put()
            mytweet=ndb.Key('Mytweet','default')
            mytweet=mytweet.get()
            for i in mytweet.query():
                if i.name==myuser.name:
                    if i.tweet==self.request.get("t"):
                        count=i.count
            if count!=None:
                mytweet=ndb.Key('Mytweet',myuser.name+" "+str(count))
                mytweet=mytweet.get()
                mytweet.tweet=self.request.get("tweet1")
                mytweet.put()
                a="Updated successfully"
            template_values= {'a':a}
            template=JINJA_ENVIRONMENT.get_template('edittweet.html')
            self.response.write(template.render(template_values))
        if self.request.get("button")=="Delete":
            #Below code used to delete  the tweets from myuser and mytweet folder
            t=self.request.get("twe")
            myuser_key=ndb.Key('Myuser',user.email())
            myuser=myuser_key.get()
            count=None
            a=""
            if t in myuser.tweet_list:
                myuser.tweet_list.remove(t)
                myuser.put()
            mytweet=ndb.Key('Mytweet','default')
            mytweet=mytweet.get()
            for i in mytweet.query():
                if i.name==myuser.name:
                    if i.tweet==t:
                        count=i.count
            if count!=None:
                mytweet=ndb.Key('Mytweet',myuser.name+" "+str(count))
                mytweet.delete()
                a="Deleted successfully"
            template_values= {'a':a}
            template=JINJA_ENVIRONMENT.get_template('edittweet.html')
            self.response.write(template.render(template_values))
