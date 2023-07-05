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
__date__ = '2023-06-19'
__copyright__ = '(C) 2023 by (C) LRA - ENSA Toulouse / LMDC - INSA Toulouse / LISST - UT2J'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import os
from pathlib import Path
import copy

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
#try: DANUBE_LAYERS
#except NameError: from DANUBE_config import DANUBE_LAYERS
from DANUBE_config import DANUBE_LAYERS, DEBUG

from DANUBE_preprocessing_tools import danube_preprocess_launch


class DANUBEtool_preprocess(QgsProcessingAlgorithm):
    """
    This is an example algorithm that takes a vector layer and
    creates a new identical one.

    It is meant to be used as an example of how to create your own
    algorithms and explain methods and variables used to do it. An
    algorithm like this will be available in all elements, and there
    is not need for additional work.

    All Processing algorithms should extend the QgsProcessingAlgorithm
    class.
    """

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.

    OUTPUT = 'OUTPUT'
    INPUT = 'INPUT'
    GEO_INPUT_FOLDER = 'GEO_INPUT_FOLDER'
    GEOCLIMATE_INPUT_BUILDINGS_UTRF = 'GEOCLIMATE_INPUT_BUILDINGS_UTRF'
    BDTOPO_INPUT_BUILDINGS = 'BDTOPO_INPUT_BUILDINGS'
    BDTOPO_INPUT_ACTIVITIES = 'BDTOPO_INPUT_ACTIVITIES'
    FILOSOFI = 'FILOSOFI'
    global DANUBE_LAYERS
    #DANUBE_tool_LAYERS = DANUBE_LAYERS

    def initAlgorithm(self, config):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        global DANUBE_LAYERS
        # Add the Geoclimate vector features source input folder.
        self.addParameter(
            QgsProcessingParameterFile(
                self.GEO_INPUT_FOLDER,
                self.tr('Geoclimate Input layers folder (not used yet)'),
                behavior=QgsProcessingParameterFile.Folder
            )
        )

        # Define Geoclimate Zone layer
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                DANUBE_LAYERS["GEO_ZONE"]["id"],
                self.tr('Geoclimate Zone input layer'),
                [QgsProcessing.TypeVectorAnyGeometry]
            )
        )

       # Define Geoclimate Building Indicators
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                DANUBE_LAYERS["GEO_BUILD_IND"]["id"],
                self.tr('Geoclimate Building Indicators input layer'),
                [QgsProcessing.TypeVectorAnyGeometry]
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                DANUBE_LAYERS["GEO_BUILD_URTF"]["id"],
                self.tr('Geoclimate Buildings UTRF layer'),
                [QgsProcessing.TypeVectorAnyGeometry]
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                DANUBE_LAYERS["GEO_RSU_UTRF_FLOOR_AREA"]["id"],
                self.tr('Geoclimate RSU UTRF FLOOR AREA layer'),
                [QgsProcessing.TypeVectorAnyGeometry]
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                DANUBE_LAYERS["TOPO_BATI"]["id"],
                self.tr('BDTOPO V3 Buildings layer'),
                [QgsProcessing.TypeVectorAnyGeometry]
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                DANUBE_LAYERS["TOPO_ACTIVITE"]["id"],
                self.tr('BDTOPO V3 Activities and Interest Zones layer'),
                [QgsProcessing.TypeVectorAnyGeometry]
            )
        )

        # Add the FILOSOFI vector features layer (INSEE data at grid format).
        ###TODO### Preload FILOSOFI layer with DANUBE embeded data layer
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                DANUBE_LAYERS["FILOSOFI"]["id"],
                self.tr('FILOSOFI Input layers'),
                [QgsProcessing.TypeVectorAnyGeometry]
            )
        )

        # We add a Vector layer in which to store our processed features (this
        # usually takes the form of a newly created vector layer when the
        # algorithm is run in QGIS).
        self.addParameter(
            QgsProcessingParameterVectorDestination(
                DANUBE_LAYERS["DANUBE_BUILD_PREPROCESS"]["id"],
                self.tr('Pre-processed Data Output layer')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        global DANUBE_LAYERS ## Global layers definition
        
        # Init progress bar to 0
        feedback.setProgress(int(0))
        # Retrieve the feature source and sink. The 'dest_id' variable is used
        # to uniquely identify the feature sink, and must be included in the
        # dictionary returned by the processAlgorithm function.
        #source = self.parameterAsSource(parameters, self.INPUT, context)
        source_folder = self.parameterAsFile(parameters, DANUBE_LAYERS["GEO_BUILD_URTF"]["id"], context)
        source = self.parameterAsSource(parameters, DANUBE_LAYERS["GEO_BUILD_URTF"]["id"], context)
        ### Create a sink layer with same property as DANUBE_BUILD_PREPROCESS layer
        (sink, dest_id) = self.parameterAsSink(parameters, DANUBE_LAYERS["DANUBE_BUILD_PREPROCESS"]["id"],
                context, source.fields(), source.wkbType(), source.sourceCrs())
        ### A tester : self.parameterDefinition('INPUT').valueAsPythonString(parameters['INPUT'], context)
        #print('Geoclimate Input layers folder:'+str(source_folder))
        #QgsMessageLog.logMessage('Geoclimate Input layers folder:'+str(source_folder_path), 'DANUBE tool', level=Qgis.Info)
        #Display Geoclimate folder path inputs
        source_folder_path = self.parameterDefinition('GEO_INPUT_FOLDER').valueAsPythonString(parameters['GEO_INPUT_FOLDER'], context)
        QgsMessageLog.logMessage('Geoclimate Input layers folder:'+str(source_folder_path), 'DANUBE tool', level=Qgis.Info)
        source_folder_path = Path(source_folder_path)
        # Add and initialize new DANUBE_tool_LAYERS attribute's values with input layers constants, using deepcopy !
        setattr(self,'DANUBE_tool_LAYERS', copy.deepcopy(DANUBE_LAYERS))
        #self.DANUBE_tool_LAYERS["GEO_ZONE"]["layer"] = self.parameterAsVectorLayer(parameters, DANUBE_LAYERS["GEO_ZONE"]["id"], context)
        if DEBUG: QgsMessageLog.logMessage('GEO_ZONE layer from parameter:'+str(self.parameterAsVectorLayer(parameters, DANUBE_LAYERS["GEO_ZONE"]["id"], context)), 'DANUBE tool', level=Qgis.Info)
        self.DANUBE_tool_LAYERS["GEO_ZONE"]["layer"] = self.parameterAsVectorLayer(parameters,DANUBE_LAYERS["GEO_ZONE"]["id"], context)
        self.DANUBE_tool_LAYERS["GEO_BUILD_URTF"]["layer"] = self.parameterAsVectorLayer(parameters, DANUBE_LAYERS["GEO_BUILD_URTF"]["id"], context)
        self.DANUBE_tool_LAYERS["GEO_BUILD_IND"]["layer"] = self.parameterAsVectorLayer(parameters, DANUBE_LAYERS["GEO_BUILD_IND"]["id"], context)
        self.DANUBE_tool_LAYERS["GEO_RSU_UTRF_FLOOR_AREA"]["layer"] = self.parameterAsVectorLayer(parameters, DANUBE_LAYERS["GEO_RSU_UTRF_FLOOR_AREA"]["id"], context)
        self.DANUBE_tool_LAYERS["TOPO_BATI"]["layer"] = self.parameterAsVectorLayer(parameters, DANUBE_LAYERS["TOPO_BATI"]["id"], context)
        self.DANUBE_tool_LAYERS["TOPO_ACTIVITE"]["layer"] = self.parameterAsVectorLayer(parameters, DANUBE_LAYERS["TOPO_ACTIVITE"]["id"], context)
        self.DANUBE_tool_LAYERS["FILOSOFI"]["layer"] = self.parameterAsVectorLayer(parameters, DANUBE_LAYERS["FILOSOFI"]["id"], context)
        output_data_layer = self.parameterAsOutputLayer(parameters, DANUBE_LAYERS["DANUBE_BUILD_PREPROCESS"]["id"], context)
        self.DANUBE_tool_LAYERS["DANUBE_BUILD_PREPROCESS"]["layer"] = output_data_layer
        #self.DANUBE_tool_LAYERS["DANUBE_BUILD_PREPROCESS"]["layer"] = sink

        if DEBUG: QgsMessageLog.logMessage('DANUBE_LAYERS[GEO_ZONE]:'+str(DANUBE_LAYERS["GEO_ZONE"]), 'DANUBE tool', level=Qgis.Info)
        if DEBUG: QgsMessageLog.logMessage('self.DANUBE_tool_LAYERS.[GEO_ZONE].source:'+str(self.DANUBE_tool_LAYERS["GEO_ZONE"]["layer"].source()), 'DANUBE tool', level=Qgis.Info)
        #if DEBUG: QgsMessageLog.logMessage('DANUBE_tool_LAYERS:'+str(self.DANUBE_tool_LAYERS), 'DANUBE tool', level=Qgis.Info)
        if DEBUG: QgsMessageLog.logMessage('self.DANUBE_tool_LAYERS.[DANUBE_BUILD_PREPROCESS].source:'+str(self.DANUBE_tool_LAYERS["DANUBE_BUILD_PREPROCESS"]["layer"]), 'DANUBE tool', level=Qgis.Info)

        """
        # Compute the number of steps to display within the progress bar and
        # get features from source
        total = 100.0 / source.featureCount() if source.featureCount() else 0

        features = source.getFeatures()
        for current, feature in enumerate(features):
            # Stop the algorithm if cancel button has been clicked
            if feedback.isCanceled():
                break
            # Add a feature in the sink
            sink.addFeature(feature, QgsFeatureSink.FastInsert)
            # Update the progress bar
            feedback.setProgress(int(current * total))
        """
        # Launch pre-process workflow with self parameter containing all layers' informations self.DANUBE_tool_LAYERS)
        # TODO: feedback parameter should be used for user feedback processing progression
        # Other parameters currently unused
        danube_preprocess_launch.preprocess_function_launch(self, parameters, context, feedback)
        feedback.pushInfo("Launching preprocess phase...")
        # Returned layer (BUILD_PP_OUTPUT) must be copied to plugin file destination (DANUBE_BUILD_PREPROCESS)
        # Using "saveselectedfeature" QGIS processing - CSR and features are kepts!
        feedback.pushInfo("Saving processing results...")
        layer_source = self.DANUBE_tool_LAYERS["BUILD_PP_OUTPUT"]["layer"]
        layer_destination_plugin = self.DANUBE_tool_LAYERS["DANUBE_BUILD_PREPROCESS"]["layer"]
        layer_source.selectAll()
        copied_layer = processing.run("native:saveselectedfeatures", {'INPUT': layer_source, 'OUTPUT': layer_destination_plugin})['OUTPUT']
        layer_source.removeSelection()
        
        # Return the results of the algorithm. In this case our only result is
        # the feature sink which contains the processed features, but some
        # algorithms may return multiple feature sinks, calculated numeric
        # statistics, etc. These should all be included in the returned
        # dictionary, with keys matching the feature corresponding parameter
        # or output names.
        # Call external preprocess funtion (preprocess folder
        # Must return result layer(s)
        feedback.pushInfo("Done with processing.")
        return {self.DANUBE_tool_LAYERS["DANUBE_BUILD_PREPROCESS"]["id"]: self.DANUBE_tool_LAYERS["DANUBE_BUILD_PREPROCESS"]["layer"]}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'Data preprocessing for DANUBE generation'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr(self.name())

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr(self.groupId())

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'DANUBE tool'
    def shortHelpString(self):
        return """
        Select data source layers for DANUBE Pre-processing (BDTOPO V3, Geoclimate, FILOSOFI). New indicators layers will be genererated.
        """

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return DANUBEtool_preprocess()
