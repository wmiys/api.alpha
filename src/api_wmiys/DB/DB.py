#************************************************************************************
#
# This class handles all the database interactions
#
#************************************************************************************

from api_wmiys.common.Utilities import Utilities
import mysql.connector
from typing import Type
import os

class DB:
    
    #------------------------------------------------------
    # static properties
    #------------------------------------------------------
    SQL_CONNECTION_DATA_FILE = os.getcwd() + '/api_wmiys/DB/' + '.mysql-info.json'
    configData = Utilities.readJsonFile(SQL_CONNECTION_DATA_FILE)
    mydb = mysql.connector.connect(user=configData['user'], password=configData['passwd'], host=configData['host'], database=configData['database'])

    #------------------------------------------------------
    # Check the DB connection.
    # If it's disconnected, reconnect
    #------------------------------------------------------
    @staticmethod
    def check_connection():
        try:
            DB.mydb.ping(reconnect=True, attempts=3, delay=1)
        except mysql.connector.Error as err:
            mydb = DB.init_db()

    #------------------------------------------------------
    # Connect the DB handle to the database
    #------------------------------------------------------
    @staticmethod
    def init_db():
        return mysql.connector.connect(user=DB.configData['user'], password=DB.configData['passwd'], host=DB.configData['host'], database=DB.configData['database'])

    #------------------------------------------------------
    # Get all users
    #------------------------------------------------------
    @staticmethod
    def get_users():
        """Returns a list of users
        """
        DB.check_connection()
        mycursor = DB.mydb.cursor(named_tuple=True)
        
        sql = """
        SELECT 
            u.id as id,
            u.email as email,
            u.password as password,
            u.name_first as name_first,
            u.name_last as name_last,
            u.created_on as created_on,
            DATE_FORMAT(u.birth_date, '%Y-%m-%d') as birth_date
        FROM Users u 
        """

        mycursor.execute(sql)
        users = mycursor.fetchall()

        return users 

    #------------------------------------------------------
    # Insert a new user into the database
    #------------------------------------------------------
    @staticmethod
    def insert_user(email: str, password: str, name_first: str, name_last: str, birth_date: str):
        """Insert a user into the Database

        Args:
            email (str): email
            password (str): password
            name_first (str): first name
            name_last (str): last name
            birth_date (str): birth day
        """        
        DB.check_connection()
        mycursor = DB.mydb.cursor(prepared=True)
        
        sql = """
        INSERT INTO Users 
        (email, password, name_first, name_last, birth_date) VALUES
        (%s, %s, %s, %s, %s)
        """

        parm_values = (email, password, name_first, name_last, birth_date)
        mycursor.execute(sql, parm_values)

        DB.mydb.commit()

        return mycursor.lastrowid

    #------------------------------------------------------
    # Retrieve a single user record
    #------------------------------------------------------
    @staticmethod
    def get_user(user_id: int):
        DB.check_connection()
        mycursor = DB.mydb.cursor(named_tuple=True)

        sql = """
        SELECT 
            u.id as id,
            u.email as email,
            u.password as password,
            u.name_first as name_first,
            u.name_last as name_last,
            u.created_on as created_on,
            DATE_FORMAT(u.birth_date, '%Y-%m-%d') as birth_date
        FROM Users u
        WHERE 
            u.id = %s
        LIMIT 1
        """
        parms = (user_id,)
        
        mycursor.execute(sql, parms)
        result = mycursor.fetchone()
        
        return result

    #------------------------------------------------------
    # Get a user's id from their email/password combination
    #------------------------------------------------------
    @staticmethod
    def getUserIDFromEmailPassword(email: str, password: str):
        DB.check_connection()
        mycursor = DB.mydb.cursor(named_tuple=True)

        sql = 'SELECT u.id FROM Users u WHERE u.email = %s AND u.password = %s'
        parms = (email, password)

        mycursor.execute(sql, parms)
        result = mycursor.fetchone()
        
        return result
    
    #------------------------------------------------------
    # Call the location search stored procedure
    #------------------------------------------------------
    @staticmethod
    def searchLocations(query: str, num_results: int=20):
        DB.check_connection()
        mycursor = DB.mydb.cursor(named_tuple=True)

        parms = [query, num_results]
        result_args = mycursor.callproc('Search_Locations', parms)
        result = next(mycursor.stored_results())

        return result.fetchall()

    #------------------------------------------------------
    # Get all the product categories
    #------------------------------------------------------
    @staticmethod
    def getProductCategories():
        DB.check_connection()
        mycursor = DB.mydb.cursor(named_tuple=True)

        sql = 'SELECT * FROM All_Categories'

        mycursor.execute(sql)
        product_categories = mycursor.fetchall()
        return product_categories


    #------------------------------------------------------
    # return all major categories
    #------------------------------------------------------
    @staticmethod
    def getProductCategoryMajors():
        DB.check_connection()
        mycursor = DB.mydb.cursor(named_tuple=True)

        sql = """
        SELECT  major.id                            AS id, 
                major.name                          AS name
        FROM    Product_Categories_Major major
        ORDER   BY major.name ASC
        """

        mycursor.execute(sql)
        major_categories = mycursor.fetchall()
        return major_categories


    #------------------------------------------------------
    # return a single major category
    #------------------------------------------------------
    @staticmethod
    def getProductCategoryMajor(id: int):
        DB.check_connection()
        mycursor = DB.mydb.cursor(named_tuple=True)

        sql = """
        SELECT  major.id                            AS id, 
                major.name                          AS name
        FROM    Product_Categories_Major major
        WHERE   major.id = %s
        LIMIT 1
        """

        parms = (id,)
        mycursor.execute(sql, parms)
        major_category = mycursor.fetchone()

        return major_category


    #------------------------------------------------------
    # return all the minor categories that belong to a specified major category
    #------------------------------------------------------
    @staticmethod
    def getProductMajorCategoryChildren(product_categories_major_id: int):
        DB.check_connection()
        mycursor = DB.mydb.cursor(named_tuple=True)

        sql = """
        SELECT  minor.id                            AS id, 
                minor.product_categories_major_id   AS product_categories_major_id, 
                minor.name                          AS name
        FROM    Product_Categories_Minor minor
        WHERE   minor.product_categories_major_id = %s
        GROUP   BY minor.id
        ORDER   BY minor.name ASC
        """

        parms = (product_categories_major_id,)
        mycursor.execute(sql, parms)
        minor_categories = mycursor.fetchall()

        return minor_categories


    #------------------------------------------------------
    # return a single minor category
    #------------------------------------------------------
    @staticmethod
    def getProductCategoryMinor(id: int):
        DB.check_connection()
        mycursor = DB.mydb.cursor(named_tuple=True)

        sql = """
        SELECT  minor.id                            AS id, 
                minor.product_categories_major_id   AS product_categories_major_id, 
                minor.name                          AS name
        FROM    Product_Categories_Minor minor
        WHERE   minor.id = %s
        LIMIT 1
        """

        parms = (id,)
        mycursor.execute(sql, parms)
        minor_category = mycursor.fetchone()

        return minor_category
    

    #------------------------------------------------------
    # return all the sub categories that belong to a specified minor category
    #------------------------------------------------------
    @staticmethod 
    def getProductMinorCategoryChildren(product_categories_minor_id: int):
        DB.check_connection()
        mycursor = DB.mydb.cursor(named_tuple=True)
        
        sql = """
        SELECT  s.id                            AS id, 
                s.product_categories_minor_id   AS product_categories_minor_id, 
                s.name                          AS name
        FROM    Product_Categories_Sub s 
        WHERE   s.product_categories_minor_id = %s
        GROUP   BY s.id
        ORDER   BY s.name ASC
        """

        parms = (product_categories_minor_id,)
        mycursor.execute(sql, parms)
        sub_categories = mycursor.fetchall()

        return sub_categories
    
    
    #------------------------------------------------------
    # return a single sub category
    #------------------------------------------------------
    @staticmethod
    def getProductCategorySub(id: int):
        DB.check_connection()
        mycursor = DB.mydb.cursor(named_tuple=True)
        
        sql = """
        SELECT  s.id                            AS id, 
                s.product_categories_minor_id   AS product_categories_minor_id, 
                s.name                          AS name
        FROM    Product_Categories_Sub s 
        WHERE   s.id = %s
        LIMIT 1
        """

        parms = (id,)
        mycursor.execute(sql, parms)
        sub_category = mycursor.fetchone()

        return sub_category
    
    #------------------------------------------------------
    # create a new product
    #------------------------------------------------------
    @staticmethod
    def insertProduct(user_id, name, description=None, product_categories_sub_id=None, location_id=None, dropoff_distance=None, price_full=None, price_half=None, image=None, minimum_age=None):
        DB.check_connection()
        mycursor = DB.mydb.cursor(prepared=True)
        
        sql = """
        INSERT INTO Products
        (user_id, name, description, product_categories_sub_id, location_id, dropoff_distance, price_full, price_half, image, minimum_age) VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        parms = (user_id, name, description, product_categories_sub_id, location_id, dropoff_distance, price_full, price_half, image, minimum_age)
        mycursor.execute(sql, parms)
        DB.mydb.commit()

        return mycursor.lastrowid
    
    #------------------------------------------------------
    # Update a product
    #------------------------------------------------------
    @staticmethod
    def updateProduct(product_id, name=None, description=None, product_categories_sub_id=None, location_id=None, dropoff_distance=None, price_full=None, price_half=None, image=None, minimum_age=None):
        DB.check_connection()
        mycursor = DB.mydb.cursor(prepared=True)

        sql = """
        UPDATE Products
        SET
            name                      = %s,
            description               = %s,
            product_categories_sub_id = %s,
            location_id               = %s,
            dropoff_distance          = %s,
            price_full                = %s,
            price_half                = %s,
            image                     = %s,
            minimum_age               = %s
        WHERE 
            id = %s
        """

        parms = (name, description, product_categories_sub_id, location_id, dropoff_distance, price_full, price_half, image, minimum_age, product_id)
        mycursor.execute(sql, parms)
        DB.mydb.commit()

        return mycursor


    #------------------------------------------------------
    # Returns a product row
    #
    # Fields:
    #   - id
    #   - name
    #   - description
    #   - product_categories_sub_id
    #   - product_categories_sub_name
    #   - product_categories_minor_id
    #   - product_categories_minor_name
    #   - product_categories_major_id
    #   - product_categories_major_name
    #   - location_id
    #   - location_city
    #   - location_state_id
    #   - location_state_name
    #   - dropoff_distance
    #   - price_full
    #   - price_half
    #   - image
    #   - created_on
    #   - user_id
    #   - user_email
    #   - user_name_first
    #   - user_name_last
    #------------------------------------------------------
    @staticmethod
    def getProduct(id: int):
        DB.check_connection()
        mycursor = DB.mydb.cursor(named_tuple=True)

        sql = """
        SELECT *
        FROM View_Products p
        WHERE  p.id = %s
        GROUP  BY p.id
        LIMIT  1 
        """

        parms = (id,)
        mycursor.execute(sql, parms)
        product = mycursor.fetchone()

        return product
    
    #------------------------------------------------------
    # Returns all of a user's products
    #
    # Product Fields:
    #   - id
    #   - name
    #   - description
    #   - product_categories_sub_id
    #   - product_categories_sub_name
    #   - product_categories_minor_id
    #   - product_categories_minor_name
    #   - product_categories_major_id
    #   - product_categories_major_name
    #   - location_id
    #   - location_city
    #   - location_state_id
    #   - location_state_name
    #   - dropoff_distance
    #   - price_full
    #   - price_half
    #   - image
    #   - created_on
    #   - user_id
    #   - user_email
    #   - user_name_first
    #   - user_name_last
    #------------------------------------------------------
    @staticmethod
    def getUserProducts(user_id: int):
        DB.check_connection()
        mycursor = DB.mydb.cursor(named_tuple=True)

        sql = """
        SELECT *
        FROM View_Products p
        WHERE  p.user_id = %s
        GROUP  BY p.id
        ORDER BY p.name ASC
        """

        parms = (user_id,)
        mycursor.execute(sql, parms)
        products = mycursor.fetchall()

        return products


    @staticmethod
    def getProductAvailabilities(product_id: int):
        """Get all the product availability records for a single product
        """

        DB.check_connection()
        mycursor = DB.mydb.cursor(named_tuple=True)

        sql = """
        SELECT   *
        FROM     View_Product_Availability pa
        WHERE    pa.product_id = %s
        ORDER BY pa.created_on DESC
        """

        parms = (product_id,)
        mycursor.execute(sql, parms)
        availabilities = mycursor.fetchall()

        return availabilities
    
    @staticmethod
    def getProductAvailability(id: int):
        """Get the database record for a single product availability

        Args:
            id (int): the id of the product 

        Returns:
            db record
        """        

        DB.check_connection()
        mycursor = DB.mydb.cursor(named_tuple=True)

        sql = """
        SELECT   *
        FROM     View_Product_Availability pa
        WHERE    pa.id = %s
        ORDER BY pa.created_on DESC
        LIMIT 1
        """

        parms = (id,)
        mycursor.execute(sql, parms)
        availability = mycursor.fetchone()

        return availability

    
    @staticmethod
    def updateProductAvailability(id, product_id, starts_on=None, ends_on=None, note=None):
        """Update a single product availability record
        """
        DB.check_connection()
        mycursor = DB.mydb.cursor(prepared=True)

        sql = """
        UPDATE Product_Availability
        SET
            product_id = %s,
            starts_on  = %s,
            ends_on    = %s,
            note       = %s
        WHERE 
            id = %s
        """

        parms = (product_id, starts_on, ends_on, note, id)
        mycursor.execute(sql, parms)
        DB.mydb.commit()
        
        return mycursor
    
    @staticmethod
    def deleteProductAvailability(id):
        """Delete a single product availability record
        """
        DB.check_connection()
        mycursor = DB.mydb.cursor(prepared=True)

        sql = """
        DELETE FROM Product_Availability
        WHERE id = %s
        """

        parms = (id,)
        mycursor.execute(sql, parms)
        DB.mydb.commit()
        
        return mycursor

    
    @staticmethod
    def insertProductAvailability(product_id, starts_on, ends_on, note=None):
        """Insert a new product availability record

        Returns:
            mycursor.lastrowid (int): the id of the newly created product availability
        """

        DB.check_connection()
        mycursor = DB.mydb.cursor(prepared=True)

        sql = """
        INSERT INTO Product_Availability 
        (product_id, starts_on, ends_on, note) VALUES
        (%s, %s, %s, %s)
        """

        parms = (product_id, starts_on, ends_on, note)
        mycursor.execute(sql, parms)
        DB.mydb.commit()
        
        return mycursor.lastrowid




