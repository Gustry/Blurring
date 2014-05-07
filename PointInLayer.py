'''
Created on 20 avr. 2014

@author: etienne
'''

from qgis.core import QgsGeometry,QgsVectorLayer,QgsFeatureRequest
from processing.tools import vector

class PointInLayer:
    
    def __init__(self, layer):
        self.__layer = layer
        self.__index = vector.spatialindex(layer)
        
    def contains(self, point):        
        """for feature in self.__layer.getFeatures():
            if point.intersects(feature.geometry()):
                contains = True
                break
        """
        intersects = self.__index.intersects(point.boundingBox())
        for i in intersects:
            request = QgsFeatureRequest().setFilterFid(i)
            feat = self.__layer.getFeatures(request).next()
            tmpGeom = QgsGeometry(feat.geometry())
            if point.intersects(tmpGeom):
                return True
        return False
    
    def countIntersection(self,bufferGeom,nb):
        count = 0
        intersects = self.__index.intersects(bufferGeom.boundingBox())
        for i in intersects:
            request = QgsFeatureRequest().setFilterFid(i)
            feat = self.__layer.getFeatures(request).next()
            tmpGeom = QgsGeometry(feat.geometry())
            if bufferGeom.intersects(tmpGeom):
                count += 1
                if count >= nb:
                    return True
        return False