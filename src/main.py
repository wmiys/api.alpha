#************************************************************************************
#
#                                   API URL Routing Page
#
#************************************************************************************
import flask
from flask import Flask, jsonify, request, current_app
from flask_cors import CORS
from functools import wraps, update_wrapper
from markupsafe import escape
from User import User
from Login import Login
from DB import DB
from Product_Categories import ProductCategories
from Product import Product
from Utilities import Utilities
import os

app = Flask(__name__)
CORS(app)


g_client_id = None


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        # if user is not logged in, redirect to login page
        if not request.authorization:
            flask.abort(401)
        
        # make sure the user is authorized
        clientID = Login.getUserID(request.authorization.username, request.authorization.password)
        if clientID == None:
            flask.abort(401)
        
        global g_client_id
        g_client_id = clientID

        # finally call f. f() now haves access to g.user
        return f(*args, **kwargs)

    return wrap

#************************************************************************************
#
#                                   Index
#
#************************************************************************************
@app.route('/')
def home():    
    return 'Welcome to the WMIYS api!'

#************************************************************************************
#
#                                   Users
#
#************************************************************************************

#------------------------------------------------------
# Create new user
#------------------------------------------------------
@app.route('/users', methods=['POST'])
def users():
    new_user = User()

    # set the user properties
    new_user.email      = request.form['email']
    new_user.password   = request.form['password']
    new_user.name_first = request.form['name_first']
    new_user.name_last  = request.form['name_last']
    new_user.birth_date = request.form['birth_date']
    
    new_user.insert()
    new_user.fetch()

    return jsonify(new_user.__dict__)


#------------------------------------------------------
# Get a single user
#------------------------------------------------------
@app.route('/users/<int:user_id>', methods=['GET'])
@login_required
def user(user_id):
    # make sure the user is authorized
    if g_client_id != user_id:
        flask.abort(403)

    user = User(id=user_id)
    user.fetch()

    return jsonify(user.as_dict(return_password=False))


#************************************************************************************
#
#                                   Login
#
#************************************************************************************
@app.route('/login', methods=['GET'])
def login():
    userID = Login.getUserID(request.args['email'], request.args['password'])

    # make sure the user is authorized
    if userID == None:
        flask.abort(404)

    user = User(id=userID)
    user.fetch()
    return jsonify(user.as_dict(False))


#************************************************************************************
#
#                               Search
#
#************************************************************************************
#------------------------------------------------------
# Locations
#------------------------------------------------------
@app.route('/search/locations', methods=['GET'])
def searchLocations():
    query = request.args.get('q')

    # make sure the q argumrnt is set by the client
    if query == None:
        flask.abort(400)

    # if no per_page argument was given or it's gt 100, set it to the default (20)
    per_page = request.args.get('per_page')
    if per_page == None or int(per_page) > 100:
        per_page = 20
    
    search_results = DB.searchLocations(query=query, num_results=per_page)

    return jsonify(search_results)


#************************************************************************************
#
#                           Product Categories
#
#************************************************************************************
#------------------------------------------------------
# All categories
#------------------------------------------------------
@app.route('/product-categories', methods=['GET'])
def productCatgories():
    return jsonify(ProductCategories.getAll())

#------------------------------------------------------
# all major categories
#------------------------------------------------------
@app.route('/product-categories/major', methods=['GET'])
def productCategoriesMajors():
    return jsonify(ProductCategories.getMajors())

#------------------------------------------------------
# single major category
#------------------------------------------------------
@app.route('/product-categories/major/<int:major_id>', methods=['GET'])
def productCategoriesMajor(major_id):
    return jsonify(ProductCategories.getMajor(major_id))

#------------------------------------------------------
# all minor categories of a major
#------------------------------------------------------
@app.route('/product-categories/major/<int:major_id>/minor', methods=['GET'])
def productCategoriesMinors(major_id):
    return jsonify(ProductCategories.getMinors(major_id))

#------------------------------------------------------
# single minor category
#------------------------------------------------------
@app.route('/product-categories/major/<int:major_id>/minor/<int:minor_id>', methods=['GET'])
def productCategoriesMinor(major_id, minor_id):
    return jsonify(ProductCategories.getMinor(minor_id))

#------------------------------------------------------
# all sub categories of a minor
#------------------------------------------------------
@app.route('/product-categories/major/<int:major_id>/minor/<int:minor_id>/sub', methods=['GET'])
def productCategoriesSubs(major_id, minor_id):
    return jsonify(ProductCategories.getSubs(minor_id))

#------------------------------------------------------
# single sub category
#------------------------------------------------------
@app.route('/product-categories/major/<int:major_id>/minor/<int:minor_id>/sub/<int:sub_id>', methods=['GET'])
def productCategoriesSub(major_id, minor_id, sub_id):
    return jsonify(ProductCategories.getSub(sub_id))


#************************************************************************************
#
#                           Products
#
#************************************************************************************

#------------------------------------------------------
# Create a new product
#------------------------------------------------------
@app.route('/users/<int:user_id>/products', methods=['POST'])
@login_required
def userProductsPost(user_id):    
    # make sure the user is authorized
    if g_client_id != user_id:
        flask.abort(403)

    newProduct                           = Product()
    newProduct.name                      = str(request.form['name'])
    newProduct.description               = str(request.form['description'])
    newProduct.product_categories_sub_id = int(request.form['product_categories_sub_id'])
    newProduct.location_id               = int(request.form['location_id'])
    newProduct.price_full                = float(request.form['price_full'])
    newProduct.price_half                = float(request.form['price_half'])
    newProduct.user_id                   = int(user_id)

    # image
    if request.files.get('image') != None:
        raw_img = request.files['image']                                # get the image from the request
        file_ext = os.path.splitext(raw_img.filename)[1]                # get the extension
        img_file_name = str(Utilities.getUUID()) + file_ext             # merge the extension with a UUID
        raw_img.save(os.path.join('product-images', img_file_name))     # save the image
        newProduct.image = img_file_name
    else:
        newProduct.image = None

    newProduct.insert()

    return jsonify(newProduct.get())


#------------------------------------------------------
# Fetch all of a user's products
#------------------------------------------------------
@app.route('/users/<int:user_id>/products', methods=['GET'])
@login_required
def userProductsGet(user_id):
    # make sure the user is authorized
    if g_client_id != user_id:
        flask.abort(403)

    userProducts = DB.getUserProducts(user_id)

    return jsonify(userProducts)


#------------------------------------------------------
# Retrieve a single user product
#------------------------------------------------------
@app.route('/users/<int:user_id>/products/<int:product_id>', methods=['GET'])
@login_required
def product(user_id, product_id):
    product = Product(id=product_id)
    return jsonify(product.get())
