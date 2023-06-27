import processing

from dev_set_test import print_d, print_fields_d, add_layer_gui


def join_topo_activite(DANUBE_LAYERS):
    """Join relevant features of TOPO_ACTIVITE into DANUBE_BUILD_PREPROCESS"""

    def filter_activ_fictive():
        """Take out fictive features from layer TOPO_ACTIVITE"""

        result_filter_activ_fictif = processing.run("native:extractbyattribute",
                                    {'INPUT': DANUBE_LAYERS['TOPO_ACTIVITE']['layer'],
                                    'FIELD': 'FICTIF',
                                    'OPERATOR': 6, # operator - begins with
                                    'VALUE': 'N', # only keep the 'Non' fictive features
                                    'OUTPUT': 'TEMPORARY_OUTPUT'})

        DANUBE_LAYERS['TOPO_ACTIVITE']['layer'] = result_filter_activ_fictif['OUTPUT']
        add_layer_gui(DANUBE_LAYERS['TOPO_ACTIVITE']['layer'] , layer_name="TOPO_ACTIVITE_dc4_after_filter" )

    def join_activ():
        """join TOPO_ACTIVITE to DANUBE_BUILD_PREPROCESS - by major intersection area"""
        result_join_build_activ = processing.run("native:joinattributesbylocation",
                                {'INPUT':DANUBE_LAYERS['DANUBE_BUILD_PREPROCESS']['layer'],
                                'JOIN': DANUBE_LAYERS['TOPO_ACTIVITE']['layer'],
                                'PREDICATE':[0], # intersect
                                'JOIN_FIELDS':['CATEGORIE','NATURE'],
                                'METHOD':2, # select just the feature with the largest matching area
                                'DISCARD_NONMATCHING': False,
                                'PREFIX':'activ_',
                                'OUTPUT':'TEMPORARY_OUTPUT'})
        DANUBE_LAYERS['DANUBE_BUILD_PREPROCESS']['layer'] = result_join_build_activ['OUTPUT']

    # run functions above
    filter_activ_fictive()
    join_activ()



def main_topo_activ(DANUBE_LAYERS):
    """Perform spatial operations"""
    print("*" * 100)
    print("Run step 4 of data consolidation : Spatially join TOPO_ACTIVITE and FILOSOFI to the building layer")
    print("*" * 100)

    print_d("Before filter 'FICTIF', field values:")
    print_d(DANUBE_LAYERS['TOPO_ACTIVITE']['layer'].uniqueValues(
        DANUBE_LAYERS['TOPO_ACTIVITE']['layer'].fields().indexFromName('FICTIF')))

    print_d("\nDANUBE_BUILD_PREPROCESS fields before join with TOPO_ACTIVITE")
    print_fields_d(DANUBE_LAYERS['DANUBE_BUILD_PREPROCESS']['layer'])

    #  run function
    join_topo_activite(DANUBE_LAYERS)

    print_d("After filter 'FICTIF', field values:")
    print_d(DANUBE_LAYERS['TOPO_ACTIVITE']['layer'].uniqueValues(
        DANUBE_LAYERS['TOPO_ACTIVITE']['layer'].fields().indexFromName('FICTIF')))

    print_d("DANUBE_BUILD_PREPROCESS fields after join with TOPO_ACTIVITE")
    print_fields_d(DANUBE_LAYERS['DANUBE_BUILD_PREPROCESS']['layer'])
    add_layer_gui(DANUBE_LAYERS['DANUBE_BUILD_PREPROCESS']['layer'], 'DANUBE_BUILD_PREPROCESS_dc4_joined_topo_activ')

    return DANUBE_LAYERS


