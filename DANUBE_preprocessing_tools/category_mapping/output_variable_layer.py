import tempfile
import os

import processing
from qgis.core import Qgis, QgsMessageLog, QgsVectorLayer, QgsProject

from config_show import print_log, add_layer_gui, print_fields


def convert_df_to_layer(df):
    """Convert the df from the end of category mapping to a QgsVectorLayer"""

    # Save df to a csv file
    name = "BUILD_BASE_cm_import_csv"
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

    return layer_from_csv, csv_path


def join_csv_data_build_lay(csv_layer, DANUBE_LAYERS):
    """Join csv data (result of category mapping) to last version of BUILD_BASE """

    layer_joined_csv_data = processing.run("native:joinattributestable", {
        'INPUT': DANUBE_LAYERS['BUILD_BASE']['layer'],
        'FIELD': 'ID_BUILD',
        'INPUT_2': csv_layer,
        'FIELD_2': 'ID_BUILD',
        'FIELDS_TO_COPY': ['typology_danube', 'typology_source', 'typology_quality',
                           'dens_pers_m2build', 'dens_quantile',
                           'usage_danube', 'usage_source', 'usage_quality',
                           'year_constr', 'year_source', 'year_quality',
                           'period_danube', 'period_source', 'period_quality',
                           'location_dept', 'location_comm', 'location_source', 'location_quality',
                           'territory_dept', 'territory_comm', 'territory_source', 'territory_quality',
                           'arch_dept', 'arch_dept_id', 'arch_comm', 'arch_comm_id'],
        'METHOD': 1,
        'DISCARD_NONMATCHING': False,
        'PREFIX': '',
        'OUTPUT': 'TEMPORARY_OUTPUT'})['OUTPUT']

    print_log("type(layer_joined_csv_data): ", type(layer_joined_csv_data))
    add_layer_gui(layer_joined_csv_data, layer_name='BUILD_BASE_cm_after_join_cm_data')
    print_fields(layer_joined_csv_data)

    return layer_joined_csv_data


def get_output_layer(df, DANUBE_LAYERS):
    print_log("+" * 100)
    print_log("Run get_output_layer : Join results from category mapping to BUILD_BASE")
    print_log("+" * 100)

    print(df.columns)

    layer_from_csv, csv_path = convert_df_to_layer(df)

    output_layer = join_csv_data_build_lay(layer_from_csv, DANUBE_LAYERS)

    # os.unlink(csv_path) # csv file cannot be deleted, since it is used in the output_layer

    return output_layer
