import os
from PyQt5 import QtCore, QtGui
#from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QAction, QLineEdit, QMessageBox

# Simple function that multiplies numbers
# Ex.	answer=survey.Mulitply(float(a), float(b))

def Multiply(a,b):
    return a * b

def askQuestion(callingClass,myTitle,myMessage):
    reply = QtGui.QMessageBox.question(callingClass, myTitle,
                     myMessage, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
    if reply==QtGui.QMessageBox.Yes:
        myreply=True
    else:
        myreply=False
    return myreply
    print(myreply)


def popup_Critical(self, inMessage):
    msg = QMessageBox()
    msg.setWindowTitle("Critial Error has occured")
    #msg.setText("Wrong Number")
    msg.setText(inMessage)
    msg.setIcon(QMessageBox.Critical)

    x = msg.exec_()


def popup_Question(self, myTitle, myMessage):
    msg = QMessageBox()
    msg.setWindowTitle(myTitle)
    msg.setText(myMessage)
    msg.setIcon(QMessageBox.Question)
    msg.setStandardButtons(QMessageBox.Yes|QMessageBox.No|QMessageBox.Cancel)

    """
    Button Options

    QMessageBox.Ok, QMessageBox.Open, QMessageBox.Save, QMessageBox.Cancel

    QMessageBox.Close, QMessageBox.Yes, QMessageBox.No, QMessageBox.Abort

    QMessageBox.Retry, QMessageBox.Ignore

    """

    msg.setDefaultButton(QMessageBox.Cancel) # Set default button

    msg.setInformativeText("This is informative text here") # More text can be entered

    msg.setDetailedText("This is the detailed text") #Adds a more text option

    msg.buttonClicked.connect(which_Button)
    #msg.buttonClicked.connect(which_Button)


    x = msg.exec_()


def popup_Warning(self, inMessage):
    msg = QMessageBox()
    msg.setWindowTitle("Warning Error has occured")
    #msg.setText("Wrong Number")
    msg.setText(inMessage)
    msg.setIcon(QMessageBox.Warning)

    x = msg.exec_()

def which_Button(i):
    pass    #will return which button was clicked
    #print(i)
    print(i.text())
    return i.text()