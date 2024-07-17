# -------------------------------------------------------------------------------
# Name:             SimpleSqlite.py
# Purpose:          Generic Sqlite starup. Open and connect to a dBase
#
# Author:           Jeffreaux
#
# Created:          07July24
#
# Required Packages:    PyQt5, PyQt5-Tools
# -------------------------------------------------------------------------------

from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
    QPushButton,
    QAction,
    QLineEdit,
    QLabel,
    QTabWidget,
    QPlainTextEdit,
)
from PyQt5 import uic

from fileModule import *
from Boxes import *
from PyQt5.QtGui import QPixmap # Create Pixmap to display Pics on a label
from PyQt5.QtGui import QImage # Create pic from BLOB data from a dB
import sys
import sqlite3
import random

# Create dBase and create cursor
conn = sqlite3.connect("general.db")
c = conn.cursor()

command_create_table = """
                    CREATE TABLE IF NOT EXISTS states(
                    id INTEGER PRIMARY KEY,
                    statename TEXT,
                    capitol TEXT,
                    photo BLOB,
                    established INTEGER
                    )"""

c.execute(command_create_table)


conn.commit()
conn.close()

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        # Load the UI file
        uic.loadUi("SimpleSqlite_GUI.ui", self)

        # define Widgets ##########################################################################
        self.tab = self.findChild(QTabWidget, "tab")

        self.btnExit = self.findChild(QPushButton, "btnExit")
        self.btnSelectPhoto = self.findChild(QPushButton, "btnSelectPhoto")
        self.btnSaveRecord = self.findChild(QPushButton, "btnSaveRecord")
        self.btnGo = self.findChild(QPushButton, "btnGo")
        self.btnIndexForward = self.findChild(QPushButton, "btnIndexForward")
        self.btnIndexBack = self.findChild(QPushButton, "btnIndexBack")

        self.lblPhoto = self.findChild(QLabel, "lblPhoto")
        self.lblStateName = self.findChild(QLabel, "lblStateName")
        self.lblEstablished = self.findChild(QLabel, "lblEstablished")
        self.lblPhotoSelected = self.findChild(QLabel, "lblPhotoSelected")
        self.lblCapitol = self.findChild(QLabel, "lblCapitol")
        self.lblCurrentIndex = self.findChild(QLabel, "lblCurrentIndex")

        self.txtStateName = self.findChild(QLineEdit, "txtStateName")
        self.txtCapitol = self.findChild(QLineEdit, "txtCapitol")
        self.txtEstablished = self.findChild(QLineEdit, "txtEstablished")
        self.txtSearchIndex = self.findChild(QLineEdit, "txtSearchIndex")
        self.txtSearchStateName = self.findChild(QLineEdit, "txtSearchStateName")

        self.pteSearchResults = self.findChild(QPlainTextEdit, "pteSearchResults")


        self.actExit = self.findChild(QAction, "actExit")

        # Define the actions ######################################################################
        self.btnExit.clicked.connect(self.closeEvent)
        self.btnSelectPhoto.clicked.connect(self.select_picture)
        self.btnSaveRecord.clicked.connect(self.write_to_db)
        self.btnGo.clicked.connect(self.go_search)
        self.btnIndexForward.clicked.connect(self.index_forward)
        self.btnIndexBack.clicked.connect(self.index_back)
        

        self.txtSearchIndex.returnPressed.connect(self.go_search)
        self.txtSearchStateName.returnPressed.connect(self.search_state_name)

        self.actExit.triggered.connect(self.closeEvent)

        # Set Opening page to Home
        self.tab.setCurrentIndex(0)

        # Show the app
        self.show()

        # Select record to be displayed at starup
        self.get_random_index()  

    def select_picture(self):
        print("Getting Photo")
        fname = getFullFilename_txt(self)  # Select pic file to display
        print(fname)
        self.photo_BLOB = convert_to_BLOB(self,fname)
        photo = QPixmap(fname)  # Create a Pixmap object
        picHeight = photo.height()
        picWidth = photo.width()
        
        if picWidth > picHeight:  # ScaledContents must be enabled in UI file.
            scaled_photo = photo.scaledToWidth(280, 0) # This value is from the size of the label container
            print("Scaled by width")
            self.lblPhotoSelected.setPixmap(scaled_photo)
            self.lblPhoto.setPixmap(scaled_photo)
        else:
            scaled_photo = photo.scaledToHeight(280, 0)
            print("Scaled to Height")
            self.lblPhotoSelected.setPixmap(scaled_photo)
            self.lblPhoto.setPixmap(scaled_photo)


    def write_to_db(self):
        print("ready to write to db")
        state_name = self.txtStateName.text()
        print(state_name)
        capitol_name = self.txtCapitol.text()
        print(capitol_name)
        established = self.txtEstablished.text()
        print(established)
        conn = sqlite3.connect("general.db")  # Open dBase
        c = conn.cursor()  # Create Cursor
        # Write Data
        c.execute(
            "INSERT INTO states (statename, capitol, photo, established) VALUES (? ,? ,?, ?)",
            (state_name, capitol_name, self.photo_BLOB, established),
        )
        conn.commit()  # Save Write
        conn.close()  # Close connection

        # Loading results to Home Page
        self.lblStateName.setText(state_name)
        self.lblCapitol.setText(capitol_name)
        self.lblEstablished.setText(established)
        #self.current_index = self.current_index + 1
        self.current_index = get_db_length(self)
        self.lblCurrentIndex.setText(str(self.current_index))

    #     # Display Home Page
        self.tab.setCurrentIndex(0)

        # Clearing Input boxes
        self.txtStateName.clear()
        self.txtCapitol.clear()
        self.txtEstablished.clear()
        self.lblPhotoSelected.clear()

    def index_forward(self):
        print("Will advance index by 1")
        eDb = get_db_length(self)
        if self.current_index >= eDb:
            self.current_index == eDb
            print("Already at the last record")
            popup_Critical(self,"At the last Record")
        else:
            self.current_index = int(self.current_index) + 1
            self.lblCurrentIndex.setText(str(self.current_index))
            #print(self.current_index)
            self.get_random_record()

    def index_back(self):
        print("Will back up index by 1")
        if self.current_index <= 1:  # Test to stay in range of available records
            self.current_index == 1
            print("At the First record")
            popup_Critical(self,"At the first Record")
        else:
            self.current_index = int(self.current_index) - 1
            self.lblCurrentIndex.setText(str(self.current_index))
            #print(self.current_index)
            self.get_random_record()


    def get_random_index(self):
        min_value = 1 
        max_value = get_db_length(self)
        print(max_value)
        self.current_index = random.randint(min_value, max_value)
        #self.lblCurrentIndex.setText(str(self.current_index))
        print(f"The Random number is {self.current_index}")
        self.get_random_record()



    def get_random_record(self):
        print(f"The random generated current index is {self.current_index}")
        conn = sqlite3.connect("general.db")  # Open dBase
        c = conn.cursor()  # Create Cursor
        c.execute(f"SELECT * FROM states WHERE id ='{self.current_index}'")  
        rlist = c.fetchone()
        conn.commit()  # Save Write
        conn.close()  # Close connection
        #print(rlist)
        print(f"{rlist[0]}, {rlist[1]}, {rlist[2]}, {rlist[4]}")
        self.lblStateName.setText(rlist[1])
        self.lblCapitol.setText(f"The Capitol is {rlist[2]}")
        self.lblEstablished.setText(f"Became a State in {str(rlist[4])}")
        self.rPicture = rlist[3]
        
        self.display_db_pic()  # Displays picture received from dB request
        # Updates displayed current index in home page
        self.lblCurrentIndex.setText(str(self.current_index))

        self.tab.setCurrentIndex(0)  # Returns to home page

    
    def go_search(self):
        self.current_index = int(self.txtSearchIndex.text())  # Get index to display
        print(self.current_index)
        print(type(self.current_index))
    #     # Clear search index box for next search
    #     self.txtSearchIndex.clear() 
        self.get_random_record()  # Display the requested record
        self.pteSearchResults.clear() # Clearing results from previous search

    
    def display_db_pic(self):
        print("Will display picture in results page")
        out_pic = QImage.fromData(self.rPicture)  # Create the image from BLOB data
        photo = QPixmap.fromImage(out_pic)  # Create a Pixmap object
        picHeight = photo.height()
        print(f"The PicHeight is {picHeight}")
        picWidth = photo.width()
        print(f"The PicWidth is {picWidth}")
        print(type(picWidth))
        # Scaling the picture for the display box
        if picWidth > picHeight:
            scaled_photo = photo.scaledToWidth(375, 0)
            print("scaled by width")
        else:
            scaled_photo = photo.scaledToHeight(375, 0)
            print("scaled by Heigth")

        self.lblPhoto.setPixmap(scaled_photo)


    def search_state_name(self):
        print("Searching through state names")
        self.pteSearchResults.clear()
        conn = sqlite3.connect("general.db")  # Opening dB for reading
        c = conn.cursor()
        state_name_search = self.txtSearchStateName.text()
        
        c.execute(
            "SELECT * FROM states WHERE statename LIKE (?) ", (state_name_search + "%",)
        )

        items = c.fetchall()
        for item in items:
            # Send results to output window
            self.pteSearchResults.appendPlainText((f"{item[0]} - {item[1]}"))
        self.txtSearchStateName.clear()

        conn.commit()
        conn.close()
        

    def closeEvent(self, *args, **kwargs):
        # print("Program closed Successfully!")
        self.close()


# Initialize the App
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()
