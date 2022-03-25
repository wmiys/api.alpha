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
from api_wmiys.common import BaseReturn

#-----------------------------------------------------
# POST the images for a product
# ----------------------------------------------------
def responses_POST(product_id) -> flask.Response:
    # get list of images provided in the request
    image_files = images.getRequestFiles()

    # no need to continue if there was no images provided in the request
    if not image_files or len(image_files) == 0:
        return responses.created()

    # save each file to the server and get the list of their file names
    save_result = _saveUploadedImages(image_files)

    if not save_result.successful:
        return responses.badRequest(str(save_result.error))

    # get the list of file names to save to the database
    file_names: list[str] = save_result.data


    # save each file name to the database
    


    return responses.created('created bitch')


#-----------------------------------------------------
# Given a list of FileStorage objects, save them to the server
#
# Returns a BaseReturn:
#     - the data attribute value will contain the list new file names (if successful)
#-----------------------------------------------------
def _saveUploadedImages(image_files: list[FileStorage]) -> BaseReturn:
    result = BaseReturn(successful=True)
    
    # get the destination path of the directory that holds all the product image files
    destination = images.getImagesDirectory()
    
    new_file_names = []

    # save the images and store each new file name
    for image in image_files:
        try:
            new_file_name = _saveImageFile(image, destination)   
            new_file_names.append(new_file_name)    
        
        except Exception as e:
            result.successful = False
            result.error = e
            return result

    result.data = new_file_names

    return result

#-----------------------------------------------------
# Generate a new, unique file name for the given FileStorage object
# Then, save it to given directory
#
# Args:
#     file_storage: the file to save
#     destination: the directory to save the file to
#
# Rerurns a the new, unique file name
#-----------------------------------------------------
def _saveImageFile(file_storage: FileStorage, destination: str) -> str:
    # create a unique file name for the image
    image_file    = images.ImageFile(file_storage)
    new_file_name = images.getUniqueFileName(image_file)

    # save it to the server
    image_file.save(
        destination = destination,
        file_name   = new_file_name,
    )

    return new_file_name







    



