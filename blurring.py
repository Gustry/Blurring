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
import PointInLayer
# Import the code for the dialog
from blurringdialog import BlurringDialog
import os.path
import sys
import random
import math
import ntpath
import inspect

from processing.core.Processing import Processing
from BlurringGeoAlgorithmProvider import BlurringGeoAlgorithmProvider
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
        self.provider = BlurringGeoAlgorithmProvider()

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
        
        #Connecteurs
        QObject.connect(self.dlg.checkBox_useMinNumberEntities, SIGNAL("clicked()"), self.enableMinEntities)
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

    def enableMinEntities(self):
        if self.dlg.checkBox_useMinNumberEntities.isChecked():
            self.dlg.spinBox__minEntities.setEnabled(True)
            self.dlg.comboBox_layerMinEntities.setEnabled(True)
            self.dlg.spinBox_step.setEnabled(True)
            self.dlg.label_layer_entities.setEnabled(True)
            self.dlg.label_nb_entities.setEnabled(True)
            self.dlg.label_step.setEnabled(True)
        else:
            self.dlg.spinBox__minEntities.setEnabled(False)
            self.dlg.comboBox_layerMinEntities.setEnabled(False)
            self.dlg.spinBox_step.setEnabled(False)
            self.dlg.label_layer_entities.setEnabled(False)
            self.dlg.label_nb_entities.setEnabled(False)
            self.dlg.label_step.setEnabled(False)
            
    def enableEnvelope(self):
        if self.dlg.checkBox_envelope.isChecked():
            self.dlg.comboBox_envelope.setEnabled(True)
        else:
            self.dlg.comboBox_envelope.setEnabled(False)

    def advanced(self):
        if self.dlg.pushButton_advanced.text() == "Less options     <<<":
            self.dlg.resize(355,275)
            self.dlg.checkBox_envelope.setChecked(False)
            self.dlg.checkBox_useMinNumberEntities.setChecked(False)
            self.enableEnvelope()
            self.enableMinEntities()
            self.dlg.pushButton_advanced.setText("More options     >>>")
        else:
            self.dlg.resize(665, 275)
            self.dlg.pushButton_advanced.setText("Less options     <<<")

    def displayComboBoxLayers(self):
        self.layers = self.iface.legendInterface().layers()
        self.dlg.comboBox_blurredLayer.clear()
        self.dlg.comboBox_envelope.clear()
        self.dlg.comboBox_layerMinEntities.clear()
        self.dlg.progressBar_progression.setValue(0)

        """Remplissage du menu déroulant"""
        for layer in self.layers:
            if layer.type() == 0 :
                if layer.geometryType() == 0 :
                    self.dlg.comboBox_blurredLayer.addItem(layer.name())
                
                if layer.geometryType() == 2 :
                    self.dlg.comboBox_envelope.addItem(layer.name())
                
                self.dlg.comboBox_layerMinEntities.addItem(layer.name())
                 
        if self.dlg.comboBox_blurredLayer.count() < 1:
            self.dlg.pushButton_ok.setEnabled(False)
        else:
            self.dlg.pushButton_ok.setEnabled(True)

    def run(self):
        
        self.dlg.checkBox_useMinNumberEntities.setChecked(False)
        self.dlg.checkBox_useMinNumberEntities.setEnabled(False)
        self.enableMinEntities()
        
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

    def displayPoly(self,geom, name):
        vl = QgsVectorLayer("Polygon",name, "memory")
        pr = vl.dataProvider()
        ft = QgsFeature()
        ft.setGeometry(geom)
        pr.addFeatures([ft])
        vl.updateExtents()
        QgsMapLayerRegistry.instance().addMapLayer(vl)


    def compute(self):
        """ None to advanced parameters"""
        self.layerEnvelope = None
        self.layerEnvelopeGeom = None
        self.layerMinEntities = None
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
        
        print self.radius
        
        if self.dlg.checkBox_envelope.isChecked():
            self.layerEnvelope = self.mapLayerRegistry.mapLayersByName(self.dlg.comboBox_envelope.currentText())[0]
            self.layerEnvelope = PointInLayer.PointInLayer(self.layerEnvelope)

        if self.dlg.checkBox_useMinNumberEntities.isChecked():
            self.layerMinEntities = self.mapLayerRegistry.mapLayersByName(self.dlg.comboBox_layerMinEntities.currentText())[0]
            self.nbFeaturesLayerMinEntities = self.layerMinEntities.featureCount()
            self.layerMinEntities = PointInLayer.PointInLayer(self.layerMinEntities)
            self.nbMinEntities = self.dlg.spinBox__minEntities.value()
            self.step = self.dlg.spinBox_step.value()
        
        if self.fileName == "" and display == False:
            self.iface.messageBar().pushMessage(QApplication.translate("Blurring", 'No file provided, "add resultat to canvas" required'), level=QgsMessageBar.CRITICAL , duration=5)
            return
        
        if display :
            self.settings = QSettings()
            self.oldDefaultProjection = self.settings.value("/Projections/defaultBehaviour")
            self.settings.setValue( "/Projections/defaultBehaviour", "useProject")
        
        self.polygonBufferFinalLayer = None
        self.fileWriter = None
        
        """Recuperation de la couche"""
        layer = self.mapLayerRegistry.mapLayersByName(layerName)[0]
        fields = layer.pendingFields()
        crsMapRenderer = self.iface.mapCanvas().mapRenderer().destinationCrs()
        crsLayer = layer.crs()
        
        #if crsMapRenderer.mapUnits() != 0 or crsLayer.mapUnits() != 0:
        #    self.iface.messageBar().pushMessage(QApplication.translate("Blurring",'The projection of the map or of the layer is not in meters. These parameters should be in meters.'), level=QgsMessageBar.CRITICAL , duration=5)
        #    return

        """Creation de la couche polygonale"""

        if self.fileName != "":
            self.fileWriter = QgsVectorFileWriter(self.fileName, None, fields, QGis.WKBPolygon, crsLayer, "ESRI Shapefile")
            if self.fileWriter.hasError() != QgsVectorFileWriter.NoError:
                self.iface.messageBar().pushMessage(QApplication.translate("Blurring","Error when creating shapefile: ", self.fileWriter.hasError()), level=QgsMessageBar.CRITICAL , duration=5)

        else :
            layerName = QApplication.translate("Blurring","Final buffer ")
            self.polygonBufferFinalLayer = QgsVectorLayer("Polygon",layerName + str(self.radius) + " m", "memory")
            self.polygonBufferFinalLayer.setCrs(crsLayer)
            self.dataProviderPolygonBufFinalLayer = self.polygonBufferFinalLayer.dataProvider()
            self.dataProviderPolygonBufFinalLayer.addAttributes(list(fields))
            self.polygonBufferFinalLayer.startEditing()
        
        """Uniquement entités selectionnées ?"""
        features = None
        self.nbFeatures = None
        if selectedFeaturesOnly:
            features = layer.selectedFeatures()
            self.nbFeatures = layer.selectedFeatureCount()
        else:
            features = layer.getFeatures()
            self.nbFeatures = layer.featureCount()
        
        if self.layerEnvelope != None:
            for feature in features:
                if not self.layerEnvelope.contains(feature.geometry()):
                    self.iface.messageBar().pushMessage(QApplication.translate("Blurring", 'Point with id '+ str(feature.id()) + ' is outside of the envelope'), level=QgsMessageBar.CRITICAL , duration=5)
                    self.dlg.progressBar_progression.setValue(0)
                    return
        
        if self.layerMinEntities != None:
            if self.nbMinEntities > self.nbFeaturesLayerMinEntities:
                self.iface.messageBar().pushMessage(QApplication.translate("Blurring", 'Not enough feature'), level=QgsMessageBar.CRITICAL , duration=5)
                return
        
        
        algoOk = False
        self.lastFeature = 0
        print "Debut iteration"
        while not algoOk:
            if selectedFeaturesOnly:
                features = layer.selectedFeatures()
                self.nbFeatures = layer.selectedFeatureCount()
            else:
                features = layer.getFeatures()
                self.nbFeatures = layer.featureCount()
                
            if self.fileName != "":
                self.fileWriter = QgsVectorFileWriter(self.fileName, None, fields, QGis.WKBPolygon, crsLayer, "ESRI Shapefile")
                if self.fileWriter.hasError() != QgsVectorFileWriter.NoError:
                    self.iface.messageBar().pushMessage(QApplication.translate("Blurring","Error when creating shapefile: ", self.fileWriter.hasError()), level=QgsMessageBar.CRITICAL , duration=5)
    
            else :
                layerName = QApplication.translate("Blurring","Final buffer ")
                self.polygonBufferFinalLayer = QgsVectorLayer("Polygon",layerName + str(self.radius) + " m", "memory")
                self.polygonBufferFinalLayer.setCrs(crsLayer)
                self.dataProviderPolygonBufFinalLayer = self.polygonBufferFinalLayer.dataProvider()
                self.dataProviderPolygonBufFinalLayer.addAttributes(list(fields))
                self.polygonBufferFinalLayer.startEditing()
                
            algoOk = self.algo(self.radius, features)

        
        """Validation des changements et ajout de la couche à la carte""" 
        if self.fileName == "":
            self.polygonBufferFinalLayer.commitChanges()
        else :
            del self.fileWriter
        
        if self.layerMinEntities != None:
                    QMessageBox.information(self.iface.mainWindow(),"Result","Min radius : " + str(self.dlg.spinBox_radius.value()) + 
                                            "<br /> Min feature : " + str(self.nbMinEntities) +
                                            "<br /> Step : " + str(self.step) + 
                                            "<br /> ----------" +
                                            "<br /> Final radius : " + str(self.radius) +
                                            "<br /> With " + str(self.radius - self.step) + " : " + str(self.lastFeature + 1) + "/" + str(self.nbFeatures))
        
        if display:            
            if self.fileName != "":
                layerName = ntpath.basename(self.fileName)
                self.newlayer = QgsVectorLayer(self.fileName, layerName,"ogr")
                self.newlayer.commitChanges()
                self.newlayer.clearCacheImage()
                QgsMapLayerRegistry.instance().addMapLayers([self.newlayer])
            else:
                QgsMapLayerRegistry.instance().addMapLayer(self.polygonBufferFinalLayer)
                
            self.settings.setValue( "/Projections/defaultBehaviour", self.oldDefaultProjection) 
                   
        self.dlg.hide()
        
        if self.fileName != "":
            self.iface.messageBar().pushMessage(QApplication.translate("Blurring", "Successful export in " + self.fileName), level=QgsMessageBar.INFO , duration=5)
        else:
            self.iface.messageBar().pushMessage(QApplication.translate("Blurring", "Succesfully done in memory ! Be careful, it's not saved ! "), level=QgsMessageBar.INFO , duration=5)




    def algo(self,radius,features):
        """Iteration sur la couche ponctuelle"""
        for j,feature in enumerate(features):
            """Recuperation de la geom et des attributs"""
            geom = feature.geometry()
            attrs = feature.attributes()
            
            """Tirage du point aleatoire"""
            pointAleaGeom = None

            if self.layerEnvelope != None:
                i = 0
                while True:
                    pointAleaGeom = self.randomPointAroundGeomPoint(geom, radius)
                    if self.layerEnvelope.contains(pointAleaGeom):
                        break
                    else:
                        i +=1
                        if i >100:
                            print "max 100"
                            pointAleaGeom = self.randomPointAroundGeomPoint(geom, 5)
                            break
            else:
                pointAleaGeom = self.randomPointAroundGeomPoint(geom, radius)
            
            """Creation du buffer final"""
            bufferGeom2 = pointAleaGeom.buffer(radius,0.5)
            bufferFeature2 = QgsFeature()
            bufferFeature2.setGeometry(bufferGeom2)
            bufferFeature2.setAttributes(attrs)
            if self.layerMinEntities != None:
                if j >= self.lastFeature:
                    print "count feature " + str(j)
                    if not self.layerMinEntities.countIntersection(bufferFeature2.geometry(), self.nbMinEntities):
                        self.radius = radius + self.step
                        print self.radius
                        self.lastFeature = j
                        print "Nb ID : " + str(self.lastFeature)
                        return False
            
            """Ajout a la couche du buffer2"""
            if self.fileName != "":
                self.fileWriter.addFeature(bufferFeature2)
            else :
                self.polygonBufferFinalLayer.dataProvider().addFeatures([bufferFeature2])
            
            """Maj de la bar de progression"""
            percent =int((j+1)*100/self.nbFeatures)
            self.dlg.progressBar_progression.setValue(percent)
        
        return True




    def randomPointAroundGeomPoint(self,point, radius):
        teta = math.pi*random.uniform(0, 2)
        deltaX = random.randint(0,radius)
        deltaY = random.randint(0,radius)
        randomX = point.asPoint().x()+ deltaX * math.cos(teta)
        randomY = point.asPoint().y()+ deltaY * math.sin(teta)
        return QgsGeometry.fromPoint(QgsPoint(randomX, randomY))

    def displayHelp(self):
        infoString = QCoreApplication.translate('Blurring', u"Plugin to blur point data, such as health personal data<br /><table><tr><td><img src=':/resources/step1' /></td><td>Creating a buffer (radius r)</td></tr><tr><td><img src=':/resources/step2' /></td><td>Random selection of a point in each buffer</td></tr><tr><td><img src=':/resources/step3' /></td><td>Creating a buffer around the new point with the same radius. The initial point is at a maximal distance 2r of the centroid of the buffer.</td></tr></table>")
        QMessageBox.information(self.dlg,u"Blurring", infoString)
                
    def cancel(self):
        self.dlg.hide()
        
    def layerDeleted(self,idLayer):
        self.displayComboBoxLayers()
        
    def layerAdded(self,idLayer):
        self.displayComboBoxLayers()