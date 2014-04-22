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

from processing.core.AlgorithmProvider import AlgorithmProvider
from processing.core.ProcessingConfig import Setting, ProcessingConfig
from BlurringGeoAlgorithm import BlurringGeoAlgorithm
from PyQt4.QtGui import QIcon

import resources

class BlurringGeoAlgorithmProvider(AlgorithmProvider):

    MY_DUMMY_SETTING = 'MY_DUMMY_SETTING'

    def __init__(self):
        AlgorithmProvider.__init__(self)

        # Deactivate provider by default
        self.activate = False

        # Load algorithms
        self.alglist = [BlurringGeoAlgorithm()]
        for alg in self.alglist:
            alg.provider = self

    def initializeSettings(self):
        AlgorithmProvider.initializeSettings(self)
        ProcessingConfig.addSetting(Setting('Blurring', BlurringGeoAlgorithmProvider.MY_DUMMY_SETTING,'Example setting', 'Default value'))

    def unload(self):
        AlgorithmProvider.unload(self)
        ProcessingConfig.removeSetting(BlurringGeoAlgorithmProvider.MY_DUMMY_SETTING)

    def getName(self):
        return 'Blurring'

    def getDescription(self):
        return 'Blurring plugin'

    def getIcon(self):
        return QIcon(":/resources/icon")

    def _loadAlgorithms(self):
        self.algs = self.alglist
