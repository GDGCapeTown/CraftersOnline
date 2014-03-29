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
class CrafterHandler(BaseHandler):

	# Do the normal home render page
	def get(self, crafter_id, crafter_name=False):
		crafter_obj = schema.Crafter.get_by_id( int(crafter_id) )
		if (crafter_obj != None):
			product_by_crafter = schema.Product.get_by_crafter( crafter_obj.key )

			# Get the newest products
			newest_products = schema.Product.get_all_by_crafter( crafter_obj.key )

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
