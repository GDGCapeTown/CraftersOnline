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
class ProductsHandler(BaseHandler):

	# Do the normal home render page
	def get(self):
		user = users.get_current_user()
		if not user:
			self.redirect(users.create_login_url(self.request.uri))

		# Get the list for the homepage
		products = schema.Product.get_by_filter(None)

		# Locales
		locales = {

			"title": "Welcome",
			'products': products

		}

		# Render the template
		self.render('products.html', locales)

class EditProductHandler(BaseHandler):
	def get(self, id):
		user = users.get_current_user()
		if not user:
			self.redirect(users.create_login_url(self.request.uri))

		crafters = schema.Crafter.get_all()
		categories = schema.Category.get_all()

		if id != "new":
			product = schema.Product.get_by_id(int(id))
			locales = { "product" : product, 'crafters': crafters, 'categories': categories}
		else:
			locales = {'crafters': crafters, 'categories': categories}

		self.render('editproduct.html', locales)


	def post(self, id):
		user = users.get_current_user()
		if not user:
			self.redirect(users.create_login_url(self.request.uri))

		request = self.request
		if id == "new":
			product = schema.Product()
		else:
			product = schema.Product.get_by_id(int(id))

		product.crafter = schema.Crafter.get_by_id(int(request.get("crafter"))).key;
		product.category = schema.Category.get_by_id(int(request.get("category"))).key;
		product.name = request.get("name");
		product.summary = request.get("summary");
		product.description = request.get("description");
		product.price = request.get("price");
		product.materials = request.get("materials");
		product.put()

		self.redirect("/products")


class DeleteProductHandler(BaseHandler):
	def get(self):
		user = users.get_current_user()
		if not user:
			self.redirect(users.create_login_url(self.request.uri))

		product = schema.Product.get_by_id(int(id))
		product.key.delete()
		self.redirect("/products")


