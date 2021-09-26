#************************************************************************************
#
#                           Product Class
#
#************************************************************************************
from __future__ import annotations
import os
from typing import Optional
from ..db import DB
from ..common import utilities
from .. import common

class Product:

    LOCAL_SERVER_COVER_PHOTO_DIRECTORY = 'product-images/covers'
    LOCAL_SERVER_COVER_PHOTO_DIRECTORY_ABS = "http://10.0.0.82/files/api.wmiys/src/product-images/covers"
    
    #------------------------------------------------------
    # Constructor
    #------------------------------------------------------
    def __init__(self, id=None, user_id=None, name=None, description=None, product_categories_sub_id=None, location_id=None, dropoff_distance=None, price_full=None, price_half=None, image=None, minimum_age=None, created_on=None):
        self.id                        = id
        self.user_id                   = user_id
        self.name                      = name
        self.description               = description
        self.product_categories_sub_id = product_categories_sub_id
        self.location_id               = location_id
        self.dropoff_distance          = dropoff_distance
        self.price_full                = price_full
        self.price_half                = price_half
        self.image                     = image
        self.minimum_age               = minimum_age
        self.created_on                = created_on
    
    #------------------------------------------------------
    # Insert the product into the database
    #------------------------------------------------------
    def insert(self):
        db = DB()
        db.connect()
        cursor = db.getCursor(False)

        sql = """
        INSERT INTO Products
        (user_id, name, description, product_categories_sub_id, location_id, dropoff_distance, price_full, price_half, image, minimum_age) VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        parms = (
            self.user_id, self.name, self.description, 
            self.product_categories_sub_id, self.location_id, self.dropoff_distance, 
            self.price_full, self.price_half, self.image, 
            self.minimum_age
        )
    
        cursor.execute(sql, parms)
        db.commit()

        self.id = cursor.lastrowid

        db.close()

    
    #------------------------------------------------------
    # Update the product database record
    #------------------------------------------------------
    def update(self) -> int:
        db = DB()
        db.connect()
        cursor = db.getCursor(False)

        sql = """
        UPDATE Products
        SET
            name                      = %s,
            description               = %s,
            product_categories_sub_id = %s,
            location_id               = %s,
            dropoff_distance          = %s,
            price_full                = %s,
            price_half                = %s,
            image                     = %s,
            minimum_age               = %s
        WHERE 
            id = %s
        """

        parms = (
            self.name,          self.description,         self.product_categories_sub_id,
            self.location_id,   self.dropoff_distance,    self.price_full,
            self.price_half,    self.image,               self.minimum_age
        )

        try:
            cursor.execute(sql, parms)
            db.commit()
            row_count = cursor.rowcount
        except:
            row_count = -1
        finally:
            db.close()

        return row_count

    #------------------------------------------------------
    # Loads the product data fields from the database
    #------------------------------------------------------
    def loadData(self):
        # make sure the product id is set
        if self.id == None:
            return
        
        db_row = self._getProductDbRecordSet()

        self.user_id                   = db_row.get('user_id', None)
        self.name                      = db_row.get('name', None)
        self.description               = db_row.get('description', None)
        self.product_categories_sub_id = db_row.get('product_categories_sub_id', None)
        self.location_id               = db_row.get('location_id', None)
        self.dropoff_distance          = db_row.get('dropoff_distance', None)
        self.price_full                = db_row.get('price_full', None)
        self.price_half                = db_row.get('price_half', None)
        self.image                     = db_row.get('image', None)
        self.minimum_age               = db_row.get('minimum_age', None)
        self.created_on                = db_row.get('created_on', None)

    #------------------------------------------------------
    # Fetch the product data from the database
    #------------------------------------------------------
    def get(self) -> dict:
        # make sure the product id is set
        if self.id == None:
            return None

        product_rs = self._getProductDbRecordSet()

        # prepend the absolute url to the image value
        if product_rs['image']:
            product_rs['image'] = Product.LOCAL_SERVER_COVER_PHOTO_DIRECTORY_ABS + '/' + product_rs['image']

        return product_rs

    #------------------------------------------------------
    # Get the object's record set from the database
    #------------------------------------------------------
    def _getProductDbRecordSet(self) -> dict:
        db = DB()
        db.connect()
        cursor = db.getCursor(True)

        sql = """
        SELECT  *
        FROM    View_Products p
        WHERE   p.id = %s
        GROUP   BY p.id
        LIMIT   1 
        """

        parms = (self.id,)

        cursor.execute(sql, parms)
        record_set = cursor.fetchone()
        db.close()

        return record_set
    
    #------------------------------------------------------
    # Set's the object's properties given a dict
    #
    # Returns boolean:
    #   false: the dict contained an extraneous field
    #   true: properties were successfully changed
    #------------------------------------------------------
    def setPropertyValuesFromDict(self, newPropertyValues: dict):
        # validate the field before changing the object property
        if not utilities.areAllKeysValidProperties(newPropertyValues, self):
            return False

        # set the object properties
        for key in newPropertyValues:
            if newPropertyValues[key]:
                setattr(self, key, newPropertyValues[key])
            else:
                setattr(self, key, None)
            
        return True
    
    #------------------------------------------------------
    # takes an raw image file, saves it locally, and sets the image field in the database to the image file name as saved on the server
    #
    # parms:
    #   newImageFile - the raw image file
    #   relative_image_directory_path - the folder name to save the image to
    #------------------------------------------------------
    def setImagePropertyFromImageFile(self, newImageFile: object, relative_image_directory_path: str):
        # remove the old image
        if self.image:
            os.remove(os.path.join(relative_image_directory_path, self.image))

        productImage = common.UserImage(newImageFile)
        newImageFileName = utilities.getUUID(True) + productImage.getFileExtension()
        self.image = productImage.saveImageFile(relative_image_directory_path, newImageFileName)


    #------------------------------------------------------
    # Get all the products owned by the specified user.
    #
    # Parms:
    #   user_id - the user's id
    #
    # Returns: list of product dictionaries
    #------------------------------------------------------
    @staticmethod
    def getAll(user_id: int) -> list[dict]:
        products = Product._getAllUserProductRecords(user_id)

        # prepend the absolute image file path to each image field, if one exists
        for product in products:
            if product['image']:
                product['image'] = Product.LOCAL_SERVER_COVER_PHOTO_DIRECTORY_ABS + '/' + product['image']

        return products


    #------------------------------------------------------
    # Get all the products owned by the specified user.
    #
    # Parms:
    #   user_id - the user's id
    #
    # Returns: list of product dictionaries
    #------------------------------------------------------
    @staticmethod
    def _getAllUserProductRecords(user_id: int) -> list[dict]:
        db = DB()
        db.connect()
        cursor = db.getCursor(True)

        sql = """
        SELECT  *
        FROM    View_Products p
        WHERE   p.user_id = %s
        GROUP   BY p.id
        ORDER   BY p.name ASC
        """

        parms = (user_id,)

        cursor.execute(sql, parms)
        product_records = cursor.fetchall()

        return product_records



            

        
        








