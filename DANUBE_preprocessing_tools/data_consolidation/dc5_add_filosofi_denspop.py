import processing
# from qgis.core import QgsProcessing

from config_show import print_log, print_fields, add_layer_gui


def join_filo(DANUBE_LAYERS):
    """join FILOSOFI to BUILD_BASE - by major intersection area"""
    result_join_build_filo = processing.run("native:joinattributesbylocation",
                                            {'INPUT': DANUBE_LAYERS['BUILD_BASE']['layer'],
                                             'JOIN': DANUBE_LAYERS['FILOSOFI']['layer'],
                                             'PREDICATE': [0],  # intersect
                                             'JOIN_FIELDS': ['Idcar_nat',
                                                             'Ind', 'Men',
                                                             'Log_av45', 'Log_45_70', 'Log_70_90', 'Log_ap90',
                                                             'Log_inc'],
                                             'METHOD': 2,  # select just the feature with the largest matching area
                                             'DISCARD_NONMATCHING': False,
                                             'PREFIX': 'filo_',
                                             'OUTPUT': 'TEMPORARY_OUTPUT'})
    DANUBE_LAYERS['BUILD_BASE']['layer'] = result_join_build_filo['OUTPUT']


def add_filo_dens_pop(DANUBE_LAYERS):
    print_log("*" * 100)
    print_log(
        "Run step 5 of data consolidation : Spatially join FILOSOFI to the building layer and calculate populational density")
    print_log("*" * 100)

    join_filo(DANUBE_LAYERS)

    print_log("BUILD_BASE fields after join with FILOSOFI")
    print_fields(DANUBE_LAYERS['BUILD_BASE']['layer'])
    add_layer_gui(DANUBE_LAYERS['BUILD_BASE']['layer'], 'BUILD_BASE_dc5_joined_filosofi')

    return DANUBE_LAYERS
