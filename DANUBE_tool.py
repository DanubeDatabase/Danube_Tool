# -*- coding: utf-8 -*-

"""
/***************************************************************************
 DANUBEtool
                                 A QGIS plugin
 DANUBE Tool plugin allows you to generate spatialized buildings' material informations from DANUBE database and urban scale typomorphological informations (IGN BDTOPO data and Geoclimate tool's outputs)  
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2023-03-31
        copyright            : (C) 2023 by (C) LRA - ENSA Toulouse / LMDC - INSA Toulouse / LISST - UT2J
        email                : lra-tech@toulouse.archi.fr
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

__author__ =  'Serge Faraut, Lorena de Carvalho Araujo - (C) LRA - ENSA Toulouse'
__date__ = '2023-06-30'
__version__ = '0.0.7'
__copyright__ = '(C) 2023 by (C) LRA - ENSA Toulouse / LMDC - INSA Toulouse / LISST - UT2J'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import os
import sys
import inspect
from pathlib import Path

from qgis.core import QgsProcessingAlgorithm, QgsApplication

cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]

if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

user_dirpath = QgsApplication.qgisSettingsDirPath() #'C:/Users/Username/AppData/Roaming/QGIS/QGIS3\\profiles\\default/'
user_dirpath = Path(user_dirpath)
#danube_dirpath = os.path.join(user_dirpath, r'python\plugins\Danube_Tool')
danube_dirpath =  str(Path(user_dirpath) / "python" / "plugins" / "Danube_Tool")
if danube_dirpath not in sys.path:
    sys.path.append(danube_dirpath)

#danube_preprocess_dirpath = os.path.join(user_dirpath, r'python\plugins\Danube_Tool\DANUBE_preprocessing_tools')
danube_preprocess_dirpath = str(Path(user_dirpath)  / "python" / "plugins" / "Danube_Tool" / "DANUBE_preprocessing_tools")
if danube_preprocess_dirpath not in sys.path:
    sys.path.append(danube_preprocess_dirpath)

from .DANUBE_tool_provider import DANUBEtoolProvider
### Import DANUBE layers definition
try: DANUBE_LAYERS
except NameError: from DANUBE_config import DANUBE_LAYERS


class DANUBEtoolPlugin(object):
    global DANUBE_LAYERS
    def __init__(self):
        self.provider = None

    def initProcessing(self):
        """Init Processing provider for QGIS >= 3.8."""
        self.provider = DANUBEtoolProvider()
        QgsApplication.processingRegistry().addProvider(self.provider)

    def initGui(self):
        self.initProcessing()

    def unload(self):
        ### Remove Modules paths
        sys.path.remove(danube_preprocess_dirpath)
        sys.path.remove(danube_dirpath)
        QgsApplication.processingRegistry().removeProvider(self.provider)
