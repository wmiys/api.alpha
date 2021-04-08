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
from Globals import Globals

# setup the flask application
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
CORS(app)

# setup the global variables container
requestGlobals = Globals(client_id=None)

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
        
        global requestGlobals
        requestGlobals.client_id = clientID

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
    new_user.email      = request.form.get('email') or None
    new_user.password   = request.form.get('password') or None
    new_user.name_first = request.form.get('name_first') or None
    new_user.name_last  = request.form.get('name_last') or None
    new_user.birth_date = request.form.get('birth_date') or None
    
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
    if requestGlobals.client_id != user_id:
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
# Fetch all of a user's products
#------------------------------------------------------
@app.route('/users/<int:user_id>/products', methods=['GET'])
@login_required
def userProductsGet(user_id):
    # make sure the user is authorized
    if requestGlobals.client_id != user_id:
        flask.abort(403)

    userProducts = DB.getUserProducts(user_id)

    return jsonify(userProducts)

#------------------------------------------------------
# Create a new product
#------------------------------------------------------
@app.route('/users/<int:user_id>/products', methods=['POST'])
@login_required
def userProductsPost(user_id):    
    # make sure the user is authorized
    if requestGlobals.client_id != user_id:
        flask.abort(403)

    newProduct                           = Product()
    newProduct.name                      = request.form.get('name') or None
    newProduct.description               = request.form.get('description') or None
    newProduct.product_categories_sub_id = request.form.get('product_categories_sub_id') or None
    newProduct.location_id               = request.form.get('location_id') or None
    newProduct.dropoff_distance          = request.form.get('dropoff_distance') or None
    newProduct.price_full                = request.form.get('price_full') or None
    newProduct.price_half                = request.form.get('price_half') or None
    newProduct.minimum_age               = request.form.get('minimum_age') or None
    newProduct.user_id                   = user_id

    # set the image if one was uploaded
    if request.files.get('image'):
        newProduct.setImagePropertyFromImageFile(request.files.get('image'), 'product-images')
    
    newProduct.insert()

    return jsonify(newProduct.get())


#------------------------------------------------------
# Retrieve/update a single user product
#------------------------------------------------------
@app.route('/users/<int:user_id>/products/<int:product_id>', methods=['GET', 'PUT'])
@login_required
def productRequest(user_id, product_id):
    # load the product data
    product = Product(id=product_id)
    product.loadData()  # load the product data from the database

    if request.method == 'PUT':
        # the request body contained a field that does not belong in the product class
        if not product.setPropertyValuesFromDict(request.form.to_dict()):
            flask.abort(400)
        
        updateResult = product.update()

        return ('', 200)
    else:
        return jsonify(product.get())

    




#************************************************************************************
#
#                           Main loop
#
#************************************************************************************
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

