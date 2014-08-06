# -*- coding: utf-8 -*-
"""
/***************************************************************************
 BlurringDialog
                                 A QGIS plugin
 Blur a point layer
                             -------------------
        begin                : 2014-08-05
        git sha              : $Format:%H$
        copyright            : (C) 2014 by IRD
        email                : etienne@trimaille.eu
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
from ui.main_window_dialog import MainWindowDialog
import os.path

class Blurring:

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'Blurring_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        #Add to processing
        #self.provider = BlurringAlgorithmProvider()
        #Processing.addProvider(self.provider, True)

    def initGui(self):

        #Main window        
        self.mainWindowAction = QAction(
            QIcon(":/plugins/Blurring/icon.png"),
            u"Blurring",
            self.iface.mainWindow())
        self.mainWindowAction.triggered.connect(self.openMainWindow)
        self.iface.addToolBarIcon(self.mainWindowAction)
        self.iface.addPluginToWebMenu(u"&Quick OSM",self.mainWindowAction)
        self.iface.Blurring_mainWindowDialog = MainWindowDialog()
        
    def unload(self):
        self.iface.removePluginWebMenu(u"&Quick OSM",self.mainWindowAction)
        self.iface.removeToolBarIcon(self.mainWindowAction)
        #Processing.removeProvider(self.provider)
    
    def openMainWindow(self):
        self.iface.Blurring_mainWindowDialog.listWidget.setCurrentRow(0)
        self.iface.Blurring_mainWindowDialog.exec_()