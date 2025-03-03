import processing

from config_show import print_log, print_fields, add_layer_gui
from data_consolidation.dc2_create_spatial_index import check_and_run_spatial_index


def filter_activ_fictive(DANUBE_LAYERS):
    """Take out fictive features from layer TOPO_ACTIVITE"""

    print_log("Before filter 'FICTIF', field values:")
    print_log(DANUBE_LAYERS['TOPO_ACTIVITE']['layer'].uniqueValues(
        DANUBE_LAYERS['TOPO_ACTIVITE']['layer'].fields().indexFromName('FICTIF')))

    result_filter_activ_fictif = processing.run("native:extractbyattribute",
                                                {'INPUT': DANUBE_LAYERS['TOPO_ACTIVITE']['layer'],
                                                 'FIELD': 'FICTIF',
                                                 'OPERATOR': 6,  # operator - begins with
                                                 'VALUE': 'N',  # only keep the 'Non' fictive features
                                                 'OUTPUT': 'TEMPORARY_OUTPUT'})

    DANUBE_LAYERS['TOPO_ACTIVITE']['layer'] = result_filter_activ_fictif['OUTPUT']
    add_layer_gui(DANUBE_LAYERS['TOPO_ACTIVITE']['layer'], layer_name="TOPO_ACTIVITE_dc4_after_filter")

    check_and_run_spatial_index(DANUBE_LAYERS['TOPO_ACTIVITE']['id'], DANUBE_LAYERS['TOPO_ACTIVITE']['layer'])

    print_log("After filter 'FICTIF', field values:")
    print_log(DANUBE_LAYERS['TOPO_ACTIVITE']['layer'].uniqueValues(
        DANUBE_LAYERS['TOPO_ACTIVITE']['layer'].fields().indexFromName('FICTIF')))


def join_topo_activ(DANUBE_LAYERS):
    """join relevant features of TOPO_ACTIVITE to BUILD_BASE by major intersection area"""

    print_log("\nBUILD_BASE fields before join with TOPO_ACTIVITE")
    print_fields(DANUBE_LAYERS['BUILD_BASE']['layer'])

    result_join_build_activ = processing.run("native:joinattributesbylocation",
                                             {'INPUT': DANUBE_LAYERS['BUILD_BASE']['layer'],
                                              'JOIN': DANUBE_LAYERS['TOPO_ACTIVITE']['layer'],
                                              'PREDICATE': [0],  # intersect
                                              'JOIN_FIELDS': ['CATEGORIE', 'NATURE'],
                                              'METHOD': 2,  # select just the feature with the largest matching area
                                              'DISCARD_NONMATCHING': False,
                                              'PREFIX': 'activ_',
                                              'OUTPUT': 'TEMPORARY_OUTPUT'})
    DANUBE_LAYERS['BUILD_BASE']['layer'] = result_join_build_activ['OUTPUT']

    check_and_run_spatial_index(DANUBE_LAYERS['BUILD_BASE']['id'], DANUBE_LAYERS['BUILD_BASE']['layer'])

    print_log("BUILD_BASE fields after join with TOPO_ACTIVITE")
    print_fields(DANUBE_LAYERS['BUILD_BASE']['layer'])
    add_layer_gui(DANUBE_LAYERS['BUILD_BASE']['layer'], 'BUILD_BASE_dc4_joined_topo_activ')


def main_topo_activ(DANUBE_LAYERS):
    """Perform spatial operations"""
    print_log("*" * 100)
    print_log("Run step 4 of data consolidation : Spatially join TOPO_ACTIVITE to the building layer")
    print_log("*" * 100)

    filter_activ_fictive(DANUBE_LAYERS)
    join_topo_activ(DANUBE_LAYERS)

    return DANUBE_LAYERS