from api_wmiys.DB.DB import DB
from api_wmiys.common.UserImage import UserImage
from api_wmiys.common.Utilities import Utilities
import os

class ProductImage:

    
    # LOCAL_SERVER_IMAGE_DIRECTORY = 'product-images/images'

    LOCAL_SERVER_IMAGE_DIRECTORY = "http://10.0.0.82/files/api.wmiys/src/product-images/images"
    LOCAL_SERVER_IMAGE_DIRECTORY_RELATIVE = 'product-images/images'


    def __init__(self, newID=None, product_id=None, file_name=None, created_on=None):
        self.id = newID
        self.product_id = product_id
        self.file_name = file_name
        self.created_on = created_on


    def insert(self):
        """Insert the product image into the database

        Returns:
            bool: if it was successful or not
        """
        if None in [self.product_id, self.file_name]:
            return False
        
        self.id = DB.insertProductImage(product_id=self.product_id, file_name=self.file_name)
        return True

    
    def load(self):
        """Loads the object properties values from the database

        Returns:
            bool: whether or not the load was successful.
        """
        if not self.id:
            return False

        imageData = DB.getProductImage(self.id)

        if not imageData:
            return False    # no records were found with the given ID


        self.product_id = imageData.product_id
        self.file_name = imageData.file_name
        self.created_on = imageData.created_on

        return True


    def setImagePropertyFromImageFile(self, newImageFile: object, relative_image_directory_path: str):
        """Takes a raw image file, saves it locally, and sets the image field in the database to the image file name as saved on the server.

        ---
        Args:
        
        - newImageFile (object): the raw image file
        - relative_image_directory_path (str): the folder name to save the image to
        """


        # remove the old image
        if self.file_name:
            os.remove(os.path.join(relative_image_directory_path, self.file_name))

        productImage = UserImage(newImageFile)
        newImageFileName = Utilities.getUUID(True) + productImage.getFileExtension()
        self.file_name = productImage.saveImageFile(relative_image_directory_path, newImageFileName)

    def toDict(self):
        """Returns the object as a dict
        """
        return dict(id=self.id, product_id=self.product_id, file_name=self.file_name, created_on=self.created_on)


    @staticmethod
    def getAll(product_id: int):
        """Retrieve all of the product images for a product

        Args:
            product_id (int): product id

        Returns:
            list: all of the product images that belong to a product
        """
        images = DB.getProductImages(product_id)
        

        # prepend the absolute url for each image file_name
        result = []
        for img in images:
            imgDict = img._asdict()
            imgDict['file_name'] = ProductImage.LOCAL_SERVER_IMAGE_DIRECTORY + '/' + imgDict['file_name']
            result.append(imgDict)

        return result

    @staticmethod
    def deleteAll(product_id: int):
        images = DB.getProductImages(product_id)

        for img in images:
            os.remove(ProductImage.LOCAL_SERVER_IMAGE_DIRECTORY_RELATIVE + '/' + img.file_name)

        return DB.deleteProductImages(product_id)

        

        





        

