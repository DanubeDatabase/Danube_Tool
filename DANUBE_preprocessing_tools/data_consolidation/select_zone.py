import processing

from dev_set_test import DEV_TEST, add_layer_gui, print_d


def main_dc_3(DANUBE_LAYERS):
    """Select the studied zone from 'TOPO_ACTIVITE' and 'FILOSOFI' layers to optimize the further spatial joins """
    print("*" * 100)
    print("Run step 3 of data consolidation : reduce size of data to the perimeters of the GEO_ZONE")
    print("*" * 100)

    # create spatial index to the layers which will be further used
    to_reduce = ['TOPO_ACTIVITE', 'FILOSOFI']
    for lay_name in to_reduce:
        print_d(lay_name)
        add_layer_gui(DANUBE_LAYERS[lay_name]['layer'], lay_name + '_before_zone_selection')

        output_extracted = processing.run("native:extractbylocation",
                                          {'INPUT': DANUBE_LAYERS[lay_name]['layer'],
                                           'PREDICATE': [0],
                                           'INTERSECT': DANUBE_LAYERS['GEO_ZONE']['layer'],
                                           'OUTPUT': 'TEMPORARY_OUTPUT'})['OUTPUT']

        add_layer_gui(output_extracted, lay_name + '_after')
        DANUBE_LAYERS[lay_name]['layer'] = output_extracted

        add_layer_gui(DANUBE_LAYERS[lay_name]['layer'], lay_name + '_after_zone_selection')
    add_layer_gui(DANUBE_LAYERS['GEO_ZONE']['layer'], 'GEO_ZONE')

    return DANUBE_LAYERS

##### TODO : Take out fictif from activite

if __name__ == '__console__':

    if DEV_TEST:
        from dev_set_test import DANUBE_LAYERS

        DANUBE_LAYERS = main_dc_2(DANUBE_LAYERS)
        DANUBE_LAYERS = main_dc_3(DANUBE_LAYERS)

    else:
        pass


