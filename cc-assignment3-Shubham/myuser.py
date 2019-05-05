from google.appengine.ext import ndb
class Myuser(ndb.Model):
    name=ndb.StringProperty()
    email=ndb.StringProperty()
    follower_list=ndb.StringProperty(repeated=True)
    followedby_list=ndb.StringProperty(repeated=True)
    tweet_list=ndb.StringProperty(repeated=True)
    description=ndb.StringProperty()
    time=ndb.DateTimeProperty()
    count=ndb.IntegerProperty(default=0)
