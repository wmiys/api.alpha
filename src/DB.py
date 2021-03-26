#************************************************************************************
#
# This class handles all the database interactions
#
#************************************************************************************

from Utilities import Utilities
import mysql.connector
from typing import Type

class DB:
    
    #------------------------------------------------------
    # static properties
    #------------------------------------------------------
    SQL_CONNECTION_DATA_FILE = '.mysql-info.json'
    configData = Utilities.readJsonFile(SQL_CONNECTION_DATA_FILE)
    mydb = mysql.connector.connect(user=configData['user'], password=configData['passwd'],
                                   host=configData['host'], database=configData['database'])

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
        return mysql.connector.connect(user=DB.configData['user'], password=DB.configData['passwd'],
                                       host=DB.configData['host'], database=DB.configData['database'])

    #------------------------------------------------------
    # Get all users
    #------------------------------------------------------
    @staticmethod
    def get_users():
        """Returns a list of users
        """
        DB.check_connection()
        mycursor = DB.mydb.cursor(named_tuple=True)
        sql = 'SELECT * FROM Users'
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

        sql = 'SELECT * FROM Users where id = %s'
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






