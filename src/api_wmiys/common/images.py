
from __future__ import annotations
import os
import flask


from werkzeug.datastructures import FileStorage
from wmiys_common.config_pairs import ApiUrls
from wmiys_common import utilities


IMAGES_DIRECTORY_NAME         = 'product-images'
PRODUCT_COVERS_DIRECTORY_NAME = 'covers'
PRODUCT_IMAGES_DIRECTORY_NAME = 'images'

STATIC_URL_PREFIX = f'{ApiUrls.PRODUCTION}/'


#----------------------------------------------------------
# Retrieve the absolute directory product covers path:
# C:\xampp\htdocs\files\api.wmiys\src\api_wmiys\static/product-images/covers/
#----------------------------------------------------------
def getCoverDirectory() -> str:
    return os.path.join(flask.current_app.static_folder, IMAGES_DIRECTORY_NAME, PRODUCT_COVERS_DIRECTORY_NAME)

#----------------------------------------------------------
# Retrieve the absolute directory product images path:
# C:\xampp\htdocs\files\api.wmiys\src\api_wmiys\static/product-images/images/
#----------------------------------------------------------
def getImagesDirectory() -> str:
    return os.path.join(flask.current_app.static_folder, IMAGES_DIRECTORY_NAME, PRODUCT_IMAGES_DIRECTORY_NAME)

#----------------------------------------------------------
# Retrieve the url for cover images
# http://api.wmiys.com/static/product-images/covers/
#----------------------------------------------------------
def getCoverUrl() -> str:
    return f'{STATIC_URL_PREFIX}static/{IMAGES_DIRECTORY_NAME}/{PRODUCT_COVERS_DIRECTORY_NAME}/'


#----------------------------------------------------------
# Retrieve the url for product images
# http://api.wmiys.com/static/product-images/images/
#----------------------------------------------------------
def getImagesUrl() -> str:
    return f'{STATIC_URL_PREFIX}static/{IMAGES_DIRECTORY_NAME}/{PRODUCT_IMAGES_DIRECTORY_NAME}/'


# ----------------------------------------------------
# Get a list of the image files (FileStorage) from the request 
# ----------------------------------------------------
def getRequestFiles() -> list[FileStorage]:
    files_dict = flask.request.files.to_dict(False)
    image_files = list(*files_dict.values()) or []
    
    return image_files

#------------------------------------------------------
# Generate a unique file name for the given ImageFile
# A unique file is a new UUID + the original file's extension
#------------------------------------------------------
def getUniqueFileName(image_file: ImageFile) -> str:
    extension = image_file.getFileExtension()
    prefix = utilities.getUUID(True)
    
    new_file_name = f'{prefix}{extension}'

    return new_file_name



class ImageFile:

    #------------------------------------------------------
    # Constructor
    #------------------------------------------------------
    def __init__(self, img_file: FileStorage):
        self.img_file = img_file

    #------------------------------------------------------
    # Returns the image file's file name extension
    #------------------------------------------------------
    def getFileExtension(self) -> str:
        # split the img_file's file name into 2 parts: name and extension
        file_name, file_extension = os.path.splitext(self.img_file.filename)

        return file_extension
    

    #------------------------------------------------------
    # Saves the image file to the server.
    #
    # Parms:
    #   directory_path - server directory to place the file
    #   new_file_name - change the name of the file on the server
    #
    # Returns the filename of the local copy of the image
    #------------------------------------------------------
    def save(self, destination: str, file_name: str=None) -> str:
        if not file_name:
            file_name = self.img_file.filename

        self.img_file.save(os.path.join(destination, file_name))     # save the image

        return file_name























    
