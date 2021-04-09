import os


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























    