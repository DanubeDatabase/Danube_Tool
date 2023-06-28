import os
from pathlib import Path

import pandas as pd

import processing

from config_show import print_log

OUTPUT_FOLDER = Path(__file__).parent / "output"


def save_output_to_csv(DANUBE_LAYERS, city_id):
    csv_file_name = f"{city_id}_DANUBE_BUILD_PREPROCESS.csv"
    csv_path = str(OUTPUT_FOLDER / csv_file_name)
    result_save_csv = processing.run("native:savefeatures", {'INPUT': DANUBE_LAYERS['DANUBE_BUILD_PREPROCESS']['layer'],
                                                             'OUTPUT': csv_path,
                                                             'LAYER_NAME': csv_file_name,
                                                             'DATASOURCE_OPTIONS': '',
                                                             'LAYER_OPTIONS': ''})

    print_log('result_save_csv["FILE_PATH"]: ', result_save_csv["FILE_PATH"], "\n")
    print_log('result_save_csv["LAYER_NAME"]: ', result_save_csv["LAYER_NAME"], "\n")

    return result_save_csv["FILE_PATH"]


def main_dc6_convert_to_df(DANUBE_LAYERS):
    """"convert DANUBE_BUILD_PREPROCESS to DataFrame and add city dept info"""
    print_log("*" * 100)
    print_log("Run step 6 of data consolidation : convert DANUBE_BUILD_PREPROCESS to DataFrame and add city dept info")
    print_log("*" * 100)

    city_id = [feature['ID_ZONE'] for feature in DANUBE_LAYERS['GEO_ZONE']['layer'].getFeatures()][0]
    print_log('_' * 21, 'city_id', '_' * 21, '\n')
    print_log(city_id)

    csv_path = save_output_to_csv(DANUBE_LAYERS, city_id)
    df = pd.read_csv(csv_path)
    print_log('df.head(): ', df.head(), "\n")

    df["dept_id"] = city_id[:2]
    df["city_id"] = city_id
    print_log('df.head(): ', df.head(), "\n")

    return df
