# Google Apis
from google.appengine.api import users
from google.appengine.api.logservice import logservice
from webapp2_extras import sessions
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api.images import get_serving_url


# Custom importing
from base import BaseHandler
import crafting.schema as schema

#
# Acts as the Frontpage when users are not signed in and the dashboard when they are.
# @author Johann du Toit
#
class CrafterHandler(BaseHandler):

	# Do the normal home render page
	def get(self, crafter_id, crafter_name=False):
		crafter_obj = schema.Crafter.get_by_id( int(crafter_id) )
		if (crafter_obj != None):
			if crafter_obj.image:
				crafter_img_url = get_serving_url(crafter_obj.image, 300)
				crafter_obj.image_url = crafter_img_url
			else:
				crafter_obj.image_url = "/img/product_300x300.jpg"
			product_by_crafter = schema.Product.get_by_crafter( crafter_obj.key )

			# Get the newest products
			newest_products = schema.Product.get_all_by_crafter( crafter_obj.key )

			for product in newest_products:
				if product.image:
					product_image_url = get_serving_url(product.image, 38)
					product.image_url_small = product_image_url
				else:
					product.image_url = "/img/crafter_38x38.jpg"

			for product in product_by_crafter:
				if product.image:
					product_image_url = get_serving_url(product.image, 140)
					product.image_url = product_image_url
				else:
					product.image_url = "/img/crafter_140x140.jpg"

			# Locales
			locales = {

				"title": crafter_obj.name,
				'crafter_obj': crafter_obj,
				'newest_products': newest_products,
				'crafter_products': product_by_crafter

			}

			# Render the template
			self.render('crafter.html', locales)

		else:

			# Redirect to homepage
			self.redirect('/')
