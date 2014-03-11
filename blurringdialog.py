# -*- coding: utf-8 -*-
"""
/***************************************************************************
 BlurringDialog
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

from PyQt4 import QtCore, QtGui
from ui_blurring import Ui_Blurring


class BlurringDialog(QtGui.QDialog, Ui_Blurring):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
