from config_show import timed_execution, print_log

from data_consolidation.main import main_dc_data_consolidation
from category_mapping.main import main_cm_category_mapping
from category_mapping.output_variable_layer import get_output_layer


def main_preprocess_all(DANUBE_LAYERS):
    print_log("#" * 100)
    print_log("--------------- START DANUBE PREPROCESSING -----------------")
    print_log("#" * 100)

    DANUBE_LAYERS, df_output_dc = timed_execution(main_dc_data_consolidation, DANUBE_LAYERS)

    DANUBE_LAYERS['BUILD_PP_OUTPUT'] = {"id":None, "type":None,'layer':None }
    DANUBE_LAYERS['BUILD_PP_OUTPUT']['layer']  = timed_execution(main_cm_category_mapping, df_output_dc, DANUBE_LAYERS)
    print_log('\nDANUBE_LAYERS.keys(): ', DANUBE_LAYERS.keys())


    print_log("#" * 100)
    print_log("--------------- END DANUBE PREPROCESSING -----------------")
    print_log("#" * 100)

    return DANUBE_LAYERS


def main_preprocess_all_plugin(self, parameters, context, feedback):
    """Run the main from the plugin giving self.DANUBE_tool_LAYERS as DANUBE_LAYERS"""
    self.DANUBE_tool_LAYERS = timed_execution(main_preprocess_all, self.DANUBE_tool_LAYERS)
