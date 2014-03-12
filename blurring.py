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
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from blurringdialog import BlurringDialog
import os.path
import random
import math


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
        self.iface.addPluginToMenu(u"&Blurring", self.action)
        
        #Variables
        self.mapLayerRegistry = QgsMapLayerRegistry.instance()
        
        #Connecteurs
        QObject.connect(self.dlg.pushButton_calculation, SIGNAL("clicked()"), self.calculation)
        QObject.connect(QgsMapLayerRegistry.instance(), SIGNAL("layerRemoved(QString)"), self.layerDeleted)
        QObject.connect(QgsMapLayerRegistry.instance(), SIGNAL("layerWasAdded(QgsMapLayer)"), self.layerAdded)
        QObject.connect(QgsMapLayerRegistry.instance(), SIGNAL("layersAdded(QgsMapLayer)"), self.layerAdded)
        #QObject.connect(QgsMapLayerRegistry.instance(), SIGNAL("legendLayersAdded(QList)"), self.layerAdded)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&Blurring", self.action)
        self.iface.removeToolBarIcon(self.action)

    # run method that performs all the real work
    def run(self):
        self.layers = self.iface.legendInterface().layers()
        self.dlg.comboBox_blurredLayer.clear()
        #Remplissage du menu déroulant
        for layer in self.layers:
            if layer.LayerType() == 0 and layer.geometryType() == 0 :
                self.dlg.comboBox_blurredLayer.addItem(layer.name())
                 
        if self.dlg.comboBox_blurredLayer.count() < 1:
            self.dlg.pushButton_calculation.setEnabled(False)
        else:
            self.dlg.pushButton_calculation.setEnabled(True)
        
        self.dlg.show()

    def calculation(self):
        """Bar de progression a 0"""
        self.dlg.progressBar_progression.setValue(0)
        
        """Recuperation des champs du formulaire"""
        layerName = self.dlg.comboBox_blurredLayer.currentText()
        radius = self.dlg.spinBox_radius.value()
        debugPointAlea = self.dlg.checkBox_pointAlea.isChecked()
        debugPremierBuffer = self.dlg.checkBox_premierBuffer.isChecked()
        
        """Recuperation de la couche"""
        layer = self.mapLayerRegistry.mapLayersByName(layerName)[0]

        """Creation de la couche polygonale"""
        self.polygonBufferFinalLayer = QgsVectorLayer("Polygon",self.dlg.tr(u"Buffer final " + str(radius)), "memory")
        self.dataProviderPolygonBufFinalLayer = self.polygonBufferFinalLayer.dataProvider()
        self.polygonBufferFinalLayer.startEditing()
        
        """Transfert de la table attributaire"""
        fields = layer.pendingFields()
        self.dataProviderPolygonBufFinalLayer.addAttributes(list(fields))
        
        """Creation de la couche buffer 1"""
        if debugPremierBuffer :
            self.polygonLayer = QgsVectorLayer("Polygon",self.dlg.tr(u"Buffer 1"), "memory")
            self.dataProviderPolygonLayer = self.polygonLayer.dataProvider()
        
        """Creation de la couche point alea"""
        if debugPointAlea :
            self.pointAleaLayer = QgsVectorLayer("Point",self.dlg.tr(u"Point Alea"), "memory")
            self.dataProviderPointAleaLayer = self.pointAleaLayer.dataProvider()
        
        """Iteration sur la couche ponctuelle"""
        for i,feature in enumerate(layer.getFeatures()):
            
            """Recuperation de la geom et des attributs"""
            geom = feature.geometry()
            attrs = feature.attributes()
            
            """Creation du premier buffer"""
            if debugPremierBuffer :
                bufferFeature1 = QgsFeature()
                bufferFeature1.setGeometry(geom.buffer(radius,30))
                self.polygonLayer.dataProvider().addFeatures([bufferFeature1])
            
            """Tirage du point aleatoire"""
            teta = math.pi*random.uniform(0, 2)
            deltaX, deltaY = random.randint(0,radius), random.randint(0,radius)
            randomX = geom.asPoint().x()+ deltaX * math.cos(teta)
            randomY = geom.asPoint().y()+ deltaY * math.sin(teta)
            
            """Creation du point aleatoire"""
            pointAleaGeom = QgsGeometry.fromPoint(QgsPoint(randomX, randomY))
            if debugPointAlea :
                pointAleaFeature = QgsFeature()
                pointAleaFeature.setGeometry(pointAleaGeom)
                self.pointAleaLayer.dataProvider().addFeatures([pointAleaFeature])
            
            """Creation du buffer final"""
            bufferGeom2 = pointAleaGeom.buffer(radius,30)
            bufferFeature2 = QgsFeature()
            bufferFeature2.setGeometry(bufferGeom2)
            bufferFeature2.setAttributes(attrs)
            
            """Ajout a la couche du buffer2"""
            self.polygonBufferFinalLayer.dataProvider().addFeatures([bufferFeature2])
            
            """Maj de la bar de progression"""
            percent =int((i+1)*100/layer.featureCount())
            self.dlg.progressBar_progression.setValue(percent)
        
        """Validation des changements et ajout de la couche à la carte""" 
        self.polygonBufferFinalLayer.commitChanges()
        QgsMapLayerRegistry.instance().addMapLayer(self.polygonBufferFinalLayer)
        
        if debugPointAlea :
            self.pointAleaLayer.commitChanges()
            QgsMapLayerRegistry.instance().addMapLayer(self.pointAleaLayer)
            
        if debugPremierBuffer :
            self.polygonLayer.commitChanges()
            QgsMapLayerRegistry.instance().addMapLayer(self.polygonLayer)

        
    def layerDeleted(self,idLayer):
        print idLayer
        
    def layerAdded(self,idLayer):
        print idLayer