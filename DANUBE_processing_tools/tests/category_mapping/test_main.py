from pathlib import Path
import pandas as pd

from tests.paths import SAMPLE_DATA_PATH
from tests.test_main_process import SMALL_SAMPLE
from config_show import timed_execution, print_log, open_layer

from category_mapping.main import main_cm_category_mapping

def define_local_danube_layer_just_geozone(small_sample):
    if small_sample:
        sample_data_folder = SAMPLE_DATA_PATH / "data_consolidation_sample"
        DANUBE_LAYERS = {
            "GEO_ZONE": {"id": "GEO_ZONE", "type": "INPUT",
                         "layer": open_layer(str(sample_data_folder / "s_geo_zone.gpkg"))},
        }
    else:
        geoclimate_folder = Path(
            r"C:\Users\lorena.carvalho\Documents\Develop_outil\data\Haute_Garonne\Geoclimate\Geoclimate-bdtopo_v3_Toulouse_31555_20042023")
        DANUBE_LAYERS = {
            "GEO_ZONE": {"id": "GEO_ZONE", "type": "INPUT",
                         "layer": open_layer(str(geoclimate_folder / "zone.geojson"))},
        }
    return DANUBE_LAYERS


def define_sample_cat_map(small_sample):
    if small_sample:
        csv_file = "31555_BUILD_BASE_s.csv"
    else:
        csv_file = "31555_BUILD_BASE_Toulouse.csv"

    csv_path = SAMPLE_DATA_PATH / "category_mapping_sample" / csv_file

    return pd.read_csv(csv_path)


if __name__ == '__console__':
    print("RUNNING TEST CATEGORY MAPPING")
    print_log("_" * 100)
    print_log("Open output from data consolidation for testing")
    print_log("_" * 100)

    DANUBE_LAYERS = define_local_danube_layer_just_geozone(SMALL_SAMPLE)
    df_output_dc = define_sample_cat_map(SMALL_SAMPLE)
    df_output_cm = timed_execution(main_cm_category_mapping, df_output_dc, DANUBE_LAYERS)


