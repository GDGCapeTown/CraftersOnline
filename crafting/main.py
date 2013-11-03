#!/usr/bin/env python

# Python Libs
import os
import sys
import urllib

# Google Apis
import webapp2
from webapp2_extras import routes

from crafting.handlers.home import HomepageHandler
from crafting.handlers.product import ProductHandler
from crafting.handlers.auth import LoginHandler, LogoutHandler, PostLoginHandler, FailedLoginHandler
from crafting.handlers.crafters import CraftersHandler
from crafting.handlers.admin import AdminHandler, EditCrafterHandler, DeleteCrafterHandler
from crafting.handlers.about import AboutHandler
from crafting.handlers.crafter import CrafterHandler
from crafting.handlers.products import ProductsHandler, EditProductHandler, DeleteProductHandler
from crafting.handlers.category import CategoriesHandler, EditCategoryHandler, DeleteCategoryHandler
from crafting.handlers.user import UsersHandler, EditUserHandler, DeleteUserHandler

# General Config for our web application
config = {}
config['webapp2_extras.sessions'] = {

    'secret_key': 'secret_key_for_session_here'

}

# Setup with our little path fix trick
# sys.path.append(os.path.join(os.path.dirname(__file__), 'hubspot'))

# Startup our app with the routes we are
# going to configure now
app = webapp2.WSGIApplication([

	('/', HomepageHandler),
	('/login', LoginHandler),
	('/auth', PostLoginHandler),
	('/authfailed', FailedLoginHandler),
	('/logout', LogoutHandler),
	('/crafters', CraftersHandler),
	('/editcrafter/key=(.*)', EditCrafterHandler),
	('/deletecrafter/key=(.*)', DeleteCrafterHandler),
	('/products', ProductsHandler),
	('/editproduct/key=(.*)', EditProductHandler),
	('/deleteproduct/key=(.*)', DeleteProductHandler),
	('/categories', CategoriesHandler),
	('/editcategory/key=(.*)', EditCategoryHandler),
	('/deletecategory/key=(.*)', DeleteCategoryHandler),
	('/users', UsersHandler),
	('/edituser/key=(.*)', EditUserHandler),
	('/deleteuser/key=(.*)', DeleteUserHandler),
	('/about', AboutHandler),
	webapp2.Route(r'/p/<product_id:\d+>', handler=ProductHandler),
	webapp2.Route(r'/c/<crafter_id:\d+>', handler=CrafterHandler),
	webapp2.Route(r'/p/<product_id:\d+>/(\w+)', handler=ProductHandler),
	webapp2.Route(r'/c/<crafter_id:\d+>/(\w+)', handler=CrafterHandler),
	('/admin', AdminHandler),
	('/crafters.json', CraftersHandler),

], debug=True, config=config)
