from qgis.core import Qgis, QgsProject
from config_show import timed_execution, print_log

from data_consolidation.main import main_dc_data_consolidation
from category_mapping.main import main_cm_category_mapping
from archetype_processing.main import main_archetype_processing
from add_danube_layers.main import main_add_danube_layers


def main_process_all(DANUBE_LAYERS):
    print_log("#" * 100)
    print_log("--------------- START DANUBE PROCESSING -----------------")
    print_log("#" * 100)

    # -------- Run data consolidation - spatial operations
    DANUBE_LAYERS, df_output_dc = timed_execution(main_dc_data_consolidation, DANUBE_LAYERS)
    DANUBE_LAYERS['BUILD_BASE']['layer'].setName('BUILD_BASE')
    QgsProject.instance().addMapLayer(DANUBE_LAYERS['BUILD_BASE']['layer'])

    # -------- Run category mapping - data treatment of non spatial fields
    df_after_cm = timed_execution(main_cm_category_mapping, df_output_dc, DANUBE_LAYERS)

    # -------- Run archetype processing - provide danube archetypes
    # Define the location in which the territories are going to be taken into account
    df_with_arch, DANUBE_LAYERS = timed_execution(main_archetype_processing, df_after_cm, DANUBE_LAYERS)

    # -------- Run add danube layer - generate danube layers
    # Define the location in which the territories are going to be taken into account
    location = 'comm'
    DANUBE_LAYERS  = timed_execution(main_add_danube_layers, df_with_arch, DANUBE_LAYERS, location)

    # -------- add layers to the project
    show_preprocess = True
    show_danube_wall = True
    show_danube_roof = True
    show_danube_floor = True
    show_danube_window = True

    # add preprocess layer to project (which has all the information necessary to get to the archetypes)
    if show_preprocess:
        QgsProject.instance().addMapLayer(DANUBE_LAYERS['BUILD_PP_OUTPUT']['layer'])

    # wall layer - has information about danube walls
    if show_danube_wall:
        QgsProject.instance().addMapLayer(DANUBE_LAYERS['DANUBE_MUR']['layer'])

    # roof layer - has information about danube roofs
    if show_danube_roof:
        QgsProject.instance().addMapLayer(DANUBE_LAYERS['DANUBE_TOIT']['layer'])

    # wall floors - has information about danube floors
    if show_danube_floor:
        QgsProject.instance().addMapLayer(DANUBE_LAYERS['DANUBE_PLANCHER']['layer'])

    # wall windows - has information about danube windows
    if show_danube_window:
        QgsProject.instance().addMapLayer(DANUBE_LAYERS['DANUBE_VITRAGE']['layer'])


    print_log("#" * 100)
    print_log("--------------- END DANUBE PROCESSING -----------------")
    print_log("#" * 100)

    return DANUBE_LAYERS


def main_process_all_plugin(self, parameters, context, feedback):
    """Run the main from the plugin giving self.DANUBE_tool_LAYERS as DANUBE_LAYERS"""
    self.DANUBE_tool_LAYERS = timed_execution(main_process_all, self.DANUBE_tool_LAYERS)
