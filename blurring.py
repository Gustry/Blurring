# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Blurring
                                 A QGIS plugin
 Blurring data
                              -------------------
        begin                : 2014-03-11
        copyright            : (C) 2014 by TER Géomatique UM2
        email                : ter-floutage@googlegroups.com
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
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
# Initialize Qt resources from file resources.py
import resources
import LayerIndex
# Import the code for the dialog
from blurringdialog import BlurringDialog
from BlurringAlgorithmCore import BlurringAlgorithmCore
import os.path
import sys
import random
import math
import ntpath
import inspect
import re

from processing.core.Processing import Processing
from processing.tools.system import *
from processing.core.GeoAlgorithmExecutionException import GeoAlgorithmExecutionException
from BlurringAlgorithmProvider import BlurringAlgorithmProvider
cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]

if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

class Blurring:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(self.plugin_dir, 'i18n', 'blurring_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = BlurringDialog()
        self.provider = BlurringAlgorithmProvider()

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/resources/icon"),
            u"Blurring", self.iface.mainWindow())
        # connect the action to the run method
        self.action.triggered.connect(self.run)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToVectorMenu(u"&Blurring", self.action)
        
        #Variables
        self.mapLayerRegistry = QgsMapLayerRegistry.instance()
        
        #Height and widht
        self.minWidth = 416
        self.maxWidth = 786
        self.height = 364
        
        #Connecteurs
        QObject.connect(self.dlg.checkBox_envelope, SIGNAL("clicked()"), self.enableEnvelope)
        QObject.connect(self.dlg.pushButton_help, SIGNAL("clicked()"), self.displayHelp)
        QObject.connect(self.dlg.pushButton_browseFolder, SIGNAL('clicked()'), self.selectFile)
        QObject.connect(self.dlg.pushButton_ok, SIGNAL("clicked()"), self.compute)
        QObject.connect(self.dlg.pushButton_cancel, SIGNAL("clicked()"), self.cancel)
        QObject.connect(self.dlg.pushButton_advanced, SIGNAL("clicked()"), self.advanced)
        
        QObject.connect(QgsMapLayerRegistry.instance(), SIGNAL("layerRemoved(QString)"), self.layerDeleted)
        QObject.connect(QgsMapLayerRegistry.instance(), SIGNAL("layerWasAdded(QgsMapLayer*)"), self.layerAdded)
        
        Processing.addProvider(self.provider, True)

    def unload(self):
        self.iface.removePluginVectorMenu(u"&Blurring", self.action)
        self.iface.removeToolBarIcon(self.action)
        Processing.removeProvider(self.provider)
            
    def enableEnvelope(self):
        if self.dlg.checkBox_envelope.isChecked():
            self.dlg.comboBox_envelope.setEnabled(True)
        else:
            self.dlg.comboBox_envelope.setEnabled(False)

    def advanced(self):
        if re.search('<<<', self.dlg.pushButton_advanced.text()):
            self.dlg.resize(self.minWidth,self.height)
            self.dlg.checkBox_envelope.setChecked(False)
            self.enableEnvelope()
            self.dlg.checkBox_exportCentroid.setChecked(False)
            self.dlg.checkBox_exportRadius.setChecked(False)
            self.dlg.checkBox_exportDistance.setChecked(False)
            self.dlg.pushButton_advanced.setText(QApplication.translate("Blurring", 'More options     >>>'))
        else:
            self.dlg.resize(self.maxWidth, self.height)
            self.dlg.pushButton_advanced.setText(QApplication.translate("Blurring", 'Less options     <<<'))

    def displayComboBoxLayers(self):
        self.layers = self.iface.legendInterface().layers()
        self.dlg.comboBox_blurredLayer.clear()
        self.dlg.comboBox_envelope.clear()
        self.dlg.progressBar_progression.setValue(0)

        """Remplissage du menu déroulant"""
        for layer in self.layers:
            if layer.type() == 0 :
                if layer.geometryType() == 0 :
                    self.dlg.comboBox_blurredLayer.addItem(layer.name())
                
                if layer.geometryType() == 2 :
                    self.dlg.comboBox_envelope.addItem(layer.name())
                 
        if self.dlg.comboBox_blurredLayer.count() < 1:
            self.dlg.pushButton_ok.setEnabled(False)
        else:
            self.dlg.pushButton_ok.setEnabled(True)

    def run(self):
            
        self.dlg.checkBox_envelope.setEnabled(True)
        self.dlg.checkBox_envelope.setChecked(False)
        self.enableEnvelope()
        
        self.displayComboBoxLayers()
        self.outputFile = ""
        self.dlg.lineEdit_outputFile.setText("")
        self.dlg.show()

    def selectFile(self):
        outputFile = QFileDialog.getSaveFileName(self.dlg, QApplication.translate("Blurring", 'Select file'),'output',"Shapefiles (*.shp)")
        if outputFile:
            self.dlg.lineEdit_outputFile.setText(outputFile)
        else:
            self.dlg.lineEdit_outputFile.setText('')

    def compute(self):
        """ None to advanced parameters"""
        self.layerEnvelope = None
        self.layerEnvelopeGeom = None
        self.nbMinEntities = None
        self.step = None
                
        """Bar de progression a 0"""
        self.dlg.progressBar_progression.setValue(0)
        
        """Recuperation des champs du formulaire"""
        layerName = self.dlg.comboBox_blurredLayer.currentText()
        self.radius = self.dlg.spinBox_radius.value()
        display = self.dlg.checkBox_addToMap.isChecked()
        selectedFeaturesOnly = self.dlg.checkBox_selectedFeatures.isChecked()
        self.fileName = self.dlg.lineEdit_outputFile.text()
        exportRadius = self.dlg.checkBox_exportRadius.isChecked()
        exportCentroid = self.dlg.checkBox_exportCentroid.isChecked()
        exportDistance = self.dlg.checkBox_exportDistance.isChecked()
                
        if self.dlg.checkBox_envelope.isChecked():
            self.layerEnvelope = self.mapLayerRegistry.mapLayersByName(self.dlg.comboBox_envelope.currentText())[0]
            self.layerEnvelope = LayerIndex.LayerIndex(self.layerEnvelope)
      
        if self.fileName == "":
            if display == False:
                self.iface.messageBar().pushMessage(QApplication.translate("Blurring", 'No file provided, "add resultat to canvas" required'), level=QgsMessageBar.CRITICAL , duration=5)
                return
            
            self.fileName = getTempFilenameInTempFolder("blurring.shp")
        
        if display :
            self.settings = QSettings()
            self.oldDefaultProjection = self.settings.value("/Projections/defaultBehaviour")
            self.settings.setValue( "/Projections/defaultBehaviour", "useProject")
        
        self.polygonBufferFinalLayer = None
        self.fileWriter = None
        
        """Recuperation de la couche"""
        layer = self.mapLayerRegistry.mapLayersByName(layerName)[0]
        fields = layer.pendingFields()
        if exportRadius:
            fields.append(QgsField(u"Radius", QVariant.Int))
        if exportCentroid:
            fields.append(QgsField(u"X centroid", QVariant.Int))
            fields.append(QgsField(u"Y centroid", QVariant.Int))
        if exportDistance:
            fields.append(QgsField(u"Distance", QVariant.Double))
        crsMapRenderer = self.iface.mapCanvas().mapRenderer().destinationCrs()
        crsLayer = layer.crs()
        
        if crsMapRenderer.mapUnits() != 0 or crsLayer.mapUnits() != 0:
            self.iface.messageBar().pushMessage(QApplication.translate("Blurring",'The projection of the map or of the layer is not in meters. These parameters should be in meters.'), level=QgsMessageBar.WARNING , duration=5)
       
        """Uniquement entités selectionnées ?"""
        features = None
        self.nbFeatures = None
              
        if selectedFeaturesOnly:
            features = layer.selectedFeatures()
            self.nbFeatures = layer.selectedFeatureCount()
        else:
            features = layer.getFeatures()
            self.nbFeatures = layer.featureCount()
        
        """Creation de la couche polygonale"""    
        self.fileWriter = QgsVectorFileWriter(self.fileName, None, fields, QGis.WKBPolygon, crsLayer, "ESRI Shapefile")
        if self.fileWriter.hasError() != QgsVectorFileWriter.NoError:
            self.iface.messageBar().pushMessage(QApplication.translate("Blurring","Error when creating shapefile: ", self.fileWriter.hasError()), level=QgsMessageBar.CRITICAL , duration=5)
            
        
        algo = BlurringAlgorithmCore.BlurringAlgorithmCore(self.radius, self.layerEnvelope, exportRadius, exportCentroid, exportDistance)
        
        for j,feature in enumerate(features):
            try:
                feature = algo.blur(feature)
            except GeoAlgorithmExecutionException as e:
                self.iface.messageBar().pushMessage(e.msg, level=QgsMessageBar.CRITICAL , duration=5)
                return
            self.fileWriter.addFeature(feature)
        
            """Maj de la bar de progression"""
            percent =int((j+1)*100/self.nbFeatures)
            self.dlg.progressBar_progression.setValue(percent)
        
            
        """Validation des changements et ajout de la couche à la carte""" 
        del self.fileWriter
            
        if display:            
            layerName = ntpath.basename(self.fileName)
            self.newlayer = QgsVectorLayer(self.fileName, layerName,"ogr")
            self.newlayer.commitChanges()
            self.newlayer.clearCacheImage()
            QgsMapLayerRegistry.instance().addMapLayers([self.newlayer])
 
            self.settings.setValue( "/Projections/defaultBehaviour", self.oldDefaultProjection) 
                   
        self.dlg.hide()
        
        self.iface.messageBar().pushMessage(QApplication.translate("Blurring", "Successful export in " + self.fileName), level=QgsMessageBar.INFO , duration=5)


    def displayHelp(self):
        infoString = QCoreApplication.translate('Blurring', u"Plugin to blur point data, such as health personal data<br /><table><tr><td><img src=':/resources/step1' /></td><td>Creating a buffer (radius r)</td></tr><tr><td><img src=':/resources/step2' /></td><td>Random selection of a point in each buffer</td></tr><tr><td><img src=':/resources/step3' /></td><td>Creating a buffer around the new point with the same radius. The initial point is at a maximal distance r of the centroid of the buffer.</td></tr></table> The envelope layer will force the algorithm to have an intersection between the centroid and this layer.")
        QMessageBox.information(self.dlg,u"Blurring", infoString)
                
    def cancel(self):
        self.dlg.hide()
        
    def layerDeleted(self,idLayer):
        self.displayComboBoxLayers()
        
    def layerAdded(self,idLayer):
        self.displayComboBoxLayers()