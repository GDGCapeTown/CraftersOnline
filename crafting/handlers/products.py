# Google Apis
from google.appengine.api import users
from google.appengine.api.logservice import logservice
from webapp2_extras import sessions
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api.images import get_serving_url

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
        product_list = tuple()

        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))

        # Get the list for the homepage
        products = schema.Product.get_by_filter(None)

        for prod in products:
            if (prod.image):
                prod_image = get_serving_url(prod.image, 150)
            else:
                prod_image = None

            prod_tuple = (prod_image, prod)

            if len(product_list) != 0:
                product_list = product_list + (prod_tuple,)
            else:
                product_list = (prod_tuple,)

        # Locales
        locales = {
            'product_list': product_list
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
            if product.image:
                product_image = get_serving_url(product.image, 150)
            else:
                product_image = None
            locales = { "product" : product, 'crafters': crafters, 'categories': categories, 'product_image': product_image}
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
    def get(self, id):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))

        product = schema.Product.get_by_id(int(id))
        product.key.delete()
        self.redirect("/products")


class EditProductImageHandler(BaseHandler, blobstore_handlers.BlobstoreUploadHandler):
    def get(self, id):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))

        product = schema.Product.get_by_id(int(id))
        upload_url = blobstore.create_upload_url('/editproductimage')
        locales = { "product" : product, "upload_url" : upload_url}
        self.render('product_addimage.html', locales)
        
    def post(self):
        upload_files = self.get_uploads('image')
        blob_info = upload_files[0]
        product = schema.Product.get_by_id(int(self.request.get("product")))
        if product.image:
            blobstore.delete(product.image)
            product.image = None

        product.image = blob_info.key()
        product.put()

        self.redirect("/editproduct/key=" + str(product.key.id()))


