

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
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QApplication, QTableView
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

        self.__name1 = "Bob Jones";
        self.__name2 = "Sarah Davis";
        self.__name3 = "Amy Fristd::endly";
        self.__name4 = "Johnny Smith";
        self.__name5 = "Carol Spears";







        #set design attributes
        self.style = "::section {""background-color: #E0E0E0; }" #set bg color of table header

        #set starting attributes
        self.ui.login_label_login_denied.setHidden(True)
        self.ui.label_welcome.setHidden(True)      
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

        #get text from label
        self.id = self.ui.client_list_edit_enter_id.text()
        self.__first_name = self.ui.client_edit_profile_first_name.text()
        self.__last_name = self.ui.client_edit_profile_last_name.text()
        self.__selected_service = self.ui.client_edit_profile_cmb_service.currentText()

        #pass data to sql table
        ManageClient.edit_client_list(self, self.id, self.__first_name, self.__last_name, self.__selected_service)

        #form navigation
        self.__nav_client_edit_profile() 

    def __add_client(self):

        #get form input
        self.form_first_name = self.ui.add_client_text_first_name.text()
        self.form_last_name = self.ui.add_client_text_last_name.text()
        self.form_selected_service = self.ui.add_client_cmb_service.currentText()       

        if self.form_first_name != "First Name" and  self.form_last_name != 'Last Name':           

            #pass data to sql table
            ManageClient.add_client(self, self.form_first_name, self.form_last_name, self.form_selected_service)

            #form navigation
            self.__nav_client_list()               

    def __delete_client(self):

        #get text from label
        self.id = self.ui.client_list_delete_enter_id.text()

        #input validation
        obj_inputvalidation = InputValidation(self.id)
        self.check_digit = obj_inputvalidation.check_has_digits()

        if self.check_digit == "True":

            #pass data to sql table
            ManageClient.delete_client(self, self.id)

            #form navigation
            self.__nav_client_delete()
        else:
            self.ui.client_list_delete_enter_id.setText("Enter ID")
            self.ui.client_list_delete_enter_id.setFocus()
            self.ui.client_list_delete_enter_id.selectAll()           
                                 
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

        #get client list for table widget
        widget_name = "client_list_list"
        get_type = "all" #all or one client(s)
        self.get_client_list(widget_name, get_type, id)
   
    def __nav_client_list_edit(self):

        #iniialize form
        self.ui.stackedWidget.setCurrentWidget(self.ui.client_list_edit)

        self.ui.client_list_edit_enter_id.setText("Enter ID")
        self.ui.client_list_edit_enter_id.selectAll()
        self.ui.client_list_edit_enter_id.setFocus()

        self.ui.client_edit_profile_first_name.setText("First Name")
        self.ui.client_edit_profile_last_name.setText("Last Name")
        self.ui.client_edit_profile_cmb_service.setCurrentIndex(0)   
        
        #get client list for table widget
        widget_name = "client_list_edit_list"
        get_type = "all" #all or one client(s)
        self.get_client_list(widget_name, get_type, id)

    def __nav_client_edit_profile(self):

        #get client id
        id = self.ui.client_list_edit_enter_id.text()

        #input validation
        obj_inputvalidation = InputValidation(id)
        self.check_digit = obj_inputvalidation.check_has_digits()

        if self.check_digit == "True":

            #iniialize form
            self.ui.stackedWidget.setCurrentWidget(self.ui.client_edit_profile)

            #get client list for table widget
            widget_name = "client_edit_profile_list"
            get_type = "one" #all or one client(s)
            self.get_client_list(widget_name, get_type, id)

            #set text
            self.ui.client_edit_profile_first_name.setText(self.__first_name)
            self.ui.client_edit_profile_last_name.setText(self.__last_name)

            if self.__selected_service == "Brokerage":
                self.ui.client_edit_profile_cmb_service.setCurrentIndex(0)
            elif self.__selected_service == "Retirement":
                self.ui.client_edit_profile_cmb_service.setCurrentIndex(1)

        else:
            self.ui.client_list_edit_enter_id.setText("Enter ID")
            self.ui.client_list_edit_enter_id.selectAll()
            self.ui.client_list_edit_enter_id.setFocus()

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

     #get client list for table widget
        widget_name = "client_list_delete_list"
        get_type = "all" #all or one client(s)
        self.get_client_list(widget_name, get_type, id)

    def __nav_delete_client_profile(self):

        #iniialize form
        self.ui.stackedWidget.setCurrentWidget(self.ui.__delete_client_profile)

    def get_client_list(self, widget_name, get_type, client_id):

        self.client_id = client_id

        if get_type == "all":

            #get client list
            obj_1 = DBGetAllClients()
            self.clients = obj_1.get_all_clients()
            df = pd.DataFrame(self.clients)
            model = pandasModel(df)

            set_model = "self.ui." + widget_name + ".setModel(model)"
            exec(set_model)

        elif get_type == "one": 

            #get client list
            obj_2 = DBGetSingleClient(self.client_id)
            self.client = obj_2.get_single_client()
            df = pd.DataFrame(self.client)
            model = pandasModel(df)

            set_model = "self.ui." + widget_name + ".setModel(model)"
            exec(set_model)

            #get values from data frame
            self.__rec_id = str(df.iloc[0][0])
            self.__first_name = str(df.iloc[0][1])
            self.__last_name = str(df.iloc[0][2])
            self.__selected_service = str(df.iloc[0][3])

        #disable widget select ability
        disable_select_1 = "self.ui." + widget_name + ".setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)"
        disable_select_2 = "self.ui." + widget_name + ".setFocusPolicy(Qt.NoFocus)"
        disable_select_3 = "self.ui." + widget_name + ".setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)"
        exec(disable_select_1), exec(disable_select_2), exec(disable_select_3)

        #set column widths
        col_width_1 = "self.ui." + widget_name + ".horizontalHeader()"
        col_width_2 = "self.ui." + widget_name + ".horizontalHeader().resizeSection(0, 25)"
        col_width_3 = "self.ui." + widget_name + ".horizontalHeader().resizeSection(1, 220)"
        col_width_4 = "self.ui." + widget_name + ".horizontalHeader().resizeSection(2, 220)"
        col_width_5 = "self.ui." + widget_name + ".horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)"
        col_width_6 = "self.ui." + widget_name + ".horizontalHeader().setDefaultAlignment(Qt.AlignLeft)"
        exec(col_width_1), exec(col_width_2), exec(col_width_3), exec(col_width_4), exec(col_width_5), exec(col_width_6)

        #reset vertical scroll to top
        reset_scroll = "self.ui." + widget_name + ".scrollTo(self.ui." + widget_name + ".model().index(0, 0))"        
        exec(reset_scroll)

        #set header bg color
        header_color = "self.ui." + widget_name + ".horizontalHeader().setStyleSheet(self.style)"
        exec(header_color)  


class ManageClient(object):

    def get_client_list(self):
        pass
        #FIXME

    def edit_client_list(self, id, first_name, last_name, selected_service):

        #update client in database
        obj_1 = DBUpdateSingleClient(id, first_name, last_name, selected_service)
        obj_1.update_single_client()

    def add_client(self, form_first_name, form_last_name, form_selected_service):

        #add client in database      
        obj_1 = DBAddSingleClient(form_first_name, form_last_name, form_selected_service)
        obj_1.add_single_client()

    def delete_client(self, client_id):

        #delete client in database
        obj_1 = DBDeleteSingleClient(client_id)
        obj_1.delete_single_client()


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










