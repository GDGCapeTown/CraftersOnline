# Google Libraries
from google.appengine.ext import ndb
from google.appengine.api.logservice import logservice
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.api import images

# Python Libs
import datetime
import logging

#
# Event Details
# @author Johann du Toit
#
class Category(ndb.Model):
	name = ndb.StringProperty()
	lastupdated = ndb.DateTimeProperty(auto_now_add=True)
	created = ndb.DateTimeProperty(auto_now_add=True)

	#
	# Returns the event by it's slug
	#
	@staticmethod
	def get_for_menu():

		query_obj = Crafter.query()
		return query_obj.fetch()
