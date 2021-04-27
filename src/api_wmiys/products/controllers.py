import flask
from flask import Blueprint, jsonify, request
import api_wmiys.Security as Security
from api_wmiys.Security import requestGlobals
from api_wmiys.DB.DB import DB
from api_wmiys.products.Product import Product

products = Blueprint('products', __name__)


#------------------------------------------------------
# Fetch all of a user's products
#------------------------------------------------------
@products.route('', methods=['GET'])
@Security.login_required
def userProductsGet(user_id):
    # make sure the user is authorized
    if requestGlobals.client_id != user_id:
        flask.abort(403)

    userProducts = DB.getUserProducts(user_id)

    return jsonify(userProducts)

#------------------------------------------------------
# Create a new product
#------------------------------------------------------
@products.route('', methods=['POST'])
@Security.login_required
def userProductsPost(user_id):    
    # make sure the user is authorized
    if requestGlobals.client_id != user_id:
        flask.abort(403)

    newProduct = Product()

    # set the object properties from the fields in the request body
    # if the request body contains an invalid field, abort
    if not newProduct.setPropertyValuesFromDict(request.form.to_dict()):
        flask.abort(400)

    newProduct.user_id = user_id    # user_id is in the URI

    # set the image if one was uploaded
    if request.files.get('image'):
        newProduct.setImagePropertyFromImageFile(request.files.get('image'), Product.LOCAL_SERVER_COVER_PHOTO_DIRECTORY)
    
    newProduct.insert()

    return jsonify(newProduct.get())


#------------------------------------------------------
# Retrieve/update a single user product
#------------------------------------------------------
@products.route('<int:product_id>', methods=['GET', 'PUT'])
@Security.login_required
def productRequest(user_id, product_id):
    # load the product data
    product = Product(id=product_id)
    product.loadData()  # load the product data from the database

    if request.method == 'PUT':
        # the request body contained a field that does not belong in the product class
        if not product.setPropertyValuesFromDict(request.form.to_dict()):
            flask.abort(400)

        # set the image if one was uploaded
        if request.files.get('image'):
            product.setImagePropertyFromImageFile(request.files.get('image'), Product.LOCAL_SERVER_COVER_PHOTO_DIRECTORY)

        updateResult = product.update()

        return ('', 200)
    else:
        return jsonify(product.get())
