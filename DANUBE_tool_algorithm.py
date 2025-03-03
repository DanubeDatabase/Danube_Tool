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
__copyright__ = '(C) 2023 by (C) LRA - ENSA Toulouse / LMDC - INSA Toulouse / LISST - UT2J'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

ADD_ALL_LAYERS = True

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
                       QgsProject, QgsApplication, QgsField, QgsFeatureRequest, QgsVectorLayer,
                       edit
                       )
from qgis.PyQt.QtCore import QVariant

### Import processing (QGIS >= 3.4) - For QGIS < 3.4 : from qgis import processing
import processing

### Import DANUBE layers definition
#try: DANUBE_LAYERS
#except NameError: from DANUBE_config import DANUBE_LAYERS
from DANUBE_config import DANUBE_LAYERS, DEBUG

#TEMPO: Force DEBUG mode:
DEBUG = True

from DANUBE_processing_tools import danube_process_launch_old

class DANUBEtoolAlgorithm(QgsProcessingAlgorithm):
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

    def initAlgorithm(self, config):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """
        
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                DANUBE_LAYERS["DANUBE_BUILD_PREPROCESS"]["id"],
                self.tr('Pre-processed building data layer (from step1)'),
                [QgsProcessing.TypeVectorAnyGeometry]
            )
        )
        
        # We add a Vector layer in which to store the final DANUBE processed features (this
        # usually takes the form of a newly created vector layer when the
        # algorithm is run in QGIS).        
        self.addParameter(
            QgsProcessingParameterVectorDestination(
                DANUBE_LAYERS["DANUBE_BUILD_DATA"]["id"],
                self.tr('DANUBE Data Output layer')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        ### Import DANUBE DATABASE module, create instance and load DANUBE data
        from PyDANUBE import DANUBE_database
        db = DANUBE_database()
        db.DANUBE_load_database()
        # Add and initialize new DANUBE_tool_LAYERS attribute's values with input layers constants, using deepcopy !
        setattr(self,'DANUBE_tool_LAYERS', copy.deepcopy(DANUBE_LAYERS))
        # Retrieve the feature source and sink. The 'dest_id' variable is used
        # to uniquely identify the feature sink, and must be included in the
        # dictionary returned by the processAlgorithm function.
        #source = self.parameterAsSource(parameters, self.INPUT, context)
        #source_folder = self.parameterAsFile(parameters, self.INPUT_BUILDINGS, context)
        #source = self.parameterAsSource(parameters, DANUBE_LAYERS["DANUBE_BUILD_PREPROCESS"]["id"], context)
        ### Create a sink layer with same property as DANUBE_BUILD_PREPROCESS layer
        #(sink, dest_id) = self.parameterAsSink(parameters, DANUBE_LAYERS["DANUBE_BUILD_DATA"]["id"],
        #        context, source.fields(), source.wkbType(), source.sourceCrs())
        self.DANUBE_tool_LAYERS["DANUBE_BUILD_PREPROCESS"]["layer"] = self.parameterAsVectorLayer(parameters, self.DANUBE_tool_LAYERS["DANUBE_BUILD_PREPROCESS"]["id"], context)
        output_data_layer = self.parameterAsOutputLayer(parameters, self.DANUBE_tool_LAYERS["DANUBE_BUILD_DATA"]["id"], context)
        self.DANUBE_tool_LAYERS["DANUBE_BUILD_DATA"]["layer"] = output_data_layer
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
        # Return the results of the algorithm. In this case our only result is
        # the feature sink which contains the processed features, but some
        # algorithms may return multiple feature sinks, calculated numeric
        # statistics, etc. These should all be included in the returned
        # dictionary, with keys matching the feature corresponding parameter
        # or output names.

        feedback.pushInfo("Launching DANUBE process phase......")
        #danube_process_launch.process_function_launch(self, parameters, context, feedback)

        ## Create output layer
        layer_source = self.DANUBE_tool_LAYERS["DANUBE_BUILD_PREPROCESS"]["layer"]
        if DEBUG: QgsMessageLog.logMessage('DANUBE_BUILD_PREPROCESS Layer source:'+str(self.DANUBE_tool_LAYERS["DANUBE_BUILD_PREPROCESS"]["layer"].source()), 'DANUBE tool', level=Qgis.Info)
        #layer_destination_plugin = self.DANUBE_tool_LAYERS["DANUBE_BUILD_DATA"]["layer"]
        layer_source.selectAll()
        layer_destination_plugin = processing.run("native:saveselectedfeatures", {'INPUT': layer_source, 'OUTPUT':'TEMPORARY_OUTPUT'})['OUTPUT']
        layer_source.removeSelection()
        if DEBUG: QgsMessageLog.logMessage('Initial DANUBE layer created...'+'Layer:'+str(layer_destination_plugin.source()), 'DANUBE tool', level=Qgis.Info)
        if ADD_ALL_LAYERS: QgsProject.instance().addMapLayer(layer_destination_plugin)

        ### Add DANUBE archetype attribute
        layer_destination_plugin.startEditing()

        pr = layer_destination_plugin.dataProvider()
        pr.addAttributes([QgsField('danube_archetype', QVariant.String)])
        layer_destination_plugin.updateFields()
        #print(layer_destination_plugin.fields().names())
        if DEBUG: QgsMessageLog.logMessage('Fields:' + str(list(layer_destination_plugin.fields().names())), 'DANUBE tool', level=Qgis.Info)

        request = QgsFeatureRequest().setFlags(QgsFeatureRequest.NoGeometry).setSubsetOfAttributes(
            ['danube_archetype', 'typology_danube', 'usage_danube', 'year_constr', 'location_comm'],
            layer_destination_plugin.fields())
        index_archetype = layer_destination_plugin.fields().indexFromName("danube_archetype")
        index_typo = layer_destination_plugin.fields().indexFromName("typology_danube")
        index_usage = layer_destination_plugin.fields().indexFromName("usage_danube")
        index_date = layer_destination_plugin.fields().indexFromName("year_constr")
        index_location = layer_destination_plugin.fields().indexFromName("location_comm")
        print('Indexes:', index_archetype, index_typo, index_usage, index_date, index_location)
        if DEBUG: QgsMessageLog.logMessage('Indexes:' + str(list(index_archetype, index_typo, index_usage, index_date, index_location)), 'DANUBE tool', level=Qgis.Info)

        # Compute the number of steps to display within the progress bar and
        # get features from source
        total = 100.0 / layer_destination_plugin.featureCount() if layer_destination_plugin.featureCount() else 0
        attr_map = {}
        current = 0
        for line in layer_destination_plugin.getFeatures(request):
            if feedback.isCanceled():
                break
            ### Get Archetype from DANUBE
            ### TODO : Get real value from Database
            archetype = str(line[index_typo]) + '-' + str(line[index_usage]) + '-' + str(line[index_date])
            ### TODO : Optimize: Location is constant in loop (hypothesis) - Data fetc can be optimized
            """
            archetype = db.DANUBE_get_archetype(Nom_typologie=str(line[index_typo]), Usage=str(line[index_usage]),
                                                     Construction_date=str(int(float(line[index_date]))),
                                                     Location=str(line[index_location]), scale='COMMUNE')
            """
            attr_map[line.id()] = {index_archetype: archetype}
            feedback.setProgress(int(current * total))
            current = current + 1
        layer_destination_plugin.dataProvider().changeAttributeValues(attr_map)

        #return {self.DANUBE_tool_LAYERS["DANUBE_BUILD_DATA"]["id"]: self.DANUBE_tool_LAYERS["DANUBE_BUILD_DATA"]["layer"]}
        return {self.DANUBE_tool_LAYERS["DANUBE_BUILD_DATA"]["id"]: layer_destination_plugin}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'Generate DANUBE\'s building data'

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
        Select data source layers (including pre-process data) for DANUBE data generation . New layer with all DANUBE generated building's information layers will be created.
        """

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return DANUBEtoolAlgorithm()
