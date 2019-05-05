import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
from myuser import Myuser
from tweet import Tweet
from edit import Edit
from follower import Follower
from followed import Followed
from edittweet import Edittweet
from google.appengine.ext import blobstore
from uploadhandler import UploadHandler
from uploadhandler import ViewPhotoHandler
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)
class Mainpage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type']= 'text/html'
        url = ''
        url_string = ''
        welcome = 'Welcome'
        myuser = None
        user = users.get_current_user()
        count=0
        count1=0
        count2=0
        a=""
        list=[]
        dict={}
        dict1={}
        list1=[]
        bool=False
        dict2={}
        img=""
        if user:
            url=users.create_logout_url(self.request.uri)
            url_string='logout'
            myuser_key=ndb.Key('Myuser',user.email())
            myuser=myuser_key.get()
            welcome = 'Welcome Back'
            if myuser==None:
                welcome="welcome"
                myuser=Myuser(id=user.email())
                myuser.put()
                myuser.email=user.email()
                myuser.put()
            elif myuser!=None:
                #count has been taken for front end dispaly
                if myuser.tweet_list !=None:
                    count=len(myuser.tweet_list)
                if myuser.follower_list!=None:
                    count1=len(myuser.follower_list)
                if myuser.followedby_list!=None:
                    count2=len(myuser.followedby_list)
                else:
                    a="Not available"
                #Below code is used to dispaly last 50 tweets
                list=myuser.follower_list
                list.append(myuser.name)
                tweet=ndb.Key('Mytweet',"default")
                tweet=tweet.get()
                l3=[]
                if tweet!=None:
                    for i1 in list:
                        for i in tweet.query():
                            if i.name==i1:
                                dict[i.time]=i.name
                                dict1[i.time]=i.tweet
                                l3.append(i.time)
                                dict2[i.time]=i.blobs
                                bool=True
                    if count>50:
                        list1=sorted(l3,reverse=True)
                        list1=list1[1:50]
                        st="Tweets are available below"
                    else:
                        list1=sorted(l3,reverse=True)
                        st="Tweets are available below"
        else:
            url=users.create_login_url(self.request.uri)
            url_string='login'
        template_values= {'url':url,'url_string':url_string,'user':user,'welcome':welcome,'myuser':myuser,'count':count,'count1':count1,'count2':count2,
        'dict':dict,'dict1':dict1,'list1':list1,'bool':bool,'dict2':dict2}
        template=JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))
    def post(self):
        self.response.headers['Content-Type']= 'text/html'
        user = users.get_current_user()
        a=""
        if self.request.get("button")=="submit":
            #Storing userdetails like name
            myuser_key=ndb.Key('Myuser',user.email())
            myuser=myuser_key.get()
            myuser.name=self.request.get("username")
            myuser.description=self.request.get("description")
            myuser.put()
            a="User Accounts Updated"
            template_values= {'a':a}
            template=JINJA_ENVIRONMENT.get_template('create.html')
            self.response.write(template.render(template_values))
        if self.request.get("button")=="search":
            #Below code used to search users in myuser datastore and help us to display userdetails.
            name=""
            description=""
            l=[]
            l1=[]
            l2=[]
            l3=[]
            dict={}
            dict1={}
            list2=[]
            Bool=True
            Bool1=True
            a=""
            myuser_key=ndb.Key('Myuser',user.email())
            myuser1=myuser_key.get()
            cname=myuser1.name
            myuser=myuser1.query()
            user_name=myuser1.name
            count=0
            dict3=[]
            st=""
            if self.request.get("User")==cname:
                a="Cannot search your user"
            else:
                for i in myuser:
                    if i.name==self.request.get("User"):
                        name=i.name
                        description=i.description
                        l=i.follower_list
                        count=i.count
                        Bool=False
                        email=i.email
                        t=ndb.Key('Mytweet',"default")
                        t=t.get()
                        if t!=None:
                            t=t.query()
                            for i1 in t:
                                if i1.email==email and i1.tweet!=None and i1.time!=None:
                                    dict[i1.count]=i1.tweet
                                    l2.append(i1.count)
                                    dict1[i1.count]=((i1.time).strftime("%b %d %Y %H:%M:%S"))
                for i in myuser:
                    if i.name==user_name:
                        for l in i.follower_list:
                            if l==self.request.get("User"):
                                Bool1=False
                if count>50:
                    l2=l2.sort(reverse=True)
                    list2=l2[1:50]
                    st="Tweets are available "
                else:
                    list2=l2.sort(reverse=True)
                    st="Tweets are available "
                if Bool==True:
                    a="No user available"
            template_values= {'name':name,'description':description,'l':l,'a':a,'Bool':Bool,'l3':l3,'l2':l2,'list2':list2,'dict':dict,'dict1':dict1,'Bool1':Bool1,'st':st}
            template=JINJA_ENVIRONMENT.get_template('user.html')
            self.response.write(template.render(template_values))
        if self.request.get("button")=="Follow":
            #Used to add the user in the followerlist of user
            myuser_key=ndb.Key('Myuser',user.email())
            myuser=myuser_key.get()
            followedby_username=myuser.name
            name=self.request.get("name")
            s1=""
            l=myuser.follower_list
            if name not in l:
                myuser.follower_list.append(name)
                myuser.put()
            else:
                s1="User already there"
            myuser=myuser.query()
            email_user=""
            for i in myuser:
                if i.name==self.request.get("name"):
                    email_user=i.email
            myuser_key=ndb.Key('Myuser',email_user)
            myuser=myuser_key.get()
            l1=myuser.followedby_list
            if followedby_username not in l1:
                myuser.followedby_list.append(followedby_username)
                s="User has been added in follower list success"
                myuser.put()
            else:
                s="User already in the list"
            template_values= {'s':s}
            template=JINJA_ENVIRONMENT.get_template('tweetquery.html')
            self.response.write(template.render(template_values))
        if self.request.get("button")=="UnFollow":
            #Removing user from follower list of logged user and followedby list
            myuser_key=ndb.Key('Myuser',user.email())
            myuser=myuser_key.get()
            followedby_username=myuser.name
            for i in myuser.follower_list:
                if i==self.request.get("name"):
                    myuser.follower_list.remove(self.request.get("name"))
                    myuser.put()
            email_user=""
            for i in myuser.query():
                if i.name==self.request.get("name"):
                    email_user=i.email
            for i in myuser.query():
                if i.name==self.request.get("name"):
                    email_user=i.email
            myuser_key=ndb.Key('Myuser',email_user)
            myuser=myuser_key.get()
            l1=myuser.followedby_list
            if followedby_username in l1:
                myuser.followedby_list.remove(followedby_username)
                s="User has been remove in followers"
                myuser.put()
            else:
                s="User already in the list"
            template_values= {'s':s}
            template=JINJA_ENVIRONMENT.get_template('tweetquery.html')
            self.response.write(template.render(template_values))
        if self.request.get("button")=="enter":
            #I have remove punctuations from the tweets like preprocessing and compared the searching tweet with the tweets in datastore.If the tweets are
            #matching,i am diaplaying those tweets in the front end.
            tweet=self.request.get("tweet1")
            s1=""
            punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
            for char in tweet:
                if char in punctuations:
                    tweet=tweet.replace(char,"")
            final_tweet=tweet.split(" ")
            for i in final_tweet:
                if i=="" or i==None:
                    final_tweet.remove(i)
            user=users.get_current_user()
            myuser_key=ndb.Key('Myuser',user.email())
            myuser=myuser_key.get()
            welcome = 'Welcome Back'
            t=ndb.Key('Mytweet',"default")
            t=t.get()
            dict={}
            lists1=[]
            dict2={}
            dict1={}
            dict3={}
            s=""
            lp=[]
            if t!=None:
                t=t.query()
                for i in t:
                    if i.tweet!=None:
                        twe=i.tweet
                        twee=twe.split(" ")
                        length=len(final_tweet)
                        count=0
                        l=[]
                        for k in twee:
                            for j in final_tweet:
                                if k==j and j not in l:
                                    count+=1
                                    l.append(j)
                                    s="Tweets available below related to search"
                        if count==length and i.time not in lists1:
                            lp.append(twe)
                            dict[i.time]=twe
                            dict1[i.time]=i.name
                            dict3[i.time]=i.blobs
                            lists1.append(i.time)
                            dict2[i.time]=((i.time).strftime("%b %d %Y %H:%M:%S"))
            else:
                s="No tweet available"
            template_values= {'dict':dict,'dict1':dict1,'lists1':lists1,'user':user,'welcome':welcome,'dict2':dict2,'s':s,'dict3':dict3}
            template=JINJA_ENVIRONMENT.get_template('tweetquery.html')
            self.response.write(template.render(template_values))











app = webapp2.WSGIApplication([('/',Mainpage),('/tweet',Tweet),('/edit',Edit),('/follower',Follower),('/upload', UploadHandler),('/view',ViewPhotoHandler),('/followed',Followed),('/edittweet',Edittweet),],debug=True)
