from config_show import timed_execution, print_log

from category_mapping.map_reference.shared_ref import PATH_DANUBE_TABLES_FOLDER

from archetype_processing.existing_archetypes import main_existing_archetypes
from archetype_processing.archetype_generalization import main_archetype_generalization
from archetype_processing.arch_variables_layer import get_arch_output_layer


def main_archetype_processing(df, DANUBE_LAYERS):
    print_log("+" * 100)
    print_log("--------------- START ARCHETYPE PROCESSING -----------------")
    print_log("+" * 100)

    print_log("\nRun archetype processing considering {location} territories\n")

    # ---------- define archetypes
    timed_execution(main_existing_archetypes, df, PATH_DANUBE_TABLES_FOLDER)

    df = main_archetype_generalization(df)  # do not modify

    # ---------- provide layer with variables to define the archetype
    DANUBE_LAYERS['BUILD_PP_OUTPUT'] = {"id": "BUILD_PP_OUTPUT", "type": "OUTPUT", 'layer': None}
    DANUBE_LAYERS['BUILD_PP_OUTPUT']['layer'] = timed_execution(get_arch_output_layer, df, DANUBE_LAYERS)
    DANUBE_LAYERS['BUILD_PP_OUTPUT']['layer'].setName('BUILD_PP_OUTPUT')
    print_log('\nDANUBE_LAYERS.keys(): ', DANUBE_LAYERS.keys())


    print_log("+" * 100)
    print_log("--------------- END ARCHETYPE PROCESSING -----------------")
    print_log("+" * 100)

    return df, DANUBE_LAYERS
