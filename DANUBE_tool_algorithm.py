# -*- coding: utf-8 -*-

"""
/***************************************************************************
 DANUBEtool
                                 A QGIS plugin
 DANUBE Tool plugin allows you to generate spatialized buildings' material informations from DANUBE database and urban scale typomorphological informations (IGN BDTOPO data and Geoclimate tool's outputs)  
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2023-03-31
        copyright            : (C) 2023 by (C) LRA - ENSAT Toulouse / LMDC - INSA Toulouse / LISST - UT2J
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

__author__ = 'Serge Faraut - (C) LRA - ENSAT Toulouse'
__date__ = '2023-03-31'
__copyright__ = '(C) 2023 by (C) LRA - ENSAT Toulouse / LMDC - INSA Toulouse / LISST - UT2J'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

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
                       QgsProcessingParameterNumber
                       )


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

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.

    OUTPUT = 'OUTPUT'
    INPUT = 'INPUT'
    INPUT_BUILDINGS = 'INPUT_BUILDINGS'
    FILOSOFI = 'FILOSOFI'

    def initAlgorithm(self, config):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        # Add the Geoclimate vector features source input folder. 
        self.addParameter(
            QgsProcessingParameterFile(
                self.INPUT,
                self.tr('Geoclimate Input layers folder'),
                behavior=QgsProcessingParameterFile.Folder  
            )
        )
        
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT_BUILDINGS,
                self.tr('Geoclimate Buildings layer'),
                [QgsProcessing.TypeVectorAnyGeometry]
            )
        )
        
        # Add the FILOSOFI vector features layer (INSEE data at grid format). 
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.FILOSOFI,
                self.tr('FILOSOFI Input layers'),
                [QgsProcessing.TypeVectorAnyGeometry]
            )
        )
        
        # We add a feature sink in which to store our processed features (this
        # usually takes the form of a newly created vector layer when the
        # algorithm is run in QGIS).
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                self.tr('DANUBE Data Output layer')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """

        # Retrieve the feature source and sink. The 'dest_id' variable is used
        # to uniquely identify the feature sink, and must be included in the
        # dictionary returned by the processAlgorithm function.
        #source = self.parameterAsSource(parameters, self.INPUT, context)
        source_folder = self.parameterAsFile(parameters, self.INPUT_BUILDINGS, context)
        source = self.parameterAsSource(parameters, self.INPUT_BUILDINGS, context)
        (sink, dest_id) = self.parameterAsSink(parameters, self.OUTPUT,
                context, source.fields(), source.wkbType(), source.sourceCrs())
        ### A tester : self.parameterDefinition('INPUT').valueAsPythonString(parameters['INPUT'], context)
        #print('Geoclimate Input layers folder:'+str(source_folder))
        #QgsMessageLog.logMessage('Geoclimate Input layers folder:'+str(source_folder_path), 'DANUBE tool', level=Qgis.Info)
        #Display Geoclimate folder path inputs
        source_folder_path = self.parameterDefinition('INPUT').valueAsPythonString(parameters['INPUT'], context)
        QgsMessageLog.logMessage('Geoclimate Input layers folder:'+str(source_folder_path), 'DANUBE tool', level=Qgis.Info)

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

        # Return the results of the algorithm. In this case our only result is
        # the feature sink which contains the processed features, but some
        # algorithms may return multiple feature sinks, calculated numeric
        # statistics, etc. These should all be included in the returned
        # dictionary, with keys matching the feature corresponding parameter
        # or output names.
        return {self.OUTPUT: dest_id}

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

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return DANUBEtoolAlgorithm()
