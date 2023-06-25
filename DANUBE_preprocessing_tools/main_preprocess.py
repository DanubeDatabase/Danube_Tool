from dev_set_test import timed_execution_d

from data_consolidation.main_data_consolidation import main_dc_data_consolidation
from category_mapping.main_category_mapping import main_cm_category_mapping
from archetype_definition.danube_archetype import main_arch


if __name__ == '__console__':
    print("#" * 100)
    print("--------------- START DANUBE PREPROCESSING -----------------")
    print("#" * 100)

    timed_execution_d(main_dc_data_consolidation)
    timed_execution_d(main_cm_category_mapping)
    timed_execution_d(main_arch)

    print("#" * 100)
    print("--------------- END DANUBE PREPROCESSING -----------------")
    print("#" * 100)