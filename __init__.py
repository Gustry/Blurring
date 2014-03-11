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
 This script initializes the plugin, making it known to QGIS.
"""

def classFactory(iface):
    # load Blurring class from file Blurring
    from blurring import Blurring
    return Blurring(iface)
