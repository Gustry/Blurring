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
from stats import Ui_Form
import os

class StatsWidget(QWidget, Ui_Form):
    
    #Signal new query
    signalProcessBlur = pyqtSignal(name='signalProcessBlur')
    
    def __init__(self, parent=None):
        super(StatsWidget, self).__init__()
        self.setupUi(self)
        
    def hide(self):
        iface.Blurring_mainWindowDialog.hide()

        
class StatsDockWidget(QDockWidget):
    def __init__(self, parent=None):
        QDockWidget.__init__(self)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.setWidget(StatsWidget())
        self.setWindowTitle(Tools.trans("Blurring - Stats"))