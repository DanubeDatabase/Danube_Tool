import tempfile

import processing
from qgis.core import Qgis, QgsMessageLog, QgsVectorLayer, QgsProject, QgsVectorDataProvider

from config_show import print_log, print_fields


def convert_danube_df_to_layer(selected_df, prefix_name):
    """Convert the df from the end of category mapping to a QgsVectorLayer"""

    # Save df to a csv file
    f = tempfile.NamedTemporaryFile(delete=False, suffix='.csv', prefix=prefix_name + '_')
    csv_path = f.name
    selected_df.to_csv(csv_path, index=False)
    print_log('\npath_to_save_csv: ', csv_path)

    # Read csv file as a QgsVectorLayer
    encoding = 'UTF-8'
    delimiter = ','
    crs = 'epsg:2154'
    uri = f'file:///{csv_path}?encoding={encoding}&delimiter={delimiter}&crs={crs}'
    layer_from_csv = QgsVectorLayer(uri, prefix_name, 'delimitedtext')

    # Check layer validity and add to QGIS GUI
    print_log("\nlayer_from_csv.isValid(): ", layer_from_csv.isValid())

    return layer_from_csv, csv_path


def join_danube_layer_base(danube_layer, base_layer):
    """Join danube layer with base_layer"""
    print_log("\n Join danube layer with base_layer\n")

    layer_joined_csv_data = processing.run("native:joinattributestable", {
        'INPUT': base_layer,
        'FIELD': 'ID_BUILD',
        'INPUT_2': danube_layer,
        'FIELD_2': 'ID_BUILD',
        'FIELDS_TO_COPY': [],
        'METHOD': 1,
        'DISCARD_NONMATCHING': False,
        'PREFIX': '',
        'OUTPUT': 'TEMPORARY_OUTPUT'})['OUTPUT']
    print_log("danube layer fields before removing undesirable fields")
    print_fields(layer_joined_csv_data)

    caps = layer_joined_csv_data.dataProvider().capabilities()
    # remove the repeated fields : ID_BUILD_2, arch_{loc}_id,
    if caps & QgsVectorDataProvider.DeleteAttributes:
        idx_to_removed = [1, 3, 5]
        res = layer_joined_csv_data.dataProvider().deleteAttributes(idx_to_removed)
        layer_joined_csv_data.updateFields()

    print_log("danube layer fields after removing undesirable fields")
    print_fields(layer_joined_csv_data)

    return layer_joined_csv_data
