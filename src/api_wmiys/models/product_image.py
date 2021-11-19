"""
**********************************************************************************************
A product image represents a single additional image given to a product (not the cover photo).

Currently, the only way to update the images for a product is by first deleting all of them,
then you can post a list of new ones.

This will need to be updated soon.
**********************************************************************************************
"""

from __future__ import annotations
import os
from wmiys_common import utilities
from ..db import DB
from ..common import UserImage, user_image


#----------------------------------------------------------
# Retrieve all of the product images for a product
#
# Parms:
#   product_id (int): product id
#
# Returns a list:
#   all of the product images that belong to a product
#----------------------------------------------------------
def getAll(product_id: int) -> list[dict]:
    images = _getAllProductImageRecords(product_id)

    prefix = user_image.getImagesUrl()

    # prepend the absolute url for each image file_name
    for image in images:
        image['file_name'] = prefix + image['file_name']

    return images

#----------------------------------------------------------
# Delete all the product images for a product
#----------------------------------------------------------
def deleteAll(product_id: int):
    _deleteAllImageFiles(product_id)
    record_count = _deleteAllImageDatabaseRecords(product_id)
    return record_count


#----------------------------------------------------------
# Deletes all the image files from storage that belong to the 
# given product id.
#----------------------------------------------------------
def _deleteAllImageFiles(product_id: int):
    prefix = user_image.getImagesDirectory()

    for img in _getAllProductImageRecords(product_id):
        img_file_path = os.path.join(prefix, img.get('file_name'))
        os.remove(img_file_path)

#----------------------------------------------------------
# Deletes all the image files from the database that belong 
# to the given product id.
#----------------------------------------------------------
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

class ProductImage:

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
    def setImagePropertyFromImageFile(self, newImageFile: object, image_directory_path: str):
        # remove the old image
        if self.file_name:
            os.remove(os.path.join(image_directory_path, self.file_name))

        image_file = UserImage(newImageFile)
        
        # create a unique name for the product image (GUID + it's original extension)
        new_image_file_name = utilities.getUUID(True) + image_file.getFileExtension()

        # now save the file to the server
        self.file_name = image_file.saveImageFile(image_directory_path, new_image_file_name)


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

        





        

