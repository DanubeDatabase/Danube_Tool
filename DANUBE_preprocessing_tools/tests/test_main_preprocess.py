from pathlib import Path
# import os

from config_show import print_log, open_layer, print_memory_use, timed_execution
from main_preprocess import main_preprocess_all
from tests.paths import SAMPLE_DATA_PATH

# _________________Set test workflow_____________________

SMALL_SAMPLE = True  # if True, it uses local small samples of data to test the workflow;
# if False, it uses local data from Haute-Garonne and Toulouse to test the workflow.



def open_local_data_sample(small_sample):
    """Define DANUBE_LAYERS for test
     Adjust the following paths in a different computer:
         -preprocess_folder
         - geoclimate_folder
         -bdtopo_folder
         -path_filosofi """

    print_memory_use()

    print_log("_" * 100)
    print_log("Open input layers for testing")
    print_log("_" * 100)

    if small_sample:
        sample_data_folder = SAMPLE_DATA_PATH / "data_consolidation_sample"
        print_log("preprocess_folder", sample_data_folder)
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


if __name__ == '__console__':
    DANUBE_LAYERS = timed_execution(open_local_data_sample, SMALL_SAMPLE)
    timed_execution(main_preprocess_all,DANUBE_LAYERS)







#________________________________________funcs to keep in case______________________________________________
    # if DANUBE_LAYERS["GEO_BUILD_URTF"]["layer"].isValid():
    #     QgsMessageLog.logMessage(
    #         ' In main_dc_data_consolidation() BEFORE -  DANUBE_LAYERS.[GEO_BUILD_URTF].source (valid):' + str(DANUBE_LAYERS["GEO_BUILD_URTF"]["layer"].source()) + "\n",
    #         'DANUBE tool', level=Qgis.Info)
    # else:
    #     QgsMessageLog.logMessage(
    #         ' In main_dc_data_consolidation() BEFORE - NOT VALID LAYER!!!!',
    #         'DANUBE tool', level=Qgis.Info)

    # def copy_layer(source_layer):
    #     source_layer.selectAll()
    #     layer_copy = processing.run("native:saveselectedfeatures", {'INPUT': source_layer, 'OUTPUT': 'memory:'})['OUTPUT']
    #     source_layer.removeSelection()
    #     name_layer_copy = f"{source_layer.name()}_copy"
    #     layer_copy.setName(name_layer_copy) # comment later, just for test
    #     QgsProject.instance().addMapLayer(layer_copy) # comment later, just for test
    #     return layer_copy