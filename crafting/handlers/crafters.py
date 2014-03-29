# Google Apis
from google.appengine.api import users
from google.appengine.api.logservice import logservice
from webapp2_extras import sessions
from google.appengine.ext import blobstore
from google.appengine.api.images import get_serving_url
from google.appengine.ext.webapp import blobstore_handlers

# Custom importing
from base import BaseHandler
import crafting.schema as schema

#
# Acts as the Frontpage when users are not signed in and the dashboard when they are.
# @author Johann du Toit
#
class CraftersHandler(BaseHandler):

    # Do the normal home render page
    def get(self):

        # Get the list for the homepage
        crafters = schema.Crafter.get_by_filter(None)

        # Locales
        locales = {

            "title": "Crafters",
            "crafters": crafters

        }

        # Render the template
        self.render('crafters.html', locales)

class EditCrafterImageHandler(BaseHandler, blobstore_handlers.BlobstoreUploadHandler):
    def get(self, id):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
        crafter = schema.Crafter.get_by_id(int(id))
        upload_url = blobstore.create_upload_url('/editcrafterimage')
        locales = { "crafter" : crafter, "upload_url" : upload_url}
        self.render('crafter_addimage.html', locales)
        
    def post(self):
        upload_files = self.get_uploads('image')
        blob_info = upload_files[0]
        crafter = schema.Crafter.get_by_id(int(self.request.get("crafter")))
        if crafter.image:
            blobstore.delete(crafter.image)
            crafter.image = None

        crafter.image = blob_info.key()
        crafter.put()

        self.redirect("/editcrafter/key=" + str(crafter.key.id()))