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

from qgis.core import QgsGeometry,QgsFeatureRequest, QgsSpatialIndex
from processing.tools import vector

class LayerIndex:
    
    def __init__(self, layer):
        self.__layer = layer        
        self.__index = QgsSpatialIndex()
        feats = vector.features(layer)
        for ft in feats:
            self.__index.insertFeature(ft)
        
    def contains(self, point):
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