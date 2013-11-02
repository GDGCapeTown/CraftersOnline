# Google Apis
from google.appengine.api import users
from google.appengine.api.logservice import logservice
from webapp2_extras import sessions

# Libraries
import webapp2

from crafting.schema.alloweduser import AllowedUser 

#
# Login with your Google Account
# @author Johann du Toit
#
class LoginHandler(webapp2.RequestHandler):
	def get(self):

		# Normal Google User Account
		self.redirect(users.create_login_url('/auth'))


#
# Logout from your Google Account
# @author Johann du Toit
#
class LogoutHandler(webapp2.RequestHandler):
	def get(self):

		# Send to logout
		self.redirect(users.create_logout_url('/'))


class PostLoginHandler(webapp2.RequestHandler):
    def get(self):

        # Normal Google User Account
        user = users.get_current_user()

        user_objs = AllowedUser.get_allowed_users()
        for dbuser in user_objs:
            if dbuser.email == user.email():
                self.redirect('/')
                return

        if len(user_objs) > 0:
            self.redirect(users.create_logout_url('/authfailed'))
        else:
            self.redirect('/')


class FailedLoginHandler(webapp2.RequestHandler):
    def get(self):

        template = jinja_environment.get_template('failedlogin.html')
        self.response.out.write(template.render())

