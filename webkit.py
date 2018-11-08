# -*- coding: utf-8 -*-
"""
Created on Sun Sep 16 14:25:19 2018

@author: yang
"""

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngine import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
 
app = QApplication(sys.argv)
 
web = QWebEngineView()
web.load(QUrl("https://pythonspot.com"))
web.show()
 
sys.exit(app.exec_())