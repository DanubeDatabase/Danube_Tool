import time
import os
from pathlib import Path
from qgis.core import QgsVectorLayer, QgsProject

# ___________________Define variables of test and debug to run the workflow___________________


DEV_OUT_PLUGIN = False  # if True, DANUBE_LAYERS is defined from local samples
# if False, if True, DANUBE_LAYERS is defined from the DANUBE_config file in the plugin

SMALL_SAMPLE = True  # if True, it uses local small samples of data to test the workflow;
# if False, it uses local data from Haute-Garonne and Toulouse to test the workflow.

DEBUG_PRINT = True  # if True, print in the console steps of the process

SHOW_GUI_LAY = True  # if True add intermediate layers to QGIS GUI to check

TIME_MEMORY = False  # import module (to be installed first) which allows showing memory use


# ___________________Functions in developing and debug mode___________________


def print_d(*args, **kwargs):
    """Print if the 'debug_print' variable is True"""
    if DEBUG_PRINT:
        print(*args, **kwargs)


def print_fields_d(layer):
    """Print the fields of a layer if the 'debug_print' variable is True"""
    print_d(f"\n{layer.name()}:\n", layer.fields().names())


def timed_execution_d(func, *args, **kwargs):
    """Run a function and print its execution time if the 'debug_print' variable is True"""
    start = time.time()
    result = func(*args, **kwargs)
    end = time.time()
    total_time = end - start
    print_d("_" * 25)
    print_d(f"\n{func.__name__} \nexecution time \n{total_time:.2f} sec or {total_time / 60:.2f} min")
    print_d("_" * 25)
    return result


if TIME_MEMORY:
    import psutil
def print_memory_use():
    """Print memory use if the 'time_memory' variable is True"""
    if TIME_MEMORY:
        print('psutil RAM memory % used:', psutil.virtual_memory()[2])
        print('psutil RAM Used (GB):', psutil.virtual_memory()[3] / 1000000000)
    else:
        pass


def add_layer_gui(layer, layer_name=None):
    """Add the layer to the QGIS GUI if the 'SHOW_GUI_LAY' variable is True"""
    if SHOW_GUI_LAY:
        # add layer to open project in QGIS
        if layer_name:
            layer.setName(layer_name)
        QgsProject.instance().addMapLayer(layer)


# ___________________Open layers functions___________________

def check_validity(layer):
    """Check if the layer is valid"""
    if layer.isValid():
        print_d(f"\nLayer '{layer.name()}' is valid. \n")
        # Perform the required operations on the layer
        layer.startEditing()  # Start editing the layer
        layer.triggerRepaint()  # Refresh the layer to show changes
        layer.commitChanges()  # Save the changes to the layer
    else:
        print_d(f"\nLayer '{layer.name()}' is NOT valid!\n")


def open_layer(layer_path_or_name):
    """ Get the layer by its name or ID"""

    if type(layer_path_or_name) is str:
        if Path(layer_path_or_name).is_file():
            layer = QgsVectorLayer(layer_path_or_name, Path(layer_path_or_name).stem, 'ogr')  # open layer from path
            check_validity(layer)
            return layer

        else:
            if layer_path_or_name in [vectl.name() for vectl in
                                      list(QgsProject.instance().mapLayers().values())]:  # test if the layer_path_or_name is an open layer
                layer = QgsProject.instance().mapLayersByName(layer_path_or_name)[
                    0]  # Retrieves the first open layer with the given name
                check_validity(layer)
                return layer

            else:
                print_d('name layer not recognized')
    else:
        print_d('Please enter a string type')


# _________________Set layers to run the workflow_____________________


def open_local_data_sample(small_sample):
    """Define DANUBE_LAYERS for test
     if 'small_sample' is False, adjust the following paths in a different computer:
        - geoclimate_folder
         -bdtopo_folder
         -path_filosofi """

    print_memory_use()

    print("_" * 100)
    print("Open input layers for testing")
    print("_" * 100)

    if small_sample:
        # preprocess_folder = Path(r"C:\Users\lorena.carvalho\Documents\Develop_outil\data\\outil_danube_dev_test_data")
        preprocess_folder = Path(os.path.dirname(os.path.realpath(__file__)))
        sample_data_folder = preprocess_folder / 'sample_data_to_test'
        print_d("preprocess_folder", sample_data_folder)
        DANUBE_LAYERS = {
            "TOPO_BATI": {"id": "TOPO_BATI", "type": "INPUT", "layer": open_layer(str(sample_data_folder / "s_topo_bati.gpkg"))},
            "TOPO_ACTIVITE": {"id": "TOPO_ACTIVITE", "type": "INPUT",
                              "layer": open_layer(str(sample_data_folder / "s_topo_activite.gpkg"))},
            "GEO_RSU_UTRF_FLOOR_AREA": {"id": "GEO_RSU_UTRF_FLOOR_AREA", "type": "INPUT",
                                        "layer": open_layer(str(sample_data_folder / "s_geo_rsu.gpkg"))},
            "GEO_BUILD_URTF": {"id": "GEO_BUILD_URTF", "type": "INPUT",
                               "layer": open_layer(str(sample_data_folder / "s_geo_build_utrf.gpkg"))},
            "GEO_ZONE": {"id": "GEO_ZONE", "type": "INPUT", "layer": open_layer(str(sample_data_folder / "s_geo_zone.gpkg"))},
            "GEO_BUILD_IND": {"id": "GEO_BUILD_IND", "type": "INPUT",
                              "layer": open_layer(str(sample_data_folder / "s_geo_build_ind.gpkg"))},
            "FILOSOFI": {"id": "FILOSOFI", "type": "INPUT", "layer": open_layer(str(sample_data_folder / "s_filosofi.gpkg"))},
            "DANUBE_BUILD_PREPROCESS": {"id": "DANUBE_BUILD_PREPROCESS", "type": "OUTPUT", "layer": None},
            "DANUBE_BUILD_DATA": {"id": "DANUBE_BUILD_DATA", "type": "OUTPUT", "layer": None},
        }
    else:
        geoclimate_folder = Path(
            r"C:\Users\lorena.carvalho\Documents\Develop_outil\data\Haute_Garonne\Geoclimate\Geoclimate-bdtopo_v3_Toulouse_31555_20042023")
        bdtopo_folder = Path(
            r"C:\Users\lorena.carvalho\Documents\Develop_outil\data\Haute_Garonne\BDTOPO\V3\BDTOPO_3-0_TOUSTHEMES_SHP_LAMB93_D031_2022-03-15\BDTOPO\1_DONNEES_LIVRAISON_2022-03-00081\BDT_3-0_SHP_LAMB93_D031-ED2022-03-15")
        path_filosofi = r"C:\Users\lorena.carvalho\Documents\Develop_outil\data\Filosofi\Filosofi2017_carreaux_nivNaturel_met.shp"
        DANUBE_LAYERS = {
            "TOPO_BATI": {"id": "TOPO_BATI", "type": "INPUT",
                          "layer": open_layer(str(bdtopo_folder / "BATI" / "BATIMENT.shp"))},
            "TOPO_ACTIVITE": {"id": "TOPO_ACTIVITE", "type": "INPUT", "layer": open_layer(
                str(bdtopo_folder / "SERVICES_ET_ACTIVITES" / "ZONE_D_ACTIVITE_OU_D_INTERET.shp"))},
            "GEO_RSU_UTRF_FLOOR_AREA": {"id": "GEO_RSU_UTRF_FLOOR_AREA", "type": "INPUT",
                                        "layer": open_layer(str(geoclimate_folder / "rsu_utrf_floor_area.geojson"))},
            "GEO_BUILD_URTF": {"id": "GEO_BUILD_URTF", "type": "INPUT",
                               "layer": open_layer(str(geoclimate_folder / "building_utrf.geojson"))},
            "GEO_ZONE": {"id": "GEO_ZONE", "type": "INPUT",
                         "layer": open_layer(str(geoclimate_folder / "zone.geojson"))},
            "GEO_BUILD_IND": {"id": "GEO_BUILD_IND", "type": "INPUT",
                              "layer": open_layer(str(geoclimate_folder / "building_indicators.geojson"))},
            "FILOSOFI": {"id": "FILOSOFI", "type": "INPUT", "layer": open_layer(path_filosofi)},
            "DANUBE_BUILD_PREPROCESS": {"id": "DANUBE_BUILD_PREPROCESS", "type": "OUTPUT", "layer": None},
            "DANUBE_BUILD_DATA": {"id": "DANUBE_BUILD_DATA", "type": "OUTPUT", "layer": None},
        }

    print_memory_use()

    return DANUBE_LAYERS

def define_danube_layer_source():
    if DEV_OUT_PLUGIN:
        DANUBE_LAYERS = timed_execution_d(open_local_data_sample, SMALL_SAMPLE)
    else:
        from DANUBE_config import DANUBE_LAYERS
    return DANUBE_LAYERS

DANUBE_LAYERS = define_danube_layer_source()

if __name__ == '__console__':
    def test_open_layer():
        folder = Path(r"C:\Users\lorena.carvalho\Documents\Develop_outil\data\outil_danube_dev_test_data")
        path_or_layer = str(folder / "small_bati.gpkg")
        layer_names = [layer.name() for layer in QgsProject.instance().mapLayers().values()]
        layer_from_path = open_layer(path_or_layer)
        print("open_layer from path is working!")
        print(layer_from_path.fields().names())

        if len(layer_names) > 0:
            layer_name = layer_names[0]
            layer_from_name = open_layer(layer_name)
            print("open_layer from layer name is working!")
            print(layer_from_name.fields().names())
        else:
            print('No layers are presently open in QGIS. Open a layer in the GIU to test this function')

    printd("That ", "is ", "a ", "test!")
    test_open_layer()

    # def copy_layer(source_layer):
    #     source_layer.selectAll()
    #     layer_copy = processing.run("native:saveselectedfeatures", {'INPUT': source_layer, 'OUTPUT': 'memory:'})['OUTPUT']
    #     source_layer.removeSelection()
    #     name_layer_copy = f"{source_layer.name()}_copy"
    #     layer_copy.setName(name_layer_copy) # comment later, just for test
    #     QgsProject.instance().addMapLayer(layer_copy) # comment later, just for test
    #     return layer_copy
