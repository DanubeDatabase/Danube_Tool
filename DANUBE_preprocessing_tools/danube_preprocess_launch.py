# -*- coding: utf-8 -*-

"""
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (Qgis,
                       QgsProcessing,
                       QgsMessageLog,
                       QgsFeatureSink,
                       QgsProcessingException,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterVectorDestination,
                       QgsProcessingParameterFile,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterFeatureSink)

from main_preprocess import main_preprocess_all_plugin
from DANUBE_config import DEBUG

GEOCLIMATE_INPUT_BUILDINGS_UTRF = 'GEOCLIMATE_INPUT_BUILDINGS_UTRF'
OUTPUT = 'OUTPUT'
FILOSOFI = 'FILOSOFI'
global DANUBE_LAYERS

#### Sample preprocesss function
def preprocess_function_launch(self, parameters, context, feedback):
        ####
        global DANUBE_LAYERS
        #source = self.parameterAsSource(parameters, GEOCLIMATE_INPUT_BUILDINGS_UTRF, context)
        #(sink, dest_id) = self.parameterAsSink(parameters, self.OUTPUT,
        #        context, source.fields(), source.wkbType(), source.sourceCrs())
        ###TEMPO### affichage dossier
        #source_folder_path = self.parameterDefinition('GEOCLIMATE_INPUT_BUILDINGS_UTRF').valueAsPythonString(parameters['GEOCLIMATE_INPUT_BUILDINGS_UTRF'], context)
        #source_folder_path = self.parameterDefinition(DANUBE_LAYERS["GEO_BUILD_URTF"]["id"]).valueAsPythonString(parameters[DANUBE_LAYERS["GEO_BUILD_URTF"]["id"]], context)
        #QgsMessageLog.logMessage('Geoclimate Building UTRF layer (in preprocess_function_sample()) :'+str(source_folder_path), 'DANUBE tool', level=Qgis.Info)
        #QgsMessageLog.logMessage('Geoclimate Building UTRF layer id (in preprocess_function_sample()) :'+str(DANUBE_LAYERS["GEO_BUILD_URTF"]["id"]), 'DANUBE tool', level=Qgis.Info)
        # if DEBUG: QgsMessageLog.logMessage('In preprocess_lauch: DANUBE_Layers='+str(self.DANUBE_tool_LAYERS), 'DANUBE tool', level=Qgis.Info)
        if DEBUG: QgsMessageLog.logMessage('    self.DANUBE_tool_LAYERS.[GEO_ZONE].source:'+str(self.DANUBE_tool_LAYERS["GEO_BUILD_URTF"]["layer"].source()), 'DANUBE tool', level=Qgis.Info)
        main_preprocess_all_plugin(self, parameters, context, feedback)
        if DEBUG: QgsMessageLog.logMessage('From main_preprocess_all_plugin DANUBE_BUILD_DATA:'+str(self.DANUBE_tool_LAYERS["DANUBE_BUILD_DATA"]["layer"].source()), 'DANUBE tool', level=Qgis.Info)
        return
