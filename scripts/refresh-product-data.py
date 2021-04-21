"""
This script refreshes all of the database data and product images
"""

from PIL import Image
import os, sys
from Utilities import Utilities
import shutil
import mysql.connector

# constants
PATH_PHOTO_DUMP = 'C:\\Users\\1\\Documents\\photo-dump'
PATH_RAW_DATA = 'raw-product-data.json'
PATH_GOOD_IMAGES = 'good-images'
PATH_API_IMAGES = 'C:\\xampp\\htdocs\\files\\api.wmiys\\src\\product-images'
PATH_MYSQL_INFO = '.mysql-info.json'


# return a list of files in a directory
def getFilesListInDirectory(path, includePath=False):
    images = list(os.listdir(path))

    if not includePath:
        return images
    
    # append the path if flag is specified
    result = list(map(lambda x: "{}\\{}".format(path, x), images))

    return result

def refreshImages():
    imageNamesAll = getFilesListInDirectory(PATH_PHOTO_DUMP, True)
    largeImageNames = []

    for imgRaw in imageNamesAll:
        # ignore any file that isn't a jpg
        parts = imgRaw.split('.')
        if parts[1] != 'jpg':
            continue

        imgW, imgH = Image.open(imgRaw).size

        # get file if its large enough
        if imgW >= 1200 and imgH >= 800:
            largeImageNames.append(imgRaw)

    productData = Utilities.getJsonData(PATH_RAW_DATA)

    # delete all the images in the api image directory
    for img in os.listdir(PATH_API_IMAGES):
        os.remove(os.path.join(PATH_API_IMAGES, img))

    # copy the images from the dump into the api image directory
    for x in range(len(productData)):
        oldFileName = largeImageNames[x]
        newFileName = os.path.join(PATH_API_IMAGES, productData[x]['image'])
        shutil.copyfile(oldFileName, newFileName)



refreshImages()


# initialize database connection
configData = Utilities.getJsonData(PATH_MYSQL_INFO)
mydb = mysql.connector.connect(user=configData['user'], password=configData['passwd'], host=configData['host'], database=configData['database'])

# connect to database
mycursor = mydb.cursor()

# delete all records in products tables
sqlStmts = []
sql = 'DELETE FROM {}'
sqlStmts.append(sql.format('Product_Availability'))
sqlStmts.append(sql.format('Products'))

for stmt in sqlStmts:
    mycursor.execute(stmt)
    

# reset the auto_increments to start at 1
sqlStmts = []
sql = 'ALTER TABLE {} AUTO_INCREMENT = 1'
sqlStmts.append(sql.format('Product_Availability'))
sqlStmts.append(sql.format('Products'))

for stmt in sqlStmts:
    mycursor.execute(stmt)
    

# insert all the products
for product in Utilities.getJsonData(PATH_RAW_DATA):
    sql = """
    INSERT INTO Products 
    (user_id, name, description, product_categories_sub_id, location_id, dropoff_distance, price_half, price_full, image, minimum_age) VALUES
    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    parms = (product["user_id"], product["name"], product["description"], product["product_categories_sub_id"], product["location_id"], product["dropoff_distance"], product["price_half"], product["price_full"], product["image"], product["minimum_age"])
    mycursor.execute(sql, parms)


mydb.commit()
print('Complete')