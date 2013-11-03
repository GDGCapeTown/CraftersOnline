# Google Apis
from google.appengine.api import users
from google.appengine.api.logservice import logservice
from webapp2_extras import sessions

# Custom importing
from base import BaseHandler
import crafting.schema as schema
from crafting.schema.alloweduser import AllowedUser

#
# Acts as the Frontpage when users are not signed in and the dashboard when they are.
# @author Johann du Toit
#

class UsersHandler(BaseHandler):
    # Do the normal home render page
    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))

        # Get the list for the homepage
        allowedusers = AllowedUser.get_allowed_users()

        # Locales
        locales = {

            "title": "Welcome",
            'users': allowedusers

        }

        # Render the template
        self.render('users.html', locales)


class EditUserHandler(BaseHandler):
    def get(self, id):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))

        if id != "new":
            alloweduser = AllowedUser.get_by_id(int(id))
            locales = { "user" : alloweduser}
        else:
            locales = {}

        self.render('edituser.html', locales)


    def post(self, id):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))

        request = self.request
        if id == "new":
            user = AllowedUser()
        else:
            user = AllowedUser.get_by_id(int(id))

        user.name = request.get("name");
        user.email = request.get("email");
        user.put()

        self.redirect("/users")


class DeleteUserHandler(BaseHandler):
    def get(self, id):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))

        user = AllowedUser.get_by_id(int(id))
        user.key.delete()
        self.redirect("/users")


