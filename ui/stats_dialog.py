# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QuickOSM
                                 A QGIS plugin
 OSM's Overpass API frontend
                             -------------------
        begin                : 2014-06-11
        copyright            : (C) 2014 by 3Liz
        email                : info at 3liz dot com
        contributor          : Etienne Trimaille
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from Blurring import *
from stats import Ui_Form
import os
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
import matplotlib.pyplot as plt

class StatsWidget(QWidget, Ui_Form):
    
    #Signal new query
    signalPercentage = pyqtSignal(int, name='signalPercentage')
    
    def __init__(self, parent=None):
        super(StatsWidget, self).__init__()
        self.setupUi(self)
        self.fillComboxboxLayers()
        self.label_progressStats.setText("")
        
        self.pushButton_refreshLayers.clicked.connect(self.fillComboxboxLayers)
        self.buttonBox_stats.button(QDialogButtonBox.Ok).clicked.connect(self.runStats)
        self.buttonBox_stats.button(QDialogButtonBox.Cancel).clicked.connect(self.hide)
        
        # a figure instance to plot on
        self.figure = plt.figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.layout_plot.addWidget(self.toolbar)
        self.layout_plot.addWidget(self.canvas)
        
    def hide(self):
        iface.Blurring_mainWindowDialog.hide()

    def fillComboxboxLayers(self):
        self.comboBox_blurredLayer.clear()
        self.comboBox_statsLayer.clear()

        for layer in iface.legendInterface().layers():
            if layer.type() == 0 :
                self.comboBox_statsLayer.addItem(layer.name(),layer)
                
                if layer.geometryType() == 2 :
                    self.comboBox_blurredLayer.addItem(layer.name(),layer)
    
    
    def plot(self,data):
        # create an axis
        ax = self.figure.add_subplot(111)
        # discards the old graph
        ax.hold(False)
        # plot data
        ax.plot(data, '*-')
        # refresh canvas
        self.canvas.draw()

    def runStats(self):
        self.progressBar_stats.setValue(0)
        self.label_progressStats.setText("")
        QApplication.processEvents()
        
        index = self.comboBox_blurredLayer.currentIndex()
        layerBlurred = self.comboBox_blurredLayer.itemData(index)
        
        index = self.comboBox_statsLayer.currentIndex()
        layerStats = self.comboBox_statsLayer.itemData(index)
        
        if layerBlurred == layerStats:
            return False
        
        if not layerBlurred or not layerStats:
            return False
        
        nbFeatureBlurred = layerBlurred.featureCount()
        
        featuresStats = {feature.id(): feature for (feature) in layerStats.getFeatures()}
        nbFeatureStats = layerStats.featureCount()
        print nbFeatureStats
        
        print "index"
        self.label_progressStats.setText("Creating index")
        QApplication.processEvents()
        index = QgsSpatialIndex()
        for i,f in enumerate(layerStats.getFeatures()):
            index.insertFeature(f)
            percent = int(100 / nbFeatureStats * (i+1))
            self.progressBar_stats.setValue(percent)
            QApplication.processEvents()
        
        tab = []
        print "calculating"
        self.label_progressStats.setText("Calculating")
        QApplication.processEvents()
        for i,feature in enumerate(layerBlurred.getFeatures()):
            count = 0
            ids = index.intersects(feature.geometry().boundingBox())
            for id in ids:
                f = featuresStats[id]
                if f.geometry().intersects(feature.geometry()):
                    count += 1
            tab.append(count)
        
        tab.sort()
        print tab
        
        self.tableWidget.setRowCount(3)
        
        self.tableWidget.setItem(0, 0, QTableWidgetItem(str("Min")))
        nb = tab[0]
        self.tableWidget.setItem(0, 1, QTableWidgetItem(str(nb)))
        
        self.tableWidget.setItem(1, 0, QTableWidgetItem(str("Average")))
        nb = sum(tab)/nbFeatureBlurred
        self.tableWidget.setItem(1, 1, QTableWidgetItem(str(nb)))
        
        self.tableWidget.setItem(2, 0, QTableWidgetItem(str("Max")))
        nb = tab[-1]
        self.tableWidget.setItem(2, 1, QTableWidgetItem(str(nb)))
        
        self.tableWidget.resizeRowsToContents()
        self.plot(tab)
        
        
class StatsDockWidget(QDockWidget):
    def __init__(self, parent=None):
        QDockWidget.__init__(self)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.setWidget(StatsWidget())
        self.setWindowTitle(Tools.trans("Blurring - Stats"))