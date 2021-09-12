

#******************************************************************
# Author: Robert Webster
# Program: Client Management App
# Date: 09/01/2021
# 
# Comments: 
#
# https://www.w3schools.com/python/python_classes.asp
# https://betterprogramming.pub/advanced-python-9-best-practices-to-apply-when-you-define-classes-871a27af658b
# https://www.youtube.com/watch?v=RSl87lqOXDE
#
#******************************************************************

import os
import sys
import string
import sqlite3
import pyodbc
import pandas as pd

from PyQt5 import QtWidgets
from PyQt5.QtCore import QAbstractTableModel, Qt, QCoreApplication
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QApplication
from application_windows import Ui_MainWindow
#from database_etl import *
#from database_create import *

class MainApplication(QtWidgets.QMainWindow): 
    
    def __init__(self):              
        super(MainApplication, self).__init__()        
        self.ui = Ui_MainWindow()    
        self.ui.setupUi(self)

        #initialize variables
        self._username = ""
        self._key = "123"

        self.__rec_id = ""
        self.__first_name = ""
        self.__last_name = ""
        self.__selected_service = ""

        #client detail
        self.__name1 = "Bob Jones"
        self.__name2 = "Sarah Davis"
        self.__name3 = "Amy Fristdendly"
        self.__name4 = "Johnny Smith"
        self.__name5 = "Carol Spears"

        #client selected choice
        self.__num1 = "Brokerage"
        self.__num2 = "Retirement"
        self.__num3 = "Brokerage"
        self.__num4 = "Brokerage"
        self.__num5 = "Retirement"

        #client list load index
        self.__client_list = 0
        self.__client_edit = 0
        self.__client_delete = 0

        #set design attributes
        self.style = "::section {""background-color: #E0E0E0; }" #set bg color of table header

        #set starting attributes
        self.ui.login_label_login_denied.setHidden(True)
        self.ui.label_welcome.setHidden(True)
        self.ui.client_list_delete_enter_id.setHidden(True)
        self.ui.client_list_edit_enter_id.setHidden(True)
        self.ui.login_text_username.selectAll()
        self.ui.menu_list.setCurrentRow(0) 

        #initialize form
        self.__nav_login

        #establish signal and slots      
        self.__connectSignalsSlots() #define form actions and calls
    
    def __connectSignalsSlots(self):
        self.ui.login_btn_Sign_In.clicked.connect(self.__authenticate)
        self.ui.menu_btn_submit.clicked.connect(self.__form_main_menu_select)
        self.ui.client_list_btn_main.clicked.connect(self.__nav_main)
        self.ui.client_list_edit_btn_main.clicked.connect(self.__nav_main)
        self.ui.client_list_edit_btn_edit.clicked.connect(self.__nav_client_edit_profile)
        self.ui.client_edit_profile_btn_update.clicked.connect(self.__update_client)
        self.ui.client_edit_profile_btn_cancel.clicked.connect(self.__nav_client_list_edit)
        self.ui.add_client_btn_add.clicked.connect(self.__add_client)
        self.ui.add_client_btn_cancel.clicked.connect(self.__nav_main)
        self.ui.client_list_delete_btn_delete.clicked.connect(self.__delete_client)
        self.ui.client_list_delete_btn_main.clicked.connect(self.__nav_main)

    def __authenticate(self):        
        #get values of username and password
        self.form_login_username = self.ui.login_text_username.text()
        self.form_login_password = self.ui.login_text_password.text()

        #input validation
        obj_inputvalidation = InputValidation(self.form_login_username)
        self.check_punctuation = obj_inputvalidation.check_has_punctuation()

        if self.check_punctuation == "True":
            
            self.ui.login_label_login_denied.setHidden(False) #make label visible       
            self.ui.login_label_login_denied.setText("Punctuation not allowed in Username") #change text 

        else:
            
            if self.form_login_username == "Username" or self.form_login_password == "Password":
                #access denied
                self.ui.login_label_login_denied.setHidden(False) #make label visible       
                self.ui.login_label_login_denied.setText("Please enter Username and Password") #change text          

            else:

                if  self._key == self.form_login_password:
                    #access granted
                    self.ui.login_label_login_denied.setHidden(True) #hide label
                    self.ui.label_welcome.setHidden(False) #unhide label
                    self.ui.label_welcome.setText("Welcome ") #change text

                    #form navigation
                    self.__nav_main()
                    self.get_client_list()
                
                else:
                    #access denied
                    self.ui.login_label_login_denied.setHidden(False) #make label visible       
                    self.ui.login_label_login_denied.setText("Incorrect Username/Password") #change text

      
    def __form_main_menu_select(self):

        #get value from list widget
        self.form_list_select = self.ui.menu_list.currentItem().text()

        #check to see if an item is selected
        items = self.ui.menu_list.selectedItems()
        selected_item = []

        for i in list(items):
                    selected_item.append(str(i.text()))

        if selected_item: #boolean if not empty

            #execute based on menu selection
            if self.form_list_select == "DISPLAY client list":
                #form navigation
                self.__nav_client_list()                                     

            elif self.form_list_select == "EDIT a client":
                #form navigation
                self.__nav_client_list_edit()

            elif self.form_list_select == "ADD a new client":
                #form navigation
                self.__nav_add_client()                

            elif self.form_list_select == "DELETE a client":
                #form navigation
                self.__nav_client_delete()  

            elif self.form_list_select == "Exit the program":
                sys.exit()
        else:
            pass
 
    def __update_client(self):

        #pass data to sql table
        self.edit_client_list(self, self.id, self.__first_name, self.__last_name, self.__selected_service)
        #FIXME




        #form navigation
        self.__nav_client_edit_profile()

    def __add_client(self):

        #get form input
        self.form_first_name = self.ui.add_client_text_first_name.text()
        self.form_last_name = self.ui.add_client_text_last_name.text()
        self.form_selected_service = self.ui.add_client_cmb_service.currentText()      
        
        self.clear_list = 0

        if self.form_first_name != "First Name" and  self.form_last_name != 'Last Name':           

            #add to list
            self.add_client(self.form_first_name, self.form_last_name, self.form_selected_service)

            #form navigation
            self.__nav_client_list()               

    def __delete_client(self):

        #get selected row
        self.selected_row = self.ui.client_list_delete_list.currentRow()

        #remove item from widget
        self.delete_client(self.selected_row)

        #form navigation
        self.__nav_client_delete()   
                                 
    def __nav_login(self):

        #iniialize form
        self.ui.stackedWidget.setCurrentWidget(self.ui.login)

    def __nav_main(self):

        #iniialize form
        self.ui.stackedWidget.setCurrentWidget(self.ui.main)  
        
        self.ui.menu_list.setCurrentRow(0) #set to default

    def __nav_client_list(self):

        #iniialize form
        self.ui.stackedWidget.setCurrentWidget(self.ui.client_list)

        #reset form fields
        self.ui.add_client_text_first_name.setText('First Name')
        self.ui.add_client_text_last_name.setText('Last Name')
        self.ui.add_client_cmb_service.setCurrentIndex(0)
        self.ui.add_client_text_first_name.selectAll()
   
    def __nav_client_list_edit(self):

        #iniialize form
        self.ui.stackedWidget.setCurrentWidget(self.ui.client_list_edit)

        self.ui.client_list_edit_enter_id.setText("Enter ID")
        self.ui.client_list_edit_enter_id.selectAll()
        self.ui.client_list_edit_enter_id.setFocus()

        self.ui.client_edit_profile_first_name.setText("First Name")
        self.ui.client_edit_profile_last_name.setText("Last Name")
        self.ui.client_edit_profile_cmb_service.setCurrentIndex(0)          


    def __nav_client_edit_profile(self):

        #get currently selected item details
        self.selected_details = self.ui.client_list_edit_list.currentItem().text()
        self.selected_row = self.ui.client_list_edit_list.currentRow()

        #split string and get first element
        x =  self.selected_details.split(" ")
        self.__rec_id = x[0]
        self.__first_name = x[1]
        self.__last_name = x[2]
        self.__selected_service = x[5]

        #iniialize form
        self.ui.stackedWidget.setCurrentWidget(self.ui.client_edit_profile)

        #set text
        self.ui.client_edit_profile_first_name.setText(self.__first_name)
        self.ui.client_edit_profile_last_name.setText(self.__last_name)

        if self.__selected_service == "Brokerage":
            self.ui.client_edit_profile_cmb_service.setCurrentIndex(0)
        elif self.__selected_service == "Retirement":
            self.ui.client_edit_profile_cmb_service.setCurrentIndex(1)

        #add client to qlistwidget
        self.ui.client_edit_profile_list.clear()
        self.client_detail = str(self.__rec_id) + " " + self.__first_name + " " + self.__last_name + " selected option " +  self.__selected_service

        #add to list qwidget
        self.ui.client_edit_profile_list.addItem(self.client_detail)



    def __nav_add_client(self):

        #iniialize form
        self.ui.stackedWidget.setCurrentWidget(self.ui.add_client)

        #select all of form box
        self.ui.add_client_text_first_name.selectAll()
        self.ui.add_client_text_first_name.setFocus()

    def __nav_client_delete(self):

        #iniialize form
        self.ui.stackedWidget.setCurrentWidget(self.ui.client_delete)

        self.ui.client_list_delete_enter_id.setText("Enter ID")
        self.ui.client_list_delete_enter_id.setFocus()
        self.ui.client_list_delete_enter_id.selectAll()

    def __nav_delete_client_profile(self):

        #iniialize form
        self.ui.stackedWidget.setCurrentWidget(self.ui.__delete_client_profile)

    def get_client_list(self):

        #build client details
        self.client_detail_1 = "1. " + self.__name1 + " selected option " + str(self.__num1)
        self.client_detail_2 = "2. " + self.__name2 + " selected option " + str(self.__num2)
        self.client_detail_3 = "3. " + self.__name3 + " selected option " + str(self.__num3)
        self.client_detail_4 = "4. " + self.__name4 + " selected option " + str(self.__num4)
        self.client_detail_5 = "5. " + self.__name5 + " selected option " + str(self.__num5)

        #add to list qwidgets
        self.ui.list_client_list.addItem(self.client_detail_1)
        self.ui.list_client_list.addItem(self.client_detail_2)
        self.ui.list_client_list.addItem(self.client_detail_3)
        self.ui.list_client_list.addItem(self.client_detail_4)
        self.ui.list_client_list.addItem(self.client_detail_5)

        self.ui.client_list_edit_list.addItem(self.client_detail_1)
        self.ui.client_list_edit_list.addItem(self.client_detail_2)
        self.ui.client_list_edit_list.addItem(self.client_detail_3)
        self.ui.client_list_edit_list.addItem(self.client_detail_4)
        self.ui.client_list_edit_list.addItem(self.client_detail_5)

        self.ui.client_list_delete_list.addItem(self.client_detail_1)
        self.ui.client_list_delete_list.addItem(self.client_detail_2)
        self.ui.client_list_delete_list.addItem(self.client_detail_3)
        self.ui.client_list_delete_list.addItem(self.client_detail_4)
        self.ui.client_list_delete_list.addItem(self.client_detail_5)


    def edit_client_list(self, id, first_name, last_name, selected_service):
        pass

        #FIXME














    def add_client(self, form_first_name, form_last_name, form_selected_service):

        #get count in list 
        next_num = self.ui.list_client_list.count() + 1
        
        #build client detail to list widgets
        self.client_detail = str(next_num) + ". " + form_first_name + " " + form_last_name + " selected option " + form_selected_service

        #add to list qwidget
        self.ui.list_client_list.addItem(self.client_detail)
        self.ui.client_list_edit_list.addItem(self.client_detail)
        self.ui.client_list_delete_list.addItem(self.client_detail)


    def delete_client(self, selected_row):

        self.selected_row = selected_row        

        self.ui.list_client_list.takeItem(int(self.selected_row))
        self.ui.client_list_edit_list.takeItem(int(self.selected_row))
        self.ui.client_list_delete_list.takeItem(int(self.selected_row))





class pandasModel(QAbstractTableModel):

    def __init__(self, data):

        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):

        return self._data.shape[0]

    def columnCount(self, parnet=None):

        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):

        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])

        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]

        return None

class InputValidation(object):     

    def __init__(self, input_string):

        self.input_string = input_string
          
    def check_has_punctuation(self):

        if any(char in string.punctuation for char in self.input_string):
            return "True"
        else:
            return "False"

    def check_has_digits(self):

        if any(char in string.digits for char in self.input_string):
            return "True"
        else:
            return "False"

    def check_has_ascii(self):

        if any(char in string.ascii_letter for char in self.input_string):
            return "True"
        else:
            return "False"




def main():

    if __name__ == "__main__":

        #create new database if does not exists
        database_path = os.environ['TEMP'] + '\cma.db'
        database_exists = os.path.exists(database_path)

        if database_exists == False:

            obj_db = CreateDB()
            obj_db.create_table_data()

        #start application
        app = QtWidgets.QApplication([])
        application = MainApplication()
        application.show()

    try:
        sys.exit(app.exec())
    except:
        print("Exiting")


main()










