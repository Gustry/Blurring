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
import resources

from processing.core.Processing import Processing
from processing.core.GeoAlgorithm import GeoAlgorithm
from processing.parameters.ParameterVector import ParameterVector
from processing.parameters.ParameterNumber import ParameterNumber
from processing.parameters.ParameterBoolean import ParameterBoolean
from processing.outputs.OutputVector import OutputVector
from processing.tools import dataobjects, vector
from BlurringAlgorithmCore import BlurringAlgorithmCore
import LayerIndex

class BlurringGeoAlgorithm(GeoAlgorithm):

    OUTPUT_LAYER = 'OUTPUT_LAYER'
    INPUT_LAYER = 'INPUT_LAYER'
    RADIUS_FIELD = 'RADIUS_FIELD'
    RADIUS_EXPORT = 'RADIUS_EXPORT'
    CENTROID_EXPORT = 'CENTROID_EXPORT'
    DISTANCE_EXPORT = 'DISTANCE_EXPORT'
    ENVELOPE_LAYER = 'ENVELOPE_LAYER'

    def defineCharacteristics(self):
        self.name = 'Simplest algo (point layer and radius only)'
        self.group = 'Blurring a point layer'

        self.addParameter(ParameterVector(self.INPUT_LAYER, 'Point layer',[ParameterVector.VECTOR_TYPE_POINT], False))
        self.addParameter(ParameterNumber(self.RADIUS_FIELD, 'Radius (maps unit)',1,999999999,1000))
        self.addParameter(ParameterVector(self.ENVELOPE_LAYER, 'Envelope layer',[ParameterVector.VECTOR_TYPE_POLYGON], True))
        self.addParameter(ParameterBoolean(self.RADIUS_EXPORT, 'Add the radius to the attribute table',False))
        self.addParameter(ParameterBoolean(self.CENTROID_EXPORT, 'Add the centroid to the attribute table',False))
        self.addParameter(ParameterBoolean(self.DISTANCE_EXPORT, 'Add the distance between the inital point and the centroid',False))

        self.addOutput(OutputVector(self.OUTPUT_LAYER,'Output layer with selected features'))

    def help(self):
        return True, "Plugin to blur point data, such as health personal data<br /><table><tr><td><img src=':/resources/step1' /></td><td>Creating a buffer (radius r)</td></tr><tr><td><img src=':/resources/step2' /></td><td>Random selection of a point in each buffer</td></tr><tr><td><img src=':/resources/step3' /></td><td>Creating a buffer around the new point with the same radius. The initial point is at a maximal distance 2r of the centroid of the buffer.</td></tr></table>"

    def processAlgorithm(self, progress):

        inputFilename = self.getParameterValue(self.INPUT_LAYER)
        radius = self.getParameterValue(self.RADIUS_FIELD)
        exportRadius = self.getParameterValue(self.RADIUS_EXPORT)
        exportCentroid = self.getParameterValue(self.CENTROID_EXPORT)
        exportDistance = self.getParameterValue(self.DISTANCE_EXPORT)
        envelopeLayerField = self.getParameterValue(self.ENVELOPE_LAYER)
        output = self.getOutputValue(self.OUTPUT_LAYER)

        vectorLayer = dataobjects.getObjectFromUri(inputFilename)
        
        vectorlayerEnvelopeIndex = None
        if envelopeLayerField != None:
            vectorLayerEnvelope = dataobjects.getObjectFromUri(envelopeLayerField)
            vectorlayerEnvelopeIndex = LayerIndex.LayerIndex(vectorLayerEnvelope)

        settings = QSettings()
        systemEncoding = settings.value('/UI/encoding', 'System')
        provider = vectorLayer.dataProvider()
        fields = provider.fields()
        
        if exportRadius:
            fields.append(QgsField(u"Radius", QVariant.Int))
        
        if exportCentroid:
            fields.append(QgsField(u"X centroid", QVariant.Int))
            fields.append(QgsField(u"Y centroid", QVariant.Int))
        
        if exportDistance:
            fields.append(QgsField(u"Distance", QVariant.Double))
        
        writer = QgsVectorFileWriter(output, systemEncoding,
                                     fields,
                                     QGis.WKBPolygon, provider.crs())
        
        algo = BlurringAlgorithmCore.BlurringAlgorithmCore(radius, vectorlayerEnvelopeIndex, exportRadius, exportCentroid, exportDistance)

        features = vector.features(vectorLayer)
        for feature in features:
            feature = algo.blur(feature)
            writer.addFeature(feature)