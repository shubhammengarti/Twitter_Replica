import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
from myuser import Myuser
from mytweet import Mytweet
from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.ext.webapp import blobstore_handlers
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)
class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        #Uploading image in blobstore and key in myuser datastore
        user = users.get_current_user()
        upload=self.get_uploads()[0]
        blobinfo=blobstore.BlobInfo(upload.key())
        filename=blobinfo.filename
        myuser_key=ndb.Key('Myuser',user.email())
        myuser=myuser_key.get()
        name=myuser.name
        count=myuser.count
        mytweet=ndb.Key('Mytweet',name+" "+str(count))
        mytweet=mytweet.get()
        mytweet.filenames=(filename)
        mytweet.blobs=(upload.key())
        mytweet.put()
        s="image uploaded"
        template_values= {'s':s}
        template=JINJA_ENVIRONMENT.get_template('tweetquery.html')
        self.response.write(template.render(template_values))
class ViewPhotoHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self):#Used to dispaly image for the id which was selected by user
        photo_key=self.request.get("id")
        if not blobstore.get(photo_key):
            self.error(404)
        else:
            self.send_blob(photo_key)
