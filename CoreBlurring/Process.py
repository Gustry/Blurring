# -*- coding: utf-8 -*-
'''
Created on 5 août 2014

@author: etienne
'''

from Blurring import *
from processing.tools.system import *

import LayerIndex
import BlurAlgo

class Process:

    @staticmethod
    def blurProcess(dialog=None, layerToBlur=None, radius=None, display=None, selectedFeaturesOnly=None, fileName=None, layerEnvelope=None, exportRadius=None, exportCentroid=None):
        print "process"
        
        if not fileName:
            fileName = getTempFilenameInTempFolder("blurring.shp")
        
        if layerEnvelope:
            layerEnvelope = LayerIndex.LayerIndex(layerEnvelope)
        
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
            #self.dlg.progressBar_progression.setValue(percent)
        
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
        