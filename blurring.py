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
from qgis.gui import QgsMessageBar
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from blurringdialog import BlurringDialog
import os.path
import random
import math
import ntpath
import time


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

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/plugins/blurring/icon.png"),
            u"Blurring", self.iface.mainWindow())
        # connect the action to the run method
        self.action.triggered.connect(self.run)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"&Bord", self.action)
        
        #Variables
        self.mapLayerRegistry = QgsMapLayerRegistry.instance()
        
        #Connecteurs
        QObject.connect(self.dlg.pushButton_help, SIGNAL("clicked()"), self.displayHelp)
        QObject.connect(self.dlg.pushButton_browseFolder, SIGNAL('clicked()'), self.selectFile)
        QObject.connect(self.dlg.pushButton_ok, SIGNAL("clicked()"), self.compute)
        QObject.connect(self.dlg.pushButton_cancel, SIGNAL("clicked()"), self.cancel)
        
        QObject.connect(QgsMapLayerRegistry.instance(), SIGNAL("layerRemoved(QString)"), self.layerDeleted)
        QObject.connect(QgsMapLayerRegistry.instance(), SIGNAL("layerWasAdded(QgsMapLayer*)"), self.layerAdded)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&Blurring", self.action)
        self.iface.removeToolBarIcon(self.action)

    def displayComboBoxLayers(self):
        self.layers = self.iface.legendInterface().layers()
        self.dlg.comboBox_blurredLayer.clear()
        self.dlg.progressBar_progression.setValue(0)

        """Remplissage du menu déroulant"""
        for layer in self.layers:
            if layer.LayerType() == 0 and layer.geometryType() == 0 :
                self.dlg.comboBox_blurredLayer.addItem(layer.name())
                 
        if self.dlg.comboBox_blurredLayer.count() < 1:
            self.dlg.pushButton_ok.setEnabled(False)
        else:
            self.dlg.pushButton_ok.setEnabled(True)

    def run(self):
        self.displayComboBoxLayers()
        self.outputFile = ""
        self.dlg.lineEdit_outputFile.setText("")
        self.dlg.show()
        
        result = self.dlg.exec_()
        if result == 1:
            self.calculation()

    def selectFile(self):
        outputFile = QFileDialog.getSaveFileName(self.dlg, 'Select file','output',"Shapefiles (*.shp)")
        if outputFile:
            self.dlg.lineEdit_outputFile.setText(outputFile)
        else:
            self.dlg.lineEdit_outputFile.setText('')

    def compute(self):
                
        """Bar de progression a 0"""
        self.dlg.progressBar_progression.setValue(0)
        
        """Recuperation des champs du formulaire"""
        layerName = self.dlg.comboBox_blurredLayer.currentText()
        radius = self.dlg.spinBox_radius.value()
        display = self.dlg.checkBox_addToMap.isChecked()
        selectedFeaturesOnly = self.dlg.checkBox_selectedFeatures.isChecked()
        fileName = self.dlg.lineEdit_outputFile.text()
        
        if fileName == "" and display == False:
            self.iface.messageBar().pushMessage(self.dlg.tr(u'No file provided, "add resultat to canvas" required'), level=QgsMessageBar.CRITICAL , duration=5)
            return
        
        self.polygonBufferFinalLayer = None
        self.fileWriter = None
        
        """Recuperation de la couche"""
        layer = self.mapLayerRegistry.mapLayersByName(layerName)[0]
        fields = layer.pendingFields()
        crsMapRenderer = self.iface.mapCanvas().mapRenderer().destinationCrs()
        crsLayer = layer.crs()
        
        if crsMapRenderer.mapUnits() != 0 or crsLayer.mapUnits() != 0:
            self.iface.messageBar().pushMessage(self.dlg.tr(u'The projection of the map or of the layer is not in meters. These parameters should be in meters.'), level=QgsMessageBar.CRITICAL , duration=5)
            return

        """Creation de la couche polygonale"""

        if fileName != "":
            self.fileWriter = QgsVectorFileWriter(fileName, None, fields, QGis.WKBPolygon, crsLayer, "ESRI Shapefile")
            if self.fileWriter.hasError() != QgsVectorFileWriter.NoError:
                print "Error when creating shapefile: ", self.fileWriter.hasError()
        else :
            self.polygonBufferFinalLayer = QgsVectorLayer("Polygon",self.dlg.tr(u"Final buffer " + str(radius) + " m"), "memory")
            self.dataProviderPolygonBufFinalLayer = self.polygonBufferFinalLayer.dataProvider()
            self.dataProviderPolygonBufFinalLayer.addAttributes(list(fields))
            self.polygonBufferFinalLayer.startEditing()
        
        """Uniquement entités selectionnées ?"""
        features = None
        nbFeatures = None
        if selectedFeaturesOnly:
            features = layer.selectedFeatures()
            nbFeatures = layer.selectedFeatureCount()
        else:
            features = layer.getFeatures()
            nbFeatures = layer.featureCount()
        
        """Iteration sur la couche ponctuelle"""
        for i,feature in enumerate(features):
            
            """Recuperation de la geom et des attributs"""
            geom = feature.geometry()
            attrs = feature.attributes()
            
            """Tirage du point aleatoire"""
            teta = math.pi*random.uniform(0, 2)
            deltaX = random.randint(0,radius)
            deltaY = random.randint(0,radius)
            randomX = geom.asPoint().x()+ deltaX * math.cos(teta)
            randomY = geom.asPoint().y()+ deltaY * math.sin(teta)
            
            """Creation du point aleatoire"""
            pointAleaGeom = QgsGeometry.fromPoint(QgsPoint(randomX, randomY))
            
            """Creation du buffer final"""
            bufferGeom2 = pointAleaGeom.buffer(radius,0.5)
            bufferFeature2 = QgsFeature()
            bufferFeature2.setGeometry(bufferGeom2)
            bufferFeature2.setAttributes(attrs)
            
            """Ajout a la couche du buffer2"""
            if fileName != "":
                self.fileWriter.addFeature(bufferFeature2)
            else :
                self.polygonBufferFinalLayer.dataProvider().addFeatures([bufferFeature2])
            
            """Maj de la bar de progression"""
            percent =int((i+1)*100/nbFeatures)
            self.dlg.progressBar_progression.setValue(percent)
        
        """Validation des changements et ajout de la couche à la carte""" 
        if fileName == "":
            self.polygonBufferFinalLayer.commitChanges()
        else :
            del self.fileWriter
        
        if display:
            
            self.settings = QSettings()
            self.oldDefaultProjection = self.settings.value("/Projections/defaultBehaviour")
            self.settings.setValue( "/Projections/defaultBehaviour", "useProject")
            
            if fileName != "":
                layerName = ntpath.basename(fileName)
                self.newlayer = QgsVectorLayer(fileName, layerName,"ogr")
                self.newlayer.commitChanges()
                self.newlayer.clearCacheImage()
                QgsMapLayerRegistry.instance().addMapLayers([self.newlayer])
            else:
                QgsMapLayerRegistry.instance().addMapLayer(self.polygonBufferFinalLayer)
                
            self.settings.setValue( "/Projections/defaultBehaviour", self.oldDefaultProjection) 
                   
        self.dlg.hide()
        
        if fileName != "":
            self.iface.messageBar().pushMessage(self.dlg.tr(u"Successful export in " + layerName), level=QgsMessageBar.INFO , duration=5)
        else:
            self.iface.messageBar().pushMessage(self.dlg.tr(u"Succesfully done !"), level=QgsMessageBar.INFO , duration=5)

    def displayHelp(self):
        msg = self.dlg.tr(u"Plugin QGIS pour le floutage des données ponctuelles. <br /> <b>Bientôt, l'aide !</b>")
        infoString = QCoreApplication.translate('Blurring', msg)
        QMessageBox.information(self.dlg,u"Blurring", infoString)
        
    def cancel(self):
        self.dlg.hide()
        
    def layerDeleted(self,idLayer):
        self.displayComboBoxLayers()
        
    def layerAdded(self,idLayer):
        #time.sleep(2)
        self.displayComboBoxLayers()