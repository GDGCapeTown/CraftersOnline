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
class AdminHandler(BaseHandler):

	# Do the normal home render page
	def get(self):
		title = "Admin"
		user = users.get_current_user()
		if not user:
			self.redirect(users.create_login_url(self.request.uri))

		crafters = schema.Crafter.get_all()
		# Locales
		locales = {
			'crafters': crafters,
			'title' : title
		}

		# Render the template
		self.render('admin.html', locales)

class EditCrafterHandler(BaseHandler):
	def get(self, id):
		user = users.get_current_user()
		if not user:
			self.redirect(users.create_login_url(self.request.uri))

		if id != "new":
			
			crafter = schema.Crafter.get_crafter(id)
			if crafter.image:
				crafter_image = get_serving_url(crafter.image, 150)
			else:
				crafter_image = None
			locales = { "crafter" : crafter,
						"crafter_image" : crafter_image}
		else:
			locales = {}

		self.render('editcrafter.html', locales)

	def post(self, id):
		user = users.get_current_user()
		if not user:
			self.redirect(users.create_login_url(self.request.uri))

		request = self.request
		if id == "new":
			crafter = schema.Crafter()
		else:
			crafter = schema.Crafter.get_crafter(id)

		crafter.name = request.get('name')
		crafter.surname = request.get('surname')
		crafter.about = request.get('about')
		crafter.cell_number = request.get('cell_number	')
		crafter.email = request.get('email')
		crafter.website = request.get('website')
		crafter.organization = request.get('organization')
		crafter.province = request.get('province')
		crafter.suburb = request.get('suburb')
		crafter.town = request.get('town')
		crafter.put()

		self.redirect("/admin")

class DeleteCrafterHandler(BaseHandler):
	def get(self, id):
		user = users.get_current_user()
		if not user:
			self.redirect(users.create_login_url(self.request.uri))

		crafter = schema.Crafter.get_crafter(id)
		crafter.key.delete()
		self.redirect("/admin")

		
