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
        crafters_list = tuple()
        # Get the list for the homepage
        crafters = schema.Crafter.get_for_homepage()
        title = "eThekwini Community Foundation"
        for crafter in crafters:
            crafter_prod_list = ()

            products = schema.Product.get_all_by_crafter(crafter.key)
            for product in products:
                if product.image:
                    prod_struct = (product.key.id(), get_serving_url(product.image, 150))
                    crafter_prod_list += (prod_struct,)
                    break

            crafter_struct = (crafter, crafter_prod_list)
            
            if len(crafters_list) == 0:
                crafters_list = (crafter_struct,)
            else:
                crafters_list = crafters_list + (crafter_struct,)

        products = schema.Product.get_newest_for_homepage()

        for product in products:
            if product.image:
                product_image_url = get_serving_url(product.image, 150)
                product.image_url = product_image_url
            else:
                product.image_url = "/img/product_180x180.jpg"


        # Locales
        locales = {
            "crafters_list": crafters_list,
            'products': products,
            'title' : title
        }

        # Render the template
        self.render('home.html', locales)
