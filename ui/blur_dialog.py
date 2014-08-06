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
from processing.tools.system import *
from Blurring.CoreBlurring import LayerIndex
from Blurring.CoreBlurring import BlurAlgo
import os

class BlurWidget(QWidget, Ui_Form):
    
    #Signal new query
    signalProcessBlur = pyqtSignal(name='signalProcessBlur')
    
    def __init__(self, parent=None):
        super(BlurWidget, self).__init__()
        self.setupUi(self)
        
        self.label_progress.setText('')
        self.checkBox_envelope.setChecked(False)
        self.comboBox_envelope.setEnabled(False)
        
        self.pushButton_browseFolder.clicked.connect(self.selectFile)
        self.pushButton_refreshLayersToBlur.clicked.connect(self.fillComboxboxLayers)
        self.buttonBox_blur.button(QDialogButtonBox.Ok).clicked.connect(self.runBlur)
        self.buttonBox_blur.button(QDialogButtonBox.Cancel).clicked.connect(self.hide)
        
    def hide(self):
        iface.Blurring_mainWindowDialog.hide()

    def selectFile(self):
        lastDir = Tools.getLastInputPath()
        outputFile = QFileDialog.getSaveFileName(parent=self,
                                                 caption=Tools.trans('Select file'),
                                                 directory=lastDir,
                                                 filter="Shapefiles (*.shp)")
        if outputFile:
            self.lineEdit_outputFile.setText(outputFile)
            path = os.path.basename(outputFile)
            Tools.setLastInputPath(path)
        else:
            self.lineEdit_outputFile.setText('')

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
        self.label_progress.setText("")
        
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
            
            
            if not fileName:
                fileName = getTempFilenameInTempFolder("blurring.shp")
        
            if layerEnvelope:
                self.label_progress.setText("Creating index ...")
                layerEnvelope = LayerIndex.LayerIndex(layerEnvelope)
                self.progressBar_blur.setValue(0)
            
            
            self.label_progress.setText("Blurring ...")
            settings = None
            oldDefaultProjection = None
            if display :
                settings = QSettings()
                oldDefaultProjection = settings.value("/Projections/defaultBehaviour")
                settings.setValue( "/Projections/defaultBehaviour", "useProject")
            
            features = None
            nbFeatures = None
            if selectedFeaturesOnly:
                features = layerToBlur.selectedFeatures()
                nbFeatures = layerToBlur.selectedFeatureCount()
            else:
                features = layerToBlur.getFeatures()
                nbFeatures = layerToBlur.featureCount()
            
            #Fields
            fields = layerToBlur.pendingFields()
            if exportRadius:
                fields.append(QgsField(u"Radius", QVariant.Int))
            if exportCentroid:
                fields.append(QgsField(u"X centroid", QVariant.Int))
                fields.append(QgsField(u"Y centroid", QVariant.Int))
            
            #Creating the output shapefile
            fileWriter = QgsVectorFileWriter(fileName, "utf-8", fields, QGis.WKBPolygon, layerToBlur.crs(), "ESRI Shapefile")
            if fileWriter.hasError() != QgsVectorFileWriter.NoError:
                raise CreatingShapeFileException(suffix=fileWriter.hasError())
            
            #Creating the algorithm with radius
            algo = BlurAlgo.BlurAlgo(radius, layerEnvelope, exportRadius, exportCentroid)
            
            for j,feature in enumerate(features):
                feature = algo.blur(feature)
                fileWriter.addFeature(feature)
            
                """Update progress bar"""
                percent =int((j+1)*100/nbFeatures)
                self.progressBar_blur.setValue(percent)
            
            #Write all features in the file
            del fileWriter
            
            if display:
                import ntpath
                layerName = ntpath.basename(fileName)
                newlayer = QgsVectorLayer(fileName, layerName,"ogr")
                newlayer.commitChanges()
                newlayer.clearCacheImage()
                QgsMapLayerRegistry.instance().addMapLayers([newlayer])
                
                settings.setValue( "/Projections/defaultBehaviour", oldDefaultProjection) 
            
            iface.messageBar().pushMessage(Tools.trans("Successful export in " + fileName), level=QgsMessageBar.INFO , duration=5)
            
            self.hide()
        
        except BlurringException,e:
            self.label_progress.setText("")
            Tools.displayMessageBar(msg=e.msg, level=e.level , duration=e.duration)
        
        finally:
            QApplication.restoreOverrideCursor()
            QApplication.processEvents()

    def setProgressPercentage(self,percent):
        '''
        Slot to update percentage during process
        '''
        self.progressBar_blur.setValue(percent)
        QApplication.processEvents()
        
    def setProgressText(self,text):
        '''
        Slot to update text during process
        '''
        self.label_progress.setText(text)
        QApplication.processEvents()
        
class BlurDockWidget(QDockWidget):
    def __init__(self, parent=None):
        QDockWidget.__init__(self)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.setWidget(BlurWidget())
        self.setWindowTitle(Tools.trans("Blurring - Blur"))