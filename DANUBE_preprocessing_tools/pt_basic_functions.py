from qgis.core import QgsField, QgsProject, QgsVectorLayer, QgsVectorLayerJoinInfo
from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (Qgis,
                        QgsFeature,
                        QgsPoint,
                        QgsMessageLog,
                        QgsProcessing,
                        QgsFeatureSink,
                        QgsProcessingAlgorithm,
                        QgsProcessingParameterVectorDestination,
                        QgsProcessingParameterFile,
                        QgsProcessingParameterFeatureSource,
                        QgsProcessingParameterFeatureSink,
                        QgsProcessingParameterNumber,
                        QgsVectorLayer
                       )
# from PyQt4.QtCore import QVariant

import pandas as pd
import processing
from pathlib import Path


#___________________Set debug mode___________________

DEBUG = True

#___________________Open layers___________________

#
def check_validity(layer):
    # Check if the layer is valid
    if layer.isValid():
        print(f"\nLayer '{layer.name()}' is valid. \n")
        # Perform the required operations on the layer
        layer.startEditing()  # Start editing the layer
        layer.triggerRepaint()  # Refresh the layer to show changes
        layer.commitChanges()  # Save the changes to the layer
    else:
        print(f"\nLayer '{layer.name()}' is NOT valid!\n")


def open_layer(layer_path_or_name):
    """ Get the layer by its name or ID"""

    if type(layer_path_or_name) is str:
        if Path(layer_path_or_name).is_file():
            layer = QgsVectorLayer(layer_path_or_name, Path(layer_path_or_name).stem, 'ogr') # open layer from path
            check_validity(layer)
            return layer

        else:
            if layer_path_or_name in [vectl.name() for vectl in list(QgsProject.instance().mapLayers().values())]:  # test if the layer_path_or_name is an open layer
                layer = QgsProject.instance().mapLayersByName(layer_path_or_name)[0] # Retrieves the first open layer with the given name
                check_validity(layer)
                return layer

            else:
                print('name layer not recognized')
    else:
        print('Please enter a string type')

def printd(obj1, obj2 = '', obj3 = '', obj4 = '' ):
    if DEBUG == True:
        print('\n',obj1, obj2, obj3, obj4)


if __name__ == '__console__':
    def test_printd():
        printd("Printing", "in debug", 'mode', 'is working!')

    def test_open_layer():
        path = r"C:\Users\lorena.carvalho\Documents\Develop_outil\data\small_sample\sample_topo_bati.gpkg"
        layer_names = [layer.name() for layer in QgsProject.instance().mapLayers().values()]
        layer_from_path = open_layer(path_or_layer)
        print("open_layer from path is working!" )
        print(layer_from_path.fields().names())

        if len(layer_names) > 0:
            layer_name = layer_names[0]
            layer_from_name = open_layer(layer_name)
            print("open_layer from layer name is working!" )
            print(layer_from_name.fields().names())
        else:
            print('No layers are presently open in QGIS. Open a layer in the GIU to test this function')

    DEBUG = True
    test_printd()
    test_open_layer()
