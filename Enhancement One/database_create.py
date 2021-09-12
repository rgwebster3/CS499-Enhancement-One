
#******************************************************************
# Author: Robert Webster
# Program: Authentication class
# Date: 09/01/2021
# 
# Comments: Database connection
#
#******************************************************************

import os
import pyodbc
import sqlite3
import pandas as pd

class DBMakeConnection():

    def make_connection(self):    
        self.__sys_temp_folder = os.environ['TEMP']
        self.__conn = sqlite3.connect(self.__sys_temp_folder + '\cma.db')
        self.__cursor = self.__conn.cursor()

class CreateDB(DBMakeConnection):

    def __init__(self):
        super(CreateDB, self).make_connection()

        self.__sys_temp_folder = os.environ['TEMP']
        self.__conn = sqlite3.connect(self.__sys_temp_folder + '\cma.db')
        self.__cursor = self.__conn.cursor()  

    def create_table_data(self):  
        
        self._DBMakeConnection__cursor.execute("""CREATE TABLE tbl_client_list (
                    id integer PRIMARY KEY AUTOINCREMENT,
                    first_name text,
                    last_name text,
                    selected_service text
                    )""")

        self._DBMakeConnection__cursor.execute("""CREATE TABLE tbl_user_list (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name text,
                    last_name text,
                    username text,
                    pw text
                    )""")
        
        #insert data
        with self._DBMakeConnection__conn:
            self._DBMakeConnection__cursor.execute("INSERT INTO tbl_client_list VALUES ( Null, 'Bob', 'Jones', 'Brokerage')")
            self._DBMakeConnection__cursor.execute("INSERT INTO tbl_client_list VALUES ( Null, 'Sarah', 'Davis', 'Retirement')")
            self._DBMakeConnection__cursor.execute("INSERT INTO tbl_client_list VALUES ( Null, 'Amy', 'Fristdendly', 'Retirement')")
            self._DBMakeConnection__cursor.execute("INSERT INTO tbl_client_list VALUES ( Null, 'Johnny', 'Smith', 'Retirement')")
            self._DBMakeConnection__cursor.execute("INSERT INTO tbl_client_list VALUES ( Null, 'Carol', 'Spears', 'Retirement')")

        with self._DBMakeConnection__conn:
            self._DBMakeConnection__cursor.execute("INSERT INTO tbl_user_list VALUES ( Null, 'Robert', 'Webster', 'rw97474', '123')")
            self._DBMakeConnection__cursor.execute("INSERT INTO tbl_user_list VALUES ( Null, 'Crystal', 'Perales', 'cp1234', '123')")
            self._DBMakeConnection__cursor.execute("INSERT INTO tbl_user_list VALUES ( Null, 'Mariah', 'Rodriguez', 'mr1234', '123')")
            self._DBMakeConnection__cursor.execute("INSERT INTO tbl_user_list VALUES ( Null, 'Janis', 'Whitehead', 'jw1234', '123')")

        #select and print records
        self._DBMakeConnection__cursor.execute("SELECT * FROM tbl_client_list")
        print(self._DBMakeConnection__cursor.fetchall())

        self._DBMakeConnection__cursor.execute("SELECT * FROM tbl_user_list")
        print(self._DBMakeConnection__cursor.fetchall())

        #clear and close db
        self._DBMakeConnection__cursor.close()
        del self._DBMakeConnection__cursor

        self._DBMakeConnection__conn.close()
        del self._DBMakeConnection__conn