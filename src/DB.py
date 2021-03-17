from Utilities import Utilities
import mysql.connector
from typing import Type
from User import User

class DB:
    
    # static properties
    SQL_CONNECTION_DATA_FILE = '.mysql-info.json'

    configData = Utilities.readJsonFile(SQL_CONNECTION_DATA_FILE)
    mydb = mysql.connector.connect(**configData)

    @staticmethod
    def get_users():
        mycursor = DB.mydb.cursor(named_tuple=True)
        sql = 'SELECT * FROM Users'
        mycursor.execute(sql)
        users = mycursor.fetchall()

        return users 

    @staticmethod
    def insert_user(email: str, password: str, name_first: str, name_last: str, birth_date: str):
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

    @staticmethod
    def get_user(user_id: int):
        mycursor = DB.mydb.cursor(named_tuple=True)

        sql = 'SELECT * FROM Users where id = %s'
        parms = (user_id,)
        
        mycursor.execute(sql, parms)
        result = mycursor.fetchone()
        
        return result



        





