import os
import flask

IMAGES_DIRECTORY_NAME         = 'product-images'
PRODUCT_COVERS_DIRECTORY_NAME = 'covers'
PRODUCT_IMAGES_DIRECTORY_NAME = 'images'

STATIC_URL_PREFIX = 'https://api.wmiys.com/'


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


class UserImage:

    #------------------------------------------------------
    # Constructor
    #------------------------------------------------------
    def __init__(self, raw_img_file):
        self.img_file = raw_img_file

    #------------------------------------------------------
    # Returns the image file extension
    #------------------------------------------------------
    def getFileExtension(self):
        file_extension = os.path.splitext(self.img_file.filename)[1]
        return file_extension
    
    #------------------------------------------------------
    # Saves the image file to the server.
    #
    # parms:
    #   relative_directory_path - server directory to place the file
    #   new_file_name - change the name of the file on the server
    #
    # returns the filename of the local copy of the image
    #------------------------------------------------------
    def saveImageFile(self, relative_directory_path: str, new_file_name: str=None):
        if not new_file_name:
            new_file_name = self.img_file.filename

        self.img_file.save(os.path.join(relative_directory_path, new_file_name))     # save the image

        return new_file_name























    
