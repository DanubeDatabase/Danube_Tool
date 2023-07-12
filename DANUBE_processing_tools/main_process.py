from qgis.core import Qgis, QgsProject
from config_show import timed_execution, print_log

from data_consolidation.main import main_dc_data_consolidation
from category_mapping.main import main_cm_category_mapping
from archetype_processing.main import main_archetype_processing


def main_process_all(DANUBE_LAYERS):
    print_log("#" * 100)
    print_log("--------------- START DANUBE PROCESSING -----------------")
    print_log("#" * 100)

    # Run data consolidation - spatial operations
    DANUBE_LAYERS, df_output_dc = timed_execution(main_dc_data_consolidation, DANUBE_LAYERS)
    DANUBE_LAYERS['BUILD_BASE']['layer'].setName('BUILD_BASE')
    QgsProject.instance().addMapLayer(DANUBE_LAYERS['BUILD_BASE']['layer'])

    df_after_cm = timed_execution(main_cm_category_mapping, df_output_dc, DANUBE_LAYERS)


    DANUBE_LAYERS  = timed_execution(main_archetype_processing, df_after_cm, DANUBE_LAYERS)

    DANUBE_LAYERS['BUILD_PP_OUTPUT']['layer'].setName('BUILD_PP_OUTPUT')
    QgsProject.instance().addMapLayer(DANUBE_LAYERS['BUILD_PP_OUTPUT']['layer'])

    print_log("#" * 100)
    print_log("--------------- END DANUBE PROCESSING -----------------")
    print_log("#" * 100)

    return DANUBE_LAYERS


def main_process_all_plugin(self, parameters, context, feedback):
    """Run the main from the plugin giving self.DANUBE_tool_LAYERS as DANUBE_LAYERS"""
    self.DANUBE_tool_LAYERS = timed_execution(main_process_all, self.DANUBE_tool_LAYERS)
