# Google Libraries
from google.appengine.ext import ndb
from google.appengine.api.logservice import logservice
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.api import images

# Python Libs
import datetime
import logging

# Allowed users who may login
# @author Johann du Toit
#
class AllowedUser(ndb.Model):

	name = ndb.StringProperty()
	email = ndb.StringProperty()

	created = ndb.DateTimeProperty(auto_now_add=True)
	lastupdated = ndb.DateTimeProperty(auto_now_add=True)

	@staticmethod
	def get_allowed_users():

		query_obj = AllowedUser.query()
		return query_obj.fetch()

