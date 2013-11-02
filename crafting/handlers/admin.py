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
class AdminHandler(BaseHandler):

	# Do the normal home render page
	def get(self):

		crafters = schema.Crafter.get_all()
		# Locales
		locales = {
			'crafters': crafters
		}

		# Render the template
		self.render('admin.html', locales)

class EditCrafterHandler(BaseHandler):
	def get(self, id):
		crafter = schema.Crafter.get_crafter(id)
		locales = { "crafter" : crafter}
		self.render('editcrafter.html', locales)
	def post(self, id):
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

class AddCrafterHandler(BaseHandler):
	def get(self):
		locales = {}
		self.render('editcrafter.html', locales)

