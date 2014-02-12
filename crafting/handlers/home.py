# Google Apis
from google.appengine.api import users
from google.appengine.api.logservice import logservice
from webapp2_extras import sessions
from google.appengine.api.images import get_serving_url

# Custom importing
from base import BaseHandler
import crafting.schema as schema

#
# Acts as the Frontpage when users are not signed in and the dashboard when they are.
# @author Johann du Toit
#
class HomepageHandler(BaseHandler):

    # Do the normal home render page
    def get(self):

        crafters_list = ()
        # Get the list for the homepage
        crafters = schema.Crafter.get_for_homepage()
        for crafter in crafters:
            crafter_struct = (crafter,)
            products = schema.Product.get_all_by_crafter(crafter.key)
            for product in products:
                if product.image:
                    prod_struct = (product.key.id(), get_serving_url(product.image, 150))
                    if len(crafter_struct) == 1:
                        crafter_struct = crafter_struct, (prod_struct,)
                    else:
                        crafter_struct[1] = crafter_struct[1], prod_struct

            if not crafters_list:
                crafters_list = (crafter_struct,)
            else:
                crafters_list = crafters_list, crafter_struct

        print crafters_list
        products = schema.Product.get_newest_for_homepage()

        # Locales
        locales = {
            "crafters": crafters,
            'products': products
        }

        # Render the template
        self.render('home.html', locales)
