#************************************************************************************
#
# This class handles all the database interactions
#
#************************************************************************************
import mysql.connector
from mysql.connector.cursor import MySQLCursor
from typing import Type
import os
import datetime
# from ..common import utilities, SortingSearchProducts, Pagination
from ..common import utilities

from . import credentials as db_credentials


class DB:

        
    #------------------------------------------------------
    # static properties
    #------------------------------------------------------
    SQL_CONNECTION_DATA_FILE = os.getcwd() + '/api_wmiys/DB/' + '.mysql-info.json'
    configData = utilities.readJsonFile(SQL_CONNECTION_DATA_FILE)
    mydb = mysql.connector.connect(user=configData['user'], password=configData['passwd'], host=configData['host'], database=configData['database'])


    def __init__(self):
        self.connection = mysql.connector.MySQLConnection()
    
    #----------------------------------------------------------
    # Connect to the database
    #----------------------------------------------------------
    def connect(self):
        self.connection = mysql.connector.connect(user=db_credentials.user, host=db_credentials.host, database=db_credentials.database, password=db_credentials.password)
    
    #----------------------------------------------------------
    # Close the database connection
    #----------------------------------------------------------
    def close(self):
        self.connection.close()

    #----------------------------------------------------------
    # Commit the current transaction
    #----------------------------------------------------------
    def commit(self):
        self.connection.commit()
        
    #----------------------------------------------------------
    # Get a cursor from the database connection.
    #
    # Args:
    #     a_dbCursorType (DbCursorTypes): Cursor type
    #
    # Returns:
    #     MySQLCursor: The connected mysql cursor.
    #----------------------------------------------------------
    def getCursor(self, asDict: bool=True) -> MySQLCursor:
        cursor = None

        if asDict:
            cursor = self.connection.cursor(dictionary=True)
        else:
            cursor = self.connection.cursor(prepared=True)
        
        return cursor








    #------------------------------------------------------
    # Check the DB connection.
    # If it's disconnected, reconnect
    #------------------------------------------------------
    @staticmethod
    def check_connection():
        try:
            DB.mydb.ping(reconnect=True, attempts=10, delay=2)
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
        raise NotImplementedError
        # """Returns a list of users
        # """
        # DB.check_connection()
        # mycursor = DB.mydb.cursor(named_tuple=True)
        
        # sql = """
        # SELECT 
        #     u.id as id,
        #     u.email as email,
        #     u.password as password,
        #     u.name_first as name_first,
        #     u.name_last as name_last,
        #     u.created_on as created_on,
        #     DATE_FORMAT(u.birth_date, '%Y-%m-%d') as birth_date
        # FROM Users u 
        # """

        # mycursor.execute(sql)
        # users = mycursor.fetchall()
        # DB.mydb.close()
        # return users 

    #------------------------------------------------------
    # Insert a new user into the database
    #------------------------------------------------------
    # @staticmethod
    # def insert_user(email: str, password: str, name_first: str, name_last: str, birth_date: str):
    #     """Insert a user into the Database

    #     Args:
    #         email (str): email
    #         password (str): password
    #         name_first (str): first name
    #         name_last (str): last name
    #         birth_date (str): birth day
    #     """        
    #     DB.check_connection()
    #     mycursor = DB.mydb.cursor(prepared=True)
        
    #     sql = """
    #     INSERT INTO Users 
    #     (email, password, name_first, name_last, birth_date) VALUES
    #     (%s, %s, %s, %s, %s)
    #     """

    #     parm_values = (email, password, name_first, name_last, birth_date)
    #     mycursor.execute(sql, parm_values)

    #     DB.mydb.commit()
    #     DB.mydb.close()

    #     return mycursor.lastrowid



    #------------------------------------------------------
    # Retrieve a single user record
    #------------------------------------------------------
    @staticmethod
    def get_user(user_id: int):
        raise NotImplementedError

        # DB.check_connection()
        # mycursor = DB.mydb.cursor(named_tuple=True)

        # sql = """
        # SELECT 
        #     u.id as id,
        #     u.email as email,
        #     u.password as password,
        #     u.name_first as name_first,
        #     u.name_last as name_last,
        #     u.created_on as created_on,
        #     DATE_FORMAT(u.birth_date, '%Y-%m-%d') as birth_date
        # FROM Users u
        # WHERE 
        #     u.id = %s
        # LIMIT 1
        # """
        # parms = (user_id,)
        
        # mycursor.execute(sql, parms)
        # result = mycursor.fetchone()
        # DB.mydb.close()
        
        # return result
    
    #------------------------------------------------------
    # Update a user record
    #------------------------------------------------------
    @staticmethod
    def update_user(id, email, password, name_first, name_last, birth_date):
        raise NotImplementedError
        # DB.check_connection()
        # mycursor = DB.mydb.cursor(prepared=True)
        
        # sql = """
        # UPDATE Users 
        # SET
        #     email = %s,
        #     password   = %s,
        #     name_first = %s,
        #     name_last  = %s,
        #     birth_date = %s
        # WHERE
        #     id = %s
        # """

        # parm_values = (email, password, name_first, name_last, birth_date, id)
        # mycursor.execute(sql, parm_values)
        # DB.mydb.commit()
        # DB.mydb.close()

        # return mycursor

        

    #------------------------------------------------------
    # Get a user's id from their email/password combination
    #------------------------------------------------------
    @staticmethod
    def getUserIDFromEmailPassword(email: str, password: str):
        raise NotImplementedError
        # DB.check_connection()
        # mycursor = DB.mydb.cursor(named_tuple=True)

        # sql = 'SELECT u.id FROM Users u WHERE u.email = %s AND u.password = %s'
        # parms = (email, password)

        # mycursor.execute(sql, parms)
        # result = mycursor.fetchone()
        # DB.mydb.close()
        
        # return result
    
    #------------------------------------------------------
    # Call the location search stored procedure
    #------------------------------------------------------
    @staticmethod
    def searchLocations(query: str, num_results: int=20):
        raise NotImplementedError
        # DB.check_connection()
        # mycursor = DB.mydb.cursor(named_tuple=True)

        # parms = [query, num_results]
        # result_args = mycursor.callproc('Search_Locations', parms)
        # result = next(mycursor.stored_results())
        # DB.mydb.close()

        # return result.fetchall()




    #------------------------------------------------------
    # Get all the product categories
    #------------------------------------------------------
    @staticmethod
    def getProductCategories():
        raise NotImplementedError
        # DB.check_connection()
        # mycursor = DB.mydb.cursor(named_tuple=True)

        # sql = 'SELECT * FROM All_Categories'

        # mycursor.execute(sql)
        # product_categories = mycursor.fetchall()
        # DB.mydb.close()
        # return product_categories


    #------------------------------------------------------
    # return all major categories
    #------------------------------------------------------
    @staticmethod
    def getProductCategoryMajors():
        raise NotImplementedError
        # DB.check_connection()
        # mycursor = DB.mydb.cursor(named_tuple=True)

        # sql = """
        # SELECT  major.id                            AS id, 
        #         major.name                          AS name
        # FROM    Product_Categories_Major major
        # ORDER   BY major.name ASC
        # """

        # mycursor.execute(sql)
        # major_categories = mycursor.fetchall()
        # DB.mydb.close()
        # return major_categories


    #------------------------------------------------------
    # return a single major category
    #------------------------------------------------------
    @staticmethod
    def getProductCategoryMajor(id: int):
        raise NotImplementedError
        # DB.check_connection()
        # mycursor = DB.mydb.cursor(named_tuple=True)

        # sql = """
        # SELECT  major.id                            AS id, 
        #         major.name                          AS name
        # FROM    Product_Categories_Major major
        # WHERE   major.id = %s
        # LIMIT 1
        # """

        # parms = (id,)
        # mycursor.execute(sql, parms)
        # major_category = mycursor.fetchone()
        # DB.mydb.close()

        # return major_category


    #------------------------------------------------------
    # return all the minor categories that belong to a specified major category
    #------------------------------------------------------
    @staticmethod
    def getProductMajorCategoryChildren(product_categories_major_id: int):
        raise NotImplementedError
        # DB.check_connection()
        # mycursor = DB.mydb.cursor(named_tuple=True)

        # sql = """
        # SELECT  minor.id                            AS id, 
        #         minor.product_categories_major_id   AS product_categories_major_id, 
        #         minor.name                          AS name
        # FROM    Product_Categories_Minor minor
        # WHERE   minor.product_categories_major_id = %s
        # GROUP   BY minor.id
        # ORDER   BY minor.name ASC
        # """

        # parms = (product_categories_major_id,)
        # mycursor.execute(sql, parms)
        # minor_categories = mycursor.fetchall()
        # DB.mydb.close()

        # return minor_categories


    #------------------------------------------------------
    # return a single minor category
    #------------------------------------------------------
    @staticmethod
    def getProductCategoryMinor(id: int):
        raise NotImplementedError
        # DB.check_connection()
        # mycursor = DB.mydb.cursor(named_tuple=True)

        # sql = """
        # SELECT  minor.id                            AS id, 
        #         minor.product_categories_major_id   AS product_categories_major_id, 
        #         minor.name                          AS name
        # FROM    Product_Categories_Minor minor
        # WHERE   minor.id = %s
        # LIMIT 1
        # """

        # parms = (id,)
        # mycursor.execute(sql, parms)
        # minor_category = mycursor.fetchone()
        # DB.mydb.close()

        # return minor_category
    

    #------------------------------------------------------
    # return all the sub categories that belong to a specified minor category
    #------------------------------------------------------
    @staticmethod 
    def getProductMinorCategoryChildren(product_categories_minor_id: int):
        raise NotImplementedError
        # DB.check_connection()
        # mycursor = DB.mydb.cursor(named_tuple=True)
        
        # sql = """
        # SELECT  s.id                            AS id, 
        #         s.product_categories_minor_id   AS product_categories_minor_id, 
        #         s.name                          AS name
        # FROM    Product_Categories_Sub s 
        # WHERE   s.product_categories_minor_id = %s
        # GROUP   BY s.id
        # ORDER   BY s.name ASC
        # """

        # parms = (product_categories_minor_id,)
        # mycursor.execute(sql, parms)
        # sub_categories = mycursor.fetchall()
        # DB.mydb.close()

        # return sub_categories
    
    
    #------------------------------------------------------
    # return a single sub category
    #------------------------------------------------------
    @staticmethod
    def getProductCategorySub(id: int):
        raise NotImplementedError
        # DB.check_connection()
        # mycursor = DB.mydb.cursor(named_tuple=True)
        
        # sql = """
        # SELECT  s.id                            AS id, 
        #         s.product_categories_minor_id   AS product_categories_minor_id, 
        #         s.name                          AS name
        # FROM    Product_Categories_Sub s 
        # WHERE   s.id = %s
        # LIMIT 1
        # """

        # parms = (id,)
        # mycursor.execute(sql, parms)
        # sub_category = mycursor.fetchone()
        # DB.mydb.close()

        # return sub_category




    
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
        DB.mydb.close()

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
        DB.mydb.close()

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
        DB.mydb.close()

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
        DB.mydb.close()

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
        DB.mydb.close()

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
        DB.mydb.close()

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
        DB.mydb.close()
        
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
        DB.mydb.close()
        
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
        DB.mydb.close()
        
        return mycursor.lastrowid

    @staticmethod
    def searchProductsAll(location_id: int, starts_on: datetime.date, ends_on: datetime.date, sorting_field: str, sorting_type: str, pagination_stmt_limit_offset: str, pagination_stmt_total_count: str):
        """Search all of the products
        
        ---
        Args:

        - location_id (int): dropoff location id
        - starts_on (date): when the request starts
        - ends_on (date): when the request ends
        - oSorting (Sorting): the sorting type to use
        - sorting_field (str): field to sort
        - sorting_type (str): type of sorting (asc or desc)
        - pagination_stmt_limit_offset (str) - sql limit offset statement
        - pagination_stmt_total_count (str) - sql statement for the count

        Returns:
            list: product search result
        """        

        # connect to the database
        DB.check_connection()
        mycursor = DB.mydb.cursor(named_tuple=True)

        # build the 
        stmt =  DB.getSearchProductSqlStmtPrefix_() + "ORDER BY {} {}".format(sorting_field, sorting_type)        
        parms = (location_id, starts_on, ends_on)

        mycursor.execute(pagination_stmt_limit_offset, parms)
        searchResults = mycursor.fetchall()

        mycursor.execute(pagination_stmt_total_count, parms)
        countResult = mycursor.fetchone()
        
        DB.mydb.close()

        return (searchResults, countResult.count)



    @staticmethod
    def searchProductsByCategory(location_id: int, starts_on: datetime.date, ends_on: datetime.date, product_category_type, product_category_id, sorting_field, sorting_type, pagination_stmt_limit, pagination_stmt_offset):
        """Calls the Search_Products stored procedure in the database.
        
        ---
        
        Args:
        - location_id (int): dropoff location id
        - starts_on (date): when the request starts
        - ends_on (date): when the request ends
        - product_category_type (int): the type of product category (1, 2, or 3) - major, minor, or sub 
        - product_categories_sub_id (int): id of the product category that the user wants to search for
        - sorting_field (str): field to sort
        - sorting_type (str): type of sorting (asc or desc)
        - oPagination (Pagination): a pagination object

        ---
        Returns:
            list: product search result
        """
        DB.check_connection()
        mycursor = DB.mydb.cursor(named_tuple=True)
 

        categoryTableName = DB.getSearchProductCategoryTableName_(product_category_type)
        stmt = DB.getSearchProductSqlStmtPrefix_() + "AND {} = %s ORDER BY {} {}"
        stmt = stmt.format(categoryTableName, sorting_field, sorting_type)

        parms = (location_id, starts_on, ends_on, product_category_id)
        
        mycursor.execute(pagination_stmt_limit, parms)
        searchResults = mycursor.fetchall()

        mycursor.execute(pagination_stmt_offset, parms)
        countResult = mycursor.fetchone()

        DB.mydb.close()

        return (searchResults, countResult.count)

    @staticmethod
    def getSearchProductSqlStmtPrefix_():
        """Generates the Search Products sql statement prefix

        Returns:
            str: the generated prefix
        """        

        sqlPrefix = """
        SELECT * FROM View_Search_Products p
        WHERE SEARCH_PRODUCTS_FILTER(p.id, %s, %s, %s) = TRUE 
        """

        return sqlPrefix

    @staticmethod
    def getSearchProductCategoryTableName_(a_iProductCategoryType: int) -> str:
        """Get the product category table name based on the input

            1 = major categories
            2 = minor categories
            3 = sub categories

        Args:
            a_iProductCategoryType (int): id of the product category table

        Returns:
            str: name of the product category table 
        """

        
        categoryTableName = ''

        if a_iProductCategoryType == 1:
            categoryTableName = 'product_categories_major_id'
        elif a_iProductCategoryType == 2:
            categoryTableName = 'product_categories_minor_id'
        else:
            categoryTableName = 'product_categories_sub_id'
        
        return categoryTableName


    @staticmethod
    def getProductImages(product_id: int):
        DB.check_connection()
        mycursor = DB.mydb.cursor(named_tuple=True)

        sql = """
        SELECT   *
        FROM     Product_Images pi
        WHERE    pi.product_id = %s
        """

        parms = (product_id,)
        mycursor.execute(sql, parms)
        images = mycursor.fetchall()

        DB.mydb.close()

        return images

    @staticmethod
    def deleteProductImages(product_id: int):
        DB.check_connection()
        mycursor = DB.mydb.cursor(prepared=True)

        sql = """
        DELETE FROM Product_Images
        WHERE product_id = %s
        """

        parms = (product_id,)
        mycursor.execute(sql, parms)
        DB.mydb.commit()

        DB.mydb.close()

        return mycursor.rowcount


    @staticmethod
    def getProductImage(product_image_id: int):
        DB.check_connection()
        mycursor = DB.mydb.cursor(named_tuple=True)

        sql = """
        SELECT   *
        FROM     Product_Images pi
        WHERE    pi.id = %s
        LIMIT 1
        """

        parms = (product_image_id,)
        mycursor.execute(sql, parms)
        image = mycursor.fetchone()

        DB.mydb.close()

        return image

        

    @staticmethod 
    def insertProductImage(product_id, file_name):
        """Insert a new product image into the database

        Args:
            product_id (int): parent id of the product the image belongs to
            file_name (str): file name of the image

        Returns:
            int: the id of the product image
        """        
        DB.check_connection()
        mycursor = DB.mydb.cursor(prepared=True)

        sql = """
        INSERT INTO Product_Images 
        (product_id, file_name) VALUES
        (%s, %s)
        """

        parms = (product_id, file_name)
        mycursor.execute(sql, parms)
        DB.mydb.commit()

        DB.mydb.close()
        
        return mycursor.lastrowid

