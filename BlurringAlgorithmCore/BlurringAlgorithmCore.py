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

from qgis.core import QgsGeometry,QgsPoint, QgsFeature
from PyQt4.QtGui import QApplication
from processing.core.GeoAlgorithmExecutionException import GeoAlgorithmExecutionException
import random, math
from math import sqrt

class BlurringAlgorithmCore:
    
    def __init__(self,radius, polygonEnvelope,addRadiusToAttributes, addCentroidToAttributes, addDistanceToAttributes):
        self.__radius = radius
        self.__polygonEnvelope = polygonEnvelope
        self.__addRadiusToAttributes = addRadiusToAttributes
        self.__addCentroidToAttributes = addCentroidToAttributes
        self.__addDistanceToAttributes = addDistanceToAttributes
 
    
    def blur(self, feature):
        geom = feature.geometry()
        attrs = feature.attributes()
        pointAleaGeom = None
        
        """Creation du point aleatoire"""
        if self.__polygonEnvelope != None:
            
            if not self.__polygonEnvelope.contains(geom):
                msg = QApplication.translate("Blurring", 'Point number ')+ str(feature.id()) + QApplication.translate("Blurring", 'is outside the envelope')
                raise GeoAlgorithmExecutionException, msg
            
            radius = self.__radius
            i = 0
            while True:
                pointAleaGeom = self.__randomPointAroundGeomPoint(geom, radius)
                if self.__polygonEnvelope.contains(pointAleaGeom):
                    break
                else:
                    i +=1
                    if i == 100:
                        radius = int(radius * 0.5)
                    elif i == 150:
                        radius = int(radius * 0.5)
                    elif i == 200:
                        radius = int(radius * 0.5)
                    elif i >= 250:
                        radius = 0
                        break
        else:
            pointAleaGeom = self.__randomPointAroundGeomPoint(geom, self.__radius)
        
        """Creation du buffer final"""
        bufferGeom = pointAleaGeom.buffer(self.__radius,20)
        bufferFeature = QgsFeature()
        bufferFeature.setGeometry(bufferGeom)
        
        if self.__addRadiusToAttributes:
            attrs.append(self.__radius)
        if self.__addCentroidToAttributes:
            attrs.append(int(bufferGeom.centroid().asPoint().x()))
            attrs.append(int(bufferGeom.centroid().asPoint().y()))
        if self.__addDistanceToAttributes:
            deltaX = bufferGeom.centroid().asPoint().x()-geom.asPoint().x()
            deltaY = bufferGeom.centroid().asPoint().y()-geom.asPoint().y()
            attrs.append(sqrt((deltaX*deltaX) + (deltaY*deltaY)))

        bufferFeature.setAttributes(attrs)
        return bufferFeature
    
    
    def __randomPointAroundGeomPoint(self,point,radius):
        """Tirage du point aleatoire"""
        teta = math.pi*random.uniform(0, 2)
        r = random.randint(0,radius)
        randomX = point.asPoint().x()+ (r * math.cos(teta))
        randomY = point.asPoint().y()+ (r * math.sin(teta))
        return QgsGeometry.fromPoint(QgsPoint(randomX, randomY))
    
    def __trunc(self,f, n):
        '''Truncates/pads a float f to n decimal places without rounding'''
        slen = len('%.*f' % (n, f))
        return str(f)[:slen]