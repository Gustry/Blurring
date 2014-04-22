'''
Created on 20 avr. 2014

@author: etienne
'''

from qgis.core import QgsGeometry,QgsVectorLayer

class PointInLayer:
    
    def __init__(self, layer):
        self.__layer = layer
        
    def contains(self, point):
        contains = False
        
        for feature in self.__layer.getFeatures():
            if point.intersects(feature.geometry()):
                contains = True
                break
        
        return contains
    
    def entityContains(self, point):
        for feature in self.__layer.getFeatures():
            if point.intersects(feature.geometry()):
                return feature.geometry()
        return False