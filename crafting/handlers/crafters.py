# Google Apis
from google.appengine.api import users
from google.appengine.api.logservice import logservice
from webapp2_extras import sessions

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