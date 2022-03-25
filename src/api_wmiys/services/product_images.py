"""
**********************************************************************************************
A product image represents a single additional image given to a product (not the cover photo).
Currently, the only way to update the images for a product is by first deleting all of them,
then you can post a list of new ones.
This will need to be updated soon.
**********************************************************************************************
"""
from __future__ import annotations


import flask
from werkzeug.datastructures import FileStorage
from wmiys_common import utilities
from api_wmiys.common import responses

from api_wmiys.common import images

#-----------------------------------------------------
# POST the images for a product
# ----------------------------------------------------
def responses_POST(product_id) -> flask.Response:
    
    # get list of images provided in the request
    image_files = _getImageFilesFromRequest()

    # no need to continue if there was no images provided in the request
    if not image_files or len(image_files) == 0:
        return responses.created()


    # now, we need to save each file to the server

    # get the destination path of the directory that holds all the product image files
    directory_path = images.getImagesDirectory()


    for image in image_files:
        userImage = images.ImageFile(image)

        extension = userImage.getFileExtension()

        new_file_name = f'{utilities.getUUID(True)}{extension}'

        print(new_file_name)




    return responses.created('created bitch')




# def _generateUniqueFileName(user_image)







# ----------------------------------------------------
# Get a list of the image files from the request 
# They are a FileStorage type
# ----------------------------------------------------
def _getImageFilesFromRequest() -> list[FileStorage]:
    files_dict = flask.request.files.to_dict(False)
    image_files = list(*files_dict.values())
    
    return image_files

    



