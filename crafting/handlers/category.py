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

class CategoriesHandler(BaseHandler):
    # Do the normal home render page
    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))

        # Get the list for the homepage
        categories = schema.Category.get_all()

        # Locales
        locales = {

            "title": "Categories",
            'categories': categories

        }

        # Render the template
        self.render('categories.html', locales)


class EditCategoryHandler(BaseHandler):
    def get(self, id):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))

        if id != "new":
            category = schema.Category.get_by_id(int(id))
            locales = { "category" : category}
        else:
            locales = {}

        self.render('editcategory.html', locales)

    def post(self, id):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))

        request = self.request
        if id == "new":
            category = schema.Category()
        else:
            category = schema.Category.get_by_id(int(id))

        category.name = request.get('name')
        category.put()

        self.redirect("/categories")


class DeleteCategoryHandler(BaseHandler):
    def get(self, id):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))

        category = schema.Category.get_by_id(int(id))
        category.key.delete()
        self.redirect("/categories")


