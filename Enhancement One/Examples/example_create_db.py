#******************************************************************
# Author: Robert Webster
# Program: Authentication class
# Date: 09/01/2021
# 
# Comments: Create database in memory
#
#******************************************************************

import sqlite3

class app_db(object):
    
    def create_db(self):

        #conn = sqlite3.connect('cma.db') #choose for file database
        conn = sqlite3.connect(":memory:") #choose for memory database

        c = conn.cursor()

        c.execute("""CREATE TABLE tbl_client_list (
                    id integer PRIMARY KEY AUTOINCREMENT,
                    first_name text,
                    last_name text,
                    selected_service text
                    )""")

        c.execute("""CREATE TABLE tbl_user_list (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name text,
                    last_name text,
                    username text,
                    pw text
                    )""")
        
        #INSERT DATA
        with conn:
            c.execute("INSERT INTO tbl_client_list VALUES ( Null, 'Bob', 'Jones', 'Brokerage')")
            c.execute("INSERT INTO tbl_client_list VALUES ( Null, 'Sarah', 'Davis', 'Retirement')")
            c.execute("INSERT INTO tbl_client_list VALUES ( Null, 'Amy', 'Fristdendly', 'Retirement')")
            c.execute("INSERT INTO tbl_client_list VALUES ( Null, 'Johnny', 'Smith', 'Retirement')")
            c.execute("INSERT INTO tbl_client_list VALUES ( Null, 'Carol', 'Spears', 'Retirement')")


        with conn:
            c.execute("INSERT INTO tbl_user_list VALUES ( Null, 'Robert', 'Webster', 'rw97474', '123')")
            c.execute("INSERT INTO tbl_user_list VALUES ( Null, 'Crystal', 'Perales', 'cp1234', '123')")
            c.execute("INSERT INTO tbl_user_list VALUES ( Null, 'Mariah', 'Rodriguez', 'mr1234', '123')")


        #SELCT AND PRINT RECORDS FROM TABLES
        c.execute("SELECT * FROM tbl_client_list")
        print(c.fetchall())

        c.execute("SELECT * FROM tbl_user_list")
        print(c.fetchall())

        #conn.close()
