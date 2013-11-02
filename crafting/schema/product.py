# Google Libraries
from google.appengine.ext import ndb
from google.appengine.api.logservice import logservice
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.api import images

from crafter import Crafter
from category import Category

# Python Libs
import datetime
import logging


class Product(ndb.Model):
	created = ndb.DateTimeProperty(auto_now_add=True)
	lastupdated = ndb.DateTimeProperty(auto_now_add=True)
	crafter = ndb.KeyProperty(kind=Crafter)
	category = ndb.KeyProperty(kind=Category)
	materials = ndb.StringProperty()
	name = ndb.StringProperty()
	summary = ndb.StringProperty()
	description = ndb.TextProperty()
	price = ndb.StringProperty()

	#
	# Returns the event by it's slug
	#
	@staticmethod
	def get_by_filter(category_obj, limit=10,offset=0):

		query_obj = Product.query()
		return query_obj.fetch(limit=10,offset=0)

	#
	# Returns the event by it's slug
	#
	@staticmethod
	def get_all_by_crafter(crafter_obj):

		query_obj = Product.query(Product.crafter == crafter_obj)
		return query_obj.fetch()

	#
	# Returns the event by it's slug
	#
	@staticmethod
	def get_by_crafter(crafter_obj, limit=10,offset=0):

		query_obj = Product.query(Product.crafter == crafter_obj)
		return query_obj.fetch(limit=10,offset=0)

	#
	# Returns the event by it's slug
	#
	@staticmethod
	def get_other_by_crafter(product_obj, crafter_obj, limit=10,offset=0):

		query_obj = Product.query(Product.crafter == crafter_obj, Product.key != product_obj)
		return query_obj.fetch(limit=10,offset=0)

	#
	# Returns the event by it's slug
	#
	@staticmethod
	def get_by_category(category_obj, limit=10,offset=0):

		query_obj = Product.query(Product.category.key == category_obj.key)
		return query_obj.fetch(limit=10,offset=0)

	#
	# Returns the event by it's slug
	#
	@staticmethod
	def get_newest_for_homepage(limit=6):

		query_obj = Product.query()
		return query_obj.fetch(limit=limit)

