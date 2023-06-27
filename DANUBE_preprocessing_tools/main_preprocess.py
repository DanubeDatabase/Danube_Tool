from config_show import timed_execution, print_log

from data_consolidation.main_data_consolidation import main_dc_data_consolidation
from category_mapping.main_category_mapping import main_cm_category_mapping
from archetype_definition.danube_archetype import main_arch


def main_preprocess_all(DANUBE_LAYERS):
    print_log("#" * 100)
    print_log("--------------- START DANUBE PREPROCESSING -----------------")
    print_log("#" * 100)

    DANUBE_LAYERS = timed_execution(main_dc_data_consolidation, DANUBE_LAYERS)
    timed_execution(main_cm_category_mapping, DANUBE_LAYERS)
    timed_execution(main_arch)

    print_log("#" * 100)
    print_log("--------------- END DANUBE PREPROCESSING -----------------")
    print_log("#" * 100)


def main_preprocess_all_plugin(self, parameters, context, feedback):
    """Run the main from the plugin giving self.DANUBE_tool_LAYERS as DANUBE_LAYERS"""
    timed_execution(main_preprocess_all, self.DANUBE_tool_LAYERS)


if __name__ == '__console__':
    main_preprocess_all(DANUBE_LAYERS)
