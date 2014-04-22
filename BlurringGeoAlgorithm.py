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

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

from processing.core.Processing import Processing
from processing.core.GeoAlgorithm import GeoAlgorithm
from processing.parameters.ParameterVector import ParameterVector
from processing.parameters.ParameterNumber import ParameterNumber
from processing.outputs.OutputVector import OutputVector
from processing.tools import dataobjects, vector

import random
import math

class BlurringGeoAlgorithm(GeoAlgorithm):

    OUTPUT_LAYER = 'OUTPUT_LAYER'
    INPUT_LAYER = 'INPUT_LAYER'
    VALUE_FIELD = 'VALUE_FIELD'

    def defineCharacteristics(self):
        self.name = 'Simplest algo (point layer and radius only)'
        self.group = 'Blurring a point layer'

        self.addParameter(ParameterVector(self.INPUT_LAYER, 'Point layer',[ParameterVector.VECTOR_TYPE_POINT], False))
        self.addParameter(ParameterNumber(self.VALUE_FIELD, 'Radius (maps unit)',1,999999999,1000))

        self.addOutput(OutputVector(self.OUTPUT_LAYER,'Output layer with selected features'))

    def processAlgorithm(self, progress):

        inputFilename = self.getParameterValue(self.INPUT_LAYER)
        radius = self.getParameterValue(self.VALUE_FIELD)
        output = self.getOutputValue(self.OUTPUT_LAYER)

        vectorLayer = dataobjects.getObjectFromUri(inputFilename)

        settings = QSettings()
        systemEncoding = settings.value('/UI/encoding', 'System')
        provider = vectorLayer.dataProvider()
        writer = QgsVectorFileWriter(output, systemEncoding,
                                     provider.fields(),
                                     QGis.WKBPolygon, provider.crs())

        features = vector.features(vectorLayer)
        for feature in features:
            
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
            bufferGeom2 = pointAleaGeom.buffer(radius,20)
            bufferFeature2 = QgsFeature()
            bufferFeature2.setGeometry(bufferGeom2)
            bufferFeature2.setAttributes(attrs)
            
            writer.addFeature(bufferFeature2)