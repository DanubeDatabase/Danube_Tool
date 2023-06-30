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
                       QgsMessageLog,
                       QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterVectorDestination,
                       QgsProcessingParameterFile,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterNumber,
                       QgsProcessingMultiStepFeedback,
                       QgsProcessingParameterVectorLayer,
                       QgsProcessingParameterDefinition,
                       )

### Import processing (QGIS >= 3.4) - For QGIS < 3.4 : from qgis import processing
import processing

### Import DANUBE layers definition
from DANUBE_config import DANUBE_LAYERS, DEBUG

### TODO : include process function
# from main_preprocess import main_preprocess_all_plugin


#### Sample preprocesss function
def process_function_launch(self, parameters, context, feedback):
    ####
    if DEBUG: QgsMessageLog.logMessage('In process_function_launch: self.DANUBE_tool_LAYERS.[DANUBE_BUILD_PREPROCESS].source:'+str(self.DANUBE_tool_LAYERS["DANUBE_BUILD_PREPROCESS"]["layer"].source()), 'DANUBE tool', level=Qgis.Info)
    if DEBUG: QgsMessageLog.logMessage('In process_function_launch: DOING NOTHING YET', 'DANUBE tool', level=Qgis.Info)
    ## TODO: call process function
    ## main_preprocess_all_plugin(self, parameters, context, feedback)
    
    return