from __future__ import annotations
import flask
import os
from ..db import DB
from ..common import utilities, user_image

class ProductImage:
    LOCAL_SERVER_IMAGE_DIRECTORY_RELATIVE = 'product-images/images'

    #----------------------------------------------------------
    # Constructor
    #----------------------------------------------------------
    def __init__(self, newID=None, product_id=None, file_name=None, created_on=None):
        self.id = newID
        self.product_id = product_id
        self.file_name = file_name
        self.created_on = created_on

    #----------------------------------------------------------
    # Insert the product image into the database
    # 
    # Returns:
    #   bool: if it was successful or not
    #----------------------------------------------------------
    def insert(self) -> bool:
        if None in [self.product_id, self.file_name]:
            return False
        
        db = DB()
        db.connect()
        cursor = db.getCursor(False)

        sql = """
        INSERT INTO Product_Images 
        (product_id, file_name) VALUES
        (%s, %s)
        """

        parms = (self.product_id, self.file_name)

        cursor.execute(sql, parms)
        db.commit()
        self.id = cursor.lastrowid

        db.close()

        return True


    #----------------------------------------------------------
    # Loads the object properties values from the database
    # 
    # Returns:
    #   bool: if it was successful or not
    #----------------------------------------------------------
    def load(self) -> bool:
        if not self.id:
            return False

        db = DB()
        db.connect()
        cursor = db.getCursor(True)

        sql = """
        SELECT   *
        FROM     Product_Images pi
        WHERE    pi.id = %s
        LIMIT 1
        """

        parms = (self.id,)
        cursor.execute(sql, parms)
        imageData = cursor.fetchone()

        if not imageData:
            return False    # no records were found with the given ID

        self.product_id = imageData.get('product_id', None)
        self.file_name  = imageData.get('file_name', None)
        self.created_on = imageData.get('created_on', None)

        db.close()

        return True
    #----------------------------------------------------------
    # Takes a raw image file, saves it locally, and sets the image 
    # field in the database to the image file name as saved on the server.
    # 
    # Parms:
    #     newImageFile (object): the raw image file
    #     relative_image_directory_path (str): the folder name to save the image to    
    #----------------------------------------------------------
    def setImagePropertyFromImageFile(self, newImageFile: object, relative_image_directory_path: str):
        # remove the old image
        if self.file_name:
            os.remove(os.path.join(relative_image_directory_path, self.file_name))

        productImage = user_image.UserImage(newImageFile)
        newImageFileName = utilities.getUUID(True) + productImage.getFileExtension()
        self.file_name = productImage.saveImageFile(relative_image_directory_path, newImageFileName)


    #----------------------------------------------------------
    # Returns the object as a dict
    #----------------------------------------------------------
    def toDict(self) -> dict:
        return dict(
            id         = self.id,
            product_id = self.product_id,
            file_name  = self.file_name,
            created_on = self.created_on
        )


    #----------------------------------------------------------
    # Retrieve all of the product images for a product
    #
    # Parms:
    #   product_id (int): product id
    #
    # Returns a list:
    #   all of the product images that belong to a product
    #----------------------------------------------------------
    @staticmethod
    def getAll(product_id: int) -> list[dict]:
        images = ProductImage._getAllProductImageRecords(product_id)


        prefix = f'{flask.request.root_url}static/{ProductImage.LOCAL_SERVER_IMAGE_DIRECTORY_RELATIVE}/'

        # prepend the absolute url for each image file_name
        for image in images:
            image['file_name'] = prefix + image['file_name']

        return images

    #----------------------------------------------------------
    # Delete all the product images for a product
    #----------------------------------------------------------
    @staticmethod
    def deleteAll(product_id: int):
        ProductImage._deleteAllImageFiles(product_id)
        record_count = ProductImage._deleteAllImageDatabaseRecords(product_id)
        return record_count
    
    
    #----------------------------------------------------------
    # Deletes all the image files from storage that belong to the 
    # given product id.
    #----------------------------------------------------------
    @staticmethod
    def _deleteAllImageFiles(product_id: int):
        prefix = f'{flask.request.root_url}static/{ProductImage.LOCAL_SERVER_IMAGE_DIRECTORY_RELATIVE}/'

        for img in ProductImage._getAllProductImageRecords(product_id):
            os.remove(prefix + img.get('file_name'))

    #----------------------------------------------------------
    # Deletes all the image files from the database that belong 
    # to the given product id.
    #----------------------------------------------------------
    @staticmethod
    def _deleteAllImageDatabaseRecords(product_id: int) -> int:
        db = DB()
        db.connect()
        cursor = db.getCursor(True)

        sql = 'DELETE FROM Product_Images WHERE product_id = %s'

        parms = (product_id,)
        cursor.execute(sql, parms)
        db.commit()
        record_count = cursor.rowcount
        db.close()

        return record_count

    #----------------------------------------------------------
    # Retrieve all the product image database records that belong
    # to the given product.
    #----------------------------------------------------------
    @staticmethod
    def _getAllProductImageRecords(product_id: int) -> list[dict]:
        db = DB()
        db.connect()
        cursor = db.getCursor(True)

        sql = """
        SELECT   *
        FROM     Product_Images pi
        WHERE    pi.product_id = %s
        """

        parms = (product_id,)
        cursor.execute(sql, parms)
        images = cursor.fetchall()
        db.close()

        return images
        





        

