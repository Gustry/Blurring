# -*- coding: utf-8 -*-
"""
/***************************************************************************
Blurring
A QGIS plugin
Blurring data
-------------------
begin : 2014-03-11
copyright : (C) 2014 by TER Géomatique UM2
email : ter-floutage@googlegroups.com
***************************************************************************/
/***************************************************************************
* *
* This program is free software; you can redistribute it and/or modify *
* it under the terms of the GNU General Public License as published by *
* the Free Software Foundation; either version 2 of the License, or *
* (at your option) any later version. *
* *
***************************************************************************/
"""
from Blurring import *
from Blurring.ProcessingBlurring.BlurringGeoAlgorithm import BlurringGeoAlgorithm
from processing.core.AlgorithmProvider import AlgorithmProvider

"""QGIS Processing"""
class BlurringAlgorithmProvider(AlgorithmProvider):
    def __init__(self):
        AlgorithmProvider.__init__(self)
    
        self.activate = True
    
        # Load algorithms
        self.alglist = [BlurringGeoAlgorithm()]
        for alg in self.alglist:
            alg.provider = self
    
    def initializeSettings(self):
        AlgorithmProvider.initializeSettings(self)
    
    def unload(self):
        AlgorithmProvider.unload(self)
    
    def getName(self):
        return 'Blurring'
    
    def getDescription(self):
        return 'Blurring plugin'
    
    def getIcon(self):
        return QIcon(":/plugins/Blurring/icon.png")
    
    def _loadAlgorithms(self):
        self.algs = self.alglist