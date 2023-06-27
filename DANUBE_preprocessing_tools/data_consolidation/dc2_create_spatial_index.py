import processing
from qgis.core import (
                        QgsFeatureSource,
                        QgsProcessing
                      )

from dev_set_test import DEV_OUTSIDE_PLUGIN, print_d, open_layer, add_layer_gui

def geoclimate_to_gpkg(DANUBE_LAYERS):
    """ save layer as gpkg in the temporary memory and open this layer"""
    print_d('_' * 21, 'Start conversion of geojson layers to gpkg', '_' * 21)

    def save_in_gpkg_open(layer, layer_name):
        """Run QgsProcessingAlgorithm 'Save vector features to file'"""
        print_d('_' * 21, 'save layer in gpk', '_' * 21)
        print_d(layer_name)
        result = processing.run("native:savefeatures",
                                {'INPUT':layer,
                                'LAYER_NAME': layer_name,
                                'OUTPUT':QgsProcessing.TEMPORARY_OUTPUT
                                })
        print_d(result['OUTPUT'])
        layer = open_layer(result['FILE_PATH'])
        return layer

    lays_to_convert = ['GEO_ZONE','GEO_RSU_UTRF_FLOOR_AREA','DANUBE_BUILD_PREPROCESS']

    for lay_name in lays_to_convert:
        print_d('Converting', lay_name)
        DANUBE_LAYERS[lay_name]['layer'] = save_in_gpkg_open(DANUBE_LAYERS[lay_name]['layer'], lay_name)

    print_d('_' * 21, 'End conversion of geojson layers to gpkg', '_' * 21, '\n')

    return DANUBE_LAYERS


def spatial_index_layers_to_be_used(DANUBE_LAYERS):
    """Creates spatial index to the layers which will be further used, if not already present"""

    def check_spatial_index(layer):
        """Check the spatial index status of a layer"""
        if layer.hasSpatialIndex() == QgsFeatureSource.SpatialIndexNotPresent:
            print_d("Spatial Index not present")
        elif layer.hasSpatialIndex() == QgsFeatureSource.SpatialIndexUnknown:
            print_d("Spatial Index unknown")
        elif layer.hasSpatialIndex() == QgsFeatureSource.SpatialIndexPresent:
            print_d("Spatial Index present")
        else:
            print_d("Could not verify the existence of spatial index")

    def check_and_run_spatial_index(layer_name, layer):
        """Run Spatial index, if not already present """
        print_d(layer_name)
        check_spatial_index(layer)
        if layer.hasSpatialIndex() == QgsFeatureSource.SpatialIndexPresent:
            print_d("No need to run spatial index")
            print_d("_" * 30)
        else:
            print_d("Run spatial index")
            processing.run("native:createspatialindex",{'INPUT':layer})
            print_d("after run spatial index")
            check_spatial_index(layer)
            print_d("_" * 30)

    # create spatial index to the layers which will be further used
    danube_lay_keys_to_be_used = ['TOPO_ACTIVITE', 'FILOSOFI', 'GEO_ZONE','GEO_RSU_UTRF_FLOOR_AREA','DANUBE_BUILD_PREPROCESS']
    for dan_lay in danube_lay_keys_to_be_used:
        layer_to_be_used = DANUBE_LAYERS[dan_lay]['layer']
        name_layer_to_be_used = DANUBE_LAYERS[dan_lay]['id']
        check_and_run_spatial_index(name_layer_to_be_used, layer_to_be_used)


def main_dc_2(DANUBE_LAYERS):
    """Perform actions needed to provide spatial index to all layer which will be further used in the workflow"""
    print("\n")
    print("*" * 100)
    print("Run step 2 of data consolidation: Convert geoclimate source layers to gpkg and create spatial index if needed")
    print("*" * 100)
    DANUBE_LAYERS = geoclimate_to_gpkg(DANUBE_LAYERS)

    spatial_index_layers_to_be_used(DANUBE_LAYERS)

    add_layer_gui(DANUBE_LAYERS['GEO_ZONE']['layer'], 'GEO_ZONE')

    if not DEV_OUTSIDE_PLUGIN:
        city_id =  [feature['ID_ZONE'] for feature in DANUBE_LAYERS['GEO_ZONE']['layer'].getFeatures()][0]
        print_d('_' * 21, 'city_id', '_' * 21, '\n')
        print_d(city_id)

    return DANUBE_LAYERS

if __name__ == '__console__':

    if DEV_OUTSIDE_PLUGIN:
        from dev_set_test import DANUBE_LAYERS
    else:
        pass

    DANUBE_LAYERS = main_dc_2(DANUBE_LAYERS)