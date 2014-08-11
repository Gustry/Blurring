# -*- coding: utf-8 -*-
'''
Created on 5 août 2014

@author: etienne
'''

from Blurring import *

class Tools:

    @staticmethod
    def getLastInputPath():
        settings = QSettings()
        return settings.value("LastInputPath")
    
    @staticmethod
    def setLastInputPath(lastDir):
        path = lastDir
        #path = QFileInfo(lastDir).absolutePath()
        settings = QSettings()
        settings.setValue( "LastInputPath", str(path))
       
    @staticmethod
    def trans(msg):
        return QApplication.translate("Blurring",msg)
    
    @staticmethod
    def displayMessageBar(title = None, msg = None,level=QgsMessageBar.INFO,duration=5):
        if iface.Blurring_mainWindowDialog.isVisible():
            iface.Blurring_mainWindowDialog.messageBar.pushMessage(title, msg, level,duration)
        else:
            iface.messageBar().pushMessage(title, msg, level,duration)
        