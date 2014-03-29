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
class ProductHandler(BaseHandler):

	# Do the normal home render page
	def get(self, product_id, product_name=False):

		product_obj = schema.Product.get_by_id( int(product_id) )
		if product_obj != None:

			# get the crafter
			crafter_obj = None

			if product_obj.image:
				product_image_url = get_serving_url(product_obj.image, 300)
				product_obj.image_url = product_image_url
			else:
				product_obj.image_url = "/img/product_150x150.jpg"

			if product_obj.crafter != None:
				crafter_obj = product_obj.crafter.get()

			if crafter_obj != None:

				# Get other products by the crafter
				other_products_by_crafter = schema.Product.get_other_by_crafter( product_obj.key, crafter_obj.key, limit=4 )

				# Get the newest products
				newest_products = schema.Product.get_newest_for_homepage(limit=15)

				# Locales
				locales = {

					"title": product_obj.name,
					'product_obj': product_obj,
					'other_products_by_crafter': other_products_by_crafter,
					'newest_products': newest_products

				}

				# Render the template
				self.render('product.html', locales)

			else:

				# back to home !
				self.redirect('/')

		else:

			# Redirect to homepage
			self.redirect('/')
