import processing
from qgis.core import Qgis, QgsMessageLog, QgsVectorLayer, QgsProject, QgsVectorDataProvider

from config_show import print_log, add_layer_gui, print_fields


def copy_layer(source_layer, name_layer):
    source_layer.selectAll()
    layer_copy = processing.run("native:saveselectedfeatures", {'INPUT': source_layer, 'OUTPUT': 'memory:'})['OUTPUT']
    source_layer.removeSelection()
    name_layer_copy = name_layer
    layer_copy.setName(name_layer_copy)  # comment later, just for test
    return layer_copy


def provide_geometry_for_danube_layers(DANUBE_LAYERS):
    print_log("*" * 100)
    print_log("Run step 1 add danube layers : provide_geometry_for_danube_layers - "
              "provide a QGIS layer with only the field ID_BUILD and the geometry")
    print_log("*" * 100)

    base_layer = copy_layer(DANUBE_LAYERS['GEO_BUILD_URTF']['layer'], 'BASE_LAYER')

    add_layer_gui(base_layer, 'base_layer_before')
    print_fields(base_layer)

    caps = base_layer.dataProvider().capabilities()
    # keep just the ID_BUILD to allow join df attributes
    if caps & QgsVectorDataProvider.DeleteAttributes:
        f_names = [field.name() for field in base_layer.fields()]
        f_idx = [base_layer.fields().indexFromName(field_name) for field_name in f_names]
        dict_field_idx = dict(zip(f_names, f_idx))
        dict_field_idx.pop('ID_BUILD')
        idx_to_removed = list(dict_field_idx.values())
        res = base_layer.dataProvider().deleteAttributes(idx_to_removed)
        base_layer.updateFields()

    add_layer_gui(base_layer, 'base_layer_after')
    print_fields(base_layer)

    return base_layer
