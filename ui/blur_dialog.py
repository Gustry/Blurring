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
from blur import Ui_Form
from Blurring.CoreBlurring.Process import Process

class BlurWidget(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(BlurWidget, self).__init__()
        self.setupUi(self)
        
        self.label_progress.setText('')
        
        self.pushButton_refreshLayersToBlur.clicked.connect(self.fillComboxboxLayers)
        self.buttonBox_blur.button(QDialogButtonBox.Ok).clicked.connect(self.runBlur)
        self.buttonBox_blur.button(QDialogButtonBox.Cancel).clicked.connect(self.hide)
        
    def hide(self):
        iface.Blurring_mainWindowDialog.hide()

    def fillComboxboxLayers(self):
        self.comboBox_layerToBlur.clear()
        self.comboBox_envelope.clear()

        for layer in iface.legendInterface().layers():
            if layer.type() == 0 :
                if layer.geometryType() == 0 :
                    self.comboBox_layerToBlur.addItem(layer.name(),layer)
                
                if layer.geometryType() == 2 :
                    self.comboBox_envelope.addItem(layer.name(),layer)
        
    def runBlur(self):
        
        self.progressBar_blur.setValue(0)
        
        """Get all the fields"""
        index = self.comboBox_layerToBlur.currentIndex()
        layerToBlur = self.comboBox_layerToBlur.itemData(index)
        radius = self.spinBox_radius.value()
        display = self.checkBox_addToMap.isChecked()
        selectedFeaturesOnly = self.checkBox_selectedOnlyFeatures.isChecked()
        fileName = self.lineEdit_outputFile.text()
        exportRadius = self.checkBox_exportRadius.isChecked()
        exportCentroid = self.checkBox_exportCentroid.isChecked()
        
        layerEnvelope = None
        if self.checkBox_envelope.isChecked():
            index = self.comboBox_envelope.currentIndex()
            layerEnvelope = self.comboBox_envelope.itemData(index)
        
        #Test values
        try:
            if not layerToBlur:
                raise NoLayerProvidedException
            
            if not fileName and not display:
                raise NoFileNoDisplayException
            
            if layerToBlur.crs().mapUnits() != 0:
                Tools.displayMessageBar(msg=Tools.trans('The projection of the map or of the layer is not in meters. These parameters should be in meters.'), level=QgsMessageBar.WARNING , duration=5)
            
            Process.blurProcess(dialog=self,
                        layerToBlur=layerToBlur,
                        radius=radius,
                        display=display,
                        selectedFeaturesOnly=selectedFeaturesOnly,
                        fileName=fileName,
                        layerEnvelope=layerEnvelope,
                        exportRadius=exportRadius,
                        exportCentroid=exportCentroid)
            
            self.hide()
        
        except BlurringException,e:
            self.label_progress.setText("")
            Tools.displayMessageBar(msg=e.msg, level=e.level , duration=e.duration)
        
        finally:
            QApplication.restoreOverrideCursor()
            QApplication.processEvents()
        
class BlurDockWidget(QDockWidget):
    def __init__(self, parent=None):
        QDockWidget.__init__(self)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.setWidget(BlurWidget())
        self.setWindowTitle(Tools.trans("Blurring - Blur"))