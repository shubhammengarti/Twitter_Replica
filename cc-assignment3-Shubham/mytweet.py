from google.appengine.ext import ndb
class Mytweet(ndb.Model):
    email=ndb.StringProperty()
    tweet=ndb.StringProperty()
    time=ndb.DateTimeProperty()
    name=ndb.StringProperty()
    count=ndb.IntegerProperty(default=0)
    filenames=ndb.StringProperty()
    blobs=ndb.BlobKeyProperty()
