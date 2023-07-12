from config_show import timed_execution, print_log

from archetype_processing.map_archetype import main_archetype
from archetype_processing.preprocess_output_layer import get_preprocess_output_layer
from category_mapping.map_reference.shared_ref import PATH_DANUBE_TABLES_FOLDER


def main_archetype_processing(df, DANUBE_LAYERS):
    timed_execution(main_archetype, df, PATH_DANUBE_TABLES_FOLDER)

    output_layer = timed_execution(get_preprocess_output_layer, df, DANUBE_LAYERS)

    return output_layer
