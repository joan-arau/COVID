import sys
import os
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic
import qdarkstyle
from pyqtgraph import PlotWidget, plot
from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import pyqtgraph.opengl as gl
from IPython.display import HTML, display
from scipy.interpolate import griddata
import numpy as np
import pandas as pd
from covid import main as c
from covid import Covid
covid = Covid()
api = c.CovId19Data()
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import webbrowser
import folium

from IPython.core.display import HTML
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('QT5Agg')

import geopandas
import plotly.express as px


# path = os.path.dirname(__file__) #uic paths from itself, not the active dir, so path needed
qtCreatorFile = "/Users/joan/PycharmProjects/COVID/Ui.ui" #Ui file name, from QtDesigner, assumes in same folder as this .py

ui, QtBaseClass = uic.loadUiType(qtCreatorFile) #process through pyuic


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self):

        super(MyApp1, self).__init__()





        self.setupUi(self)




class MyApp1(QMainWindow,  ui): #gui class
    def __init__(self):
        #The following sets up the gui via Qt
        super(MyApp1, self).__init__()

        self.setupUi(self)

        self.pushButton_3.clicked.connect(self.close)
        self.countries = api.show_available_countries()
        print(self.countries)


        self.comboBox_2.addItems(['Line','Change'])
        self.comboBox_2.setCurrentIndex(0)

        self.comboBox_3.addItems(['All', 'Confirmed','Deaths','Recovered'])
        self.comboBox_3.setCurrentIndex(0)

        country = 'Germany'
        self.comboBox.addItems(self.countries)
        self.comboBox.setCurrentIndex(self.countries.index(country))
        country = country.lower()

        self.comboBox_4.addItems(['None']+self.countries)
        self.comboBox_4.setCurrentIndex(0)

        self.pushButton.clicked.connect(self.world_map)
        # print(h.dtypes)

        # plt.plot(pd.to_datetime(h['date']), h['confirmed'].astype(int))
        # plt.show()

        # self.rows = 1
        # self.row_dic = {}


        self.plotter(self.comboBox_2.currentText(),[country],'all')

        self.pushButton_2.clicked.connect(self.go)
        # self.pushButton.clicked.connect(self.new_row)
        # self.row_dic[0] = {'+': self.pushButton, 'count': self.comboBox}

    def go(self):

        if self.comboBox_4.currentText() == 'None':
            self.plotter(self.comboBox_2.currentText(), [self.comboBox.currentText().lower()],self.comboBox_3.currentText().lower())
        else:
            self.plotter(self.comboBox_2.currentText(), [self.comboBox.currentText().lower(),self.comboBox_4.currentText().lower()],
                         self.comboBox_3.currentText().lower())
    def plotter(self,mode,countries,show):
        self.graphWidget = pg.PlotWidget()
        self.graph.addWidget(self.graphWidget, 0, 0)
        self.graphWidget.showGrid(x=True, y=True)
        self.graphWidget.addLegend()
        if len(countries) == 1:
            h = api.get_history_by_country(countries[0])

              # .drop(['change_confirmed', 'change_deaths', 'change_recovered'], axis=1)
            # print(h)
            h = pd.DataFrame.from_dict(h[countries[0]]['history']).T.reset_index().rename(columns={'index': 'date'},
                                                                                          inplace=False)

            print(mode)
            if mode == 'Line':
                if show == 'all':
                    self.graphWidget.plot(h.index, h['confirmed'].astype(float), pen=pg.mkPen('y', width=3),name = 'Confirmed')
                    self.graphWidget.plot(h.index, h['deaths'].astype(float), pen=pg.mkPen('r', width=3),name = 'Deaths')
                    self.graphWidget.plot(h.index, h['recovered'].astype(float), pen=pg.mkPen('g', width=3),name = 'Recovered')
                else:
                    self.graphWidget.plot(h.index, h[show].astype(float), pen=pg.mkPen(width=3))
            else:
                if show == 'all':
                # h[['change_confirmed','change_deaths','change_recovered']] = h[['change_confirmed','change_deaths','change_recovered']].fillna(0)
                    print(h['confirmed'].diff().astype(float).dropna().reset_index(drop=True))
                    self.graphWidget.plot(h.index[:-1], h['confirmed'].diff().astype(float).dropna().reset_index(drop=True), pen=pg.mkPen('y', width=3))
                    self.graphWidget.plot(h.index[:-1], h['deaths'].diff().astype(float).dropna().reset_index(drop=True), pen=pg.mkPen('r', width=3))
                    self.graphWidget.plot(h.index[:-1], h['recovered'].diff().astype(float).dropna().reset_index(drop=True), pen=pg.mkPen('g', width=3))
                else:
                    self.graphWidget.plot(h.index[:-1],
                                          h[show].diff().astype(float).dropna().reset_index(drop=True),
                                          pen=pg.mkPen(width=3))

        else:
            if show == 'all':
                show = 'confirmed'
               
            if show != 'all':
                x = 0
                colors = ['y','g']
                for i in countries:

                    h = api.get_history_by_country(i)
                    h = pd.DataFrame.from_dict(h[i]['history']).T.reset_index().rename(
                        columns={'index': 'date'},
                        inplace=False)
                    self.graphWidget.plot(h.index, h[show].astype(float), pen=pg.mkPen(colors[x],width=3),name = i)

                    x+=1

    def world_map(self):
        df =pd.DataFrame(covid.get_data()).dropna()
        print(df)

        gdf = geopandas.GeoDataFrame(
            df, geometry=geopandas.points_from_xy(df.longitude, df.latitude))

        pd.set_option('display.max_columns', None)
        print(gdf)
        # gdf = px.data.gapminder().query("year == 2007")
        # print(gdf)

        if self.comboBox_3.currentText().lower() == 'all':
            show = 'confirmed'
        else:
            show = self.comboBox_3.currentText().lower()

        fig = px.scatter_geo(gdf, lat=gdf.geometry.y,
                             lon=gdf.geometry.x,
                             color=show,  # which column to use to set the color of markers
                             hover_name="country",  # column added to hover information
                             size=show,  # size of markers
                             )
        # fig = px.density_mapbox(gdf, lat=gdf.geometry.y,
        #                      lon=gdf.geometry.x,
        #                        # which column to use to set the color of markers
        #                      radius = 10,  # column added to hover information
        #                       z=show,# size of markers
        #                      )
        fig.update(layout_showlegend=False)
        fig.show()


        # Save it as html



    # def new_row(self):
    #     # print('Clicked')
    #
    #     self.new_row_btn = QPushButton('+', self)
    #     self.gridLayout_2.addWidget(self.new_row_btn)
    #     self.new_row_btn.clicked.connect(self.new_row)
    #
    #     #countries
    #     self.count = QtWidgets.QComboBox(self.centralwidget)
    #     self.count.addItems(self.countries)
    #     self.gridLayout_2.addWidget(self.count)
    #
    #
    #     self.remove_row_btn = QPushButton('-', self)
    #
    #     self.gridLayout_2.addWidget(self.remove_row_btn)
    #
    #
    #
    #
    #
    #     # print(self.row_dic)
    #
    #     self.remove_row_btn.clicked.connect(lambda _, r=self.rows: self.remove_row(r))
    #
    #     self.row_dic[self.rows]={'+':self.new_row_btn,'count':self.count,'-':self.remove_row_btn}
    #     print(self.row_dic)
    #
    #     self.rows += 1
    #
    #
    #     self.show()
    #
    # def remove_row(self, r):
    #
    #     # print(self.row_dic[r])
    #     # print('row: ', r)
    #
    #     for item in self.row_dic[r].values():
    #         item.setParent(None)
    #
    #     del self.row_dic[r]
    #
    #     self.rows -= 1



def Cov_ui():
    app = QApplication(sys.argv) #instantiate a QtGui (holder for the app)


    # global window
    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    window = MyApp1()
    window.show()
    sys.exit(app.exec_())
    # return window

if __name__ == "__main__":
    Cov_ui()