import tempfile
import os
from pathlib import Path

import pandas as pd

import processing

from config_show import print_log

def save_output_to_csv(DANUBE_LAYERS):
    file_prefix = "BUILD_BASE_before_CM_"

    result_save_csv = processing.run("native:savefeatures", {'INPUT': DANUBE_LAYERS['BUILD_BASE']['layer'],
                                                             'OUTPUT': tempfile.NamedTemporaryFile(delete=False,
                                                                                                   prefix=file_prefix,
                                                                                                   suffix='.csv').name,
                                                             'LAYER_NAME': file_prefix,
                                                             'DATASOURCE_OPTIONS': '',
                                                             'LAYER_OPTIONS': ''})

    print_log('result_save_csv["FILE_PATH"]: ', result_save_csv["FILE_PATH"], "\n")
    print_log('result_save_csv["LAYER_NAME"]: ', result_save_csv["LAYER_NAME"], "\n")

    return result_save_csv["FILE_PATH"]


def main_dc6_convert_to_df(DANUBE_LAYERS):
    """"convert BUILD_BASE to DataFrame and add city dept info"""
    print_log("*" * 100)
    print_log("Run step 6 of data consolidation : convert BUILD_BASE to DataFrame and add city dept info")
    print_log("*" * 100)

    csv_path = save_output_to_csv(DANUBE_LAYERS)
    df = pd.read_csv(csv_path)

    os.unlink(csv_path)

    print_log('df.head(): ', df.head(), "\n")


    return DANUBE_LAYERS, df
