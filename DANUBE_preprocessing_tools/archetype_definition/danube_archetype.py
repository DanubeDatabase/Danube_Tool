import tempfile
from pathlib import Path

import processing
from qgis.core import Qgis, QgsMessageLog, QgsVectorLayer, QgsProject

from config_show import print_log, add_layer_gui, print_fields
# from PyDANUBE.PyDANUBE import DANUBE_get_territory

def convert_df_layer(df):
    """Convert the df from the end of category mapping to a QgsVectorLayer"""

    # Save df to a csv file
    name = "BUILD_BASE_after_CM"
    f = tempfile.NamedTemporaryFile(delete=False, suffix='.csv', prefix=name + '_')
    csv_path = f.name
    df.to_csv(csv_path, index=False)
    print_log('\npath_to_save_csv: ', csv_path)

    # Read csv file as a QgsVectorLayer
    encoding = 'UTF-8'
    delimiter = ','
    crs = 'epsg:2154'
    uri = f'file:///{csv_path}?encoding={encoding}&delimiter={delimiter}&crs={crs}'
    layer_from_csv = QgsVectorLayer(uri, name, 'delimitedtext')

    # Check layer validity and add to QGIS GUI
    print_log("\nlayer_from_csv.isValid(): ", layer_from_csv.isValid())
    add_layer_gui(layer_from_csv)

    return layer_from_csv


def join_csv_data_build_lay(csv_layer, DANUBE_LAYERS):
    """Join csv data (result of category mapping) to last version of BUILD_BASE """

    layer_joined_csv_data = processing.run("native:joinattributestable", {
        'INPUT': DANUBE_LAYERS['BUILD_BASE']['layer'],
        'FIELD': 'ID_BUILD',
        'INPUT_2': csv_layer,
        'FIELD_2': 'ID_BUILD',
        'FIELDS_TO_COPY': ['typo_map', 'typo_source', 'typo_quality', 'dens_pop', 'dens_perc_order', 'usage_map',
                           'usage_source', 'usage_quality', 'year_map', 'year_source', 'year_quality', 'location_dept',
                           'location_city', 'location_source', 'location_quality'], 'METHOD': 1,
        'DISCARD_NONMATCHING': False,
        'PREFIX': 'cm_',
        'OUTPUT': 'TEMPORARY_OUTPUT'})['OUTPUT']

    print_log("type(layer_joined_csv_data): ", type(layer_joined_csv_data))
    add_layer_gui(layer_joined_csv_data, layer_name='BUILD_AFTER_DC_CM')
    print_fields(layer_joined_csv_data)

    return layer_joined_csv_data


# def associate_4_danube_vars_archetype(df):
def associate_4_danube_vars_archetype(layer_with_cm):
    # print_log('TODO - ASSOCIATE ARCHS ENTRIES in DF')
    # print("For now - df_archs = df -> need to add algo")
    # df_archs = df # to add operations !!!


    final_layer = layer_with_cm
    # final_layer = DANUBE_get_territory(layer_with_cm)

    # return df_archs
    return final_layer


def main_arch(df, DANUBE_LAYERS):
    print_log("+" * 100)
    print_log("Run archetype_definition : Archetype definition")
    print_log("+" * 100)

    print(df.columns)

    # df_archs = associate_4_danube_vars_archetype(df)
    # layer_joined_df = join_df_build_lay(df_archs, DANUBE_LAYERS)

    layer_from_csv = convert_df_layer(df)

    layer_joined_csv = join_csv_data_build_lay(layer_from_csv, DANUBE_LAYERS)

    final_layer = associate_4_danube_vars_archetype(layer_joined_csv)

    return layer_joined_csv
