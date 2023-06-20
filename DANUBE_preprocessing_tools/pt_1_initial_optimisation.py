import logging
from datetime import datetime

from pathlib import Path
import processing
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

from pt_basic_functions import open_layer, printd, DEBUG


# TODO #############################################
# # define log file
#   # for Python3
# name_executed = 'TEST'
# name_log = f'myLog_{name_executed}_{datetime.now().strftime("%m-%d-%Y_%Hh%Mmin")}.log'
# handlers = [logging.FileHandler(name_log), logging.StreamHandler()]
# logging.basicConfig(level = logging.INFO,
#                     format = '  %(message)s',
#                     handlers = handlers)
# log_dir = r"C:\Users\lorena.carvalho\Documents\Develop_outil\code\pyqgis\logging info test"
# os.chmod(log_dir, 0o777)


def geoclimate_to_gpkg(root_path_geo):
    """ open geoclimate files and convert them into gpkg format
    Parameters:
        root_path_geo (str): the local path of the geoclimate folder
    Returns:
        layers_geo_gpkg (dict) : a dictionnary of the geoclimate layers further
        used in the pre-treatement.
    """
    files_geo = {
                # "geo_build_ind" : "building_indicators.geojson",
                # "geo_build_utrf" : "building_utrf.geojson",
                # "geo_rsu_utrf" : "rsu_utrf_area.geojson",
                "geo_zone" : "zone.geojson",
                }
    printd('_'*21,'files_geo', '_'*21)
    printd(files_geo)

    # construct path of geoclimate files
    paths_geo = {k : root_path_geo / v for (k,v) in files_geo.items()}
    printd('_'*21,'paths_geo', '_'*21)
    printd(paths_geo)

    # convert path in string (which is accepted by the QGIS layer object constructor)
    paths_geo = {k : str(v) for (k,v) in paths_geo.items()}
    printd('_'*21,'paths_geo in str', '_'*21)
    printd(paths_geo)

    # open geoclimate layers
    layers_geo = {name_layer : open_layer(path_layer) for (name_layer,path_layer) in paths_geo.items()}
    printd('_'*21,'layers_geo', '_'*21)
    printd(layers_geo)

    # save layer as gpkg in the computer and return a layer
    def save_in_gpkg_open(layer, layer_name):
        # Turn QgsProcessingAlgorithm "Save vector features to file"
        result = processing.run("native:savefeatures",
                                {'INPUT':layer,
                                'LAYER_NAME': layer_name,
                                'OUTPUT':QgsProcessing.TEMPORARY_OUTPUT
                                })
        print(type(result.values()))
        layer = open_layer(result['FILE_PATH'])
        printd('_'*21,'saved layer in gpk', '_'*21)
        printd(layer)

        if DEBUG == True:
            # add layer to open project in QGIS
            layer.setName(layer_name)
            QgsProject.instance().addMapLayer(layer)

        return layer

    layers_geo_gpkg = {layer_name : save_in_gpkg_open(layer, layer_name) for (layer_name,layer) in layers_geo.items()}
    printd('_'*21,'layers_geo_gpkg', '_'*21)
    printd(layers_geo_gpkg)

    return layers_geo_gpkg

def main_1():
    print("\n")
    print("#" * 60)
    print("Run main 1 : Initial optimisations")
    print("#" * 60)
    root_path_geo = Path(r"C:\Users\lorena.carvalho\Documents\Develop_outil\data\Haute_Garonne\Geoclimate\Geoclimate-bdtopo_v3_Toulouse_31555_20042023")
    ######## around 4 min to Toulouse in my computer
    layers = geoclimate_to_gpkg(root_path_geo)

    city_id =  [feature['ID_ZONE'] for feature in layers['geo_zone'].getFeatures()][0]
    print('_'*21,'city_id', '_'*21,'\n')
    print(city_id)



if __name__ == '__console__':
    main_1()
