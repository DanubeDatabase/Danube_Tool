from dev_set_test import DANUBE_LAYERS, timed_execution_d

from data_consolidation.main_data_consolidation import main_dc_data_consolidation
from category_mapping.main_category_mapping import main_cm_category_mapping
from archetype_definition.danube_archetype import main_arch


def main_preprocess_all(DANUBE_LAYERS):
    print("#" * 100)
    print("--------------- START DANUBE PREPROCESSING -----------------")
    print("#" * 100)

    timed_execution_d(main_dc_data_consolidation,DANUBE_LAYERS)
    timed_execution_d(main_cm_category_mapping)
    timed_execution_d(main_arch)

    print("#" * 100)
    print("--------------- END DANUBE PREPROCESSING -----------------")
    print("#" * 100)

def main_preprocess_all_plugin(self, parameters, context, feedback):
	main_preprocess_all(self.DANUBE_tool_LAYERS)

    
if __name__ == '__console__':
    main_preprocess_all(DANUBE_LAYERS)
