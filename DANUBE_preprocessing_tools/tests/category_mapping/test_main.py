from pathlib import Path
import pandas as pd

from tests.paths import SAMPLE_DATA_PATH
from tests.test_main_preprocess import SMALL_SAMPLE
from config_show import timed_execution

from category_mapping.main import main_cm_category_mapping


def define_sample_cat_map(small_sample):
    if small_sample:
        csv_file = "31555_DANUBE_BUILD_PREPROCESS_s.csv"
    else:
        csv_file = "31555_DANUBE_BUILD_PREPROCESS_Toulouse.csv"

    # city_id = csv_file.split('_')[0]

    csv_path = SAMPLE_DATA_PATH / "category_mapping_sample" / csv_file

    return pd.read_csv(csv_path)


if __name__ == '__console__':
    print("RUNNING TEST CATEGORY MAPPING")
    print_log("_" * 100)
    print_log("Open output from data consolidation for testing")
    print_log("_" * 100)

    df_output_dc = define_sample_cat_map(SMALL_SAMPLE)
    df_output_cm = timed_execution(main_cm_category_mapping, df_output_dc)


