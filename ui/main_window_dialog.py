# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Blurring
                                 A QGIS plugin
 Blur a point layer
                             -------------------
        begin                : 2014-08-05
        copyright            : (C) 2014 by IRD
        email                : etienne@trimaille.eu
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""

from Blurring import *
from main_window import Ui_BlurringDialogBase

class MainWindowDialog(QDialog, Ui_BlurringDialogBase):
       
    def __init__(self, parent=None):
        '''
        Constructor
        '''
        QDialog.__init__(self)
        self.setupUi(self)