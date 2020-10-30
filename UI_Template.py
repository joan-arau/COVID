import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic

import pyqtgraph as pg
from PyQt5.QtWidgets import *

import pandas as pd
from covid import main as c
from covid import Covid

covid = Covid()
api = c.CovId19Data()

import matplotlib
import geopandas
import plotly.express as px

# path = os.path.dirname(__file__) #uic paths from itself, not the active dir, so path needed
qtCreatorFile = "/Users/joan/PycharmProjects/COVID/Ui.ui"  # Ui file name, from QtDesigner, assumes in same folder as this .py

ui, QtBaseClass = uic.loadUiType(qtCreatorFile)  # process through pyuic



class MyApp1(QMainWindow, ui):  # gui class
    def __init__(self):
        # The following sets up the gui via Qt
        super(MyApp1, self).__init__()

        self.setupUi(self)



def Cov_ui():
    app = QApplication(sys.argv)  # instantiate a QtGui (holder for the app)


    window = MyApp1()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    Cov_ui()