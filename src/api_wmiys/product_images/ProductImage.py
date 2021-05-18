from api_wmiys.DB.DB import DB
from api_wmiys.common.UserImage import UserImage
from api_wmiys.common.Utilities import Utilities
import os

class ProductImage:

    
    LOCAL_SERVER_IMAGE_DIRECTORY = 'product-images/images'


    def __init__(self, newID=None, product_id=None, file_name=None, created_on=None):
        self.id = newID
        self.product_id = product_id
        self.file_name = file_name
        self.created_on = created_on


    def insert(self):
        if None in [self.product_id, self.file_name]:
            return False
        
        self.id = DB.insertProductImage(product_id=self.product_id, file_name=self.file_name)
        return True

    
    def load(self):
        if not self.id:
            return False

        imageData = DB.getProductImage(self.id)

        if not imageData:
            return False    # no records were found with the given ID


        self.product_id = imageData.product_id
        self.file_name = imageData.file_name
        self.created_on = imageData.created_on

        return True

    #------------------------------------------------------
    # takes an raw image file, saves it locally, and sets the image field in the database to the image file name as saved on the server
    #
    # parms:
    #   newImageFile - the raw image file
    #   relative_image_directory_path - the folder name to save the image to
    #------------------------------------------------------
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
        return dict(id=self.id, product_id=self.product_id, file_name=self.file_name, created_on=self.created_on)


    @staticmethod
    def getAll(product_id: int):
        images = DB.getProductImages(product_id)
        return images

        

