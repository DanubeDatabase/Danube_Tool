import processing

from config_show import add_layer_gui, print_log, print_fields


def main_dc_3(DANUBE_LAYERS):
    """Select the studied zone from 'TOPO_ACTIVITE' and 'FILOSOFI' layers to optimize the further spatial joins """
    print_log("*" * 100)
    print_log("Run step 3 of data consolidation : reduce size of data to the perimeters of the GEO_ZONE")
    print_log("*" * 100)

    # create spatial index to the layers which will be further used
    to_reduce = ['TOPO_ACTIVITE', 'FILOSOFI']
    for lay_name in to_reduce:
        print_log(lay_name)
        add_layer_gui(DANUBE_LAYERS[lay_name]['layer'], lay_name + '_dc3_before_zone_selection')

        output_extracted = processing.run("native:extractbylocation",
                                          {'INPUT': DANUBE_LAYERS[lay_name]['layer'],
                                           'PREDICATE': [0],
                                           'INTERSECT': DANUBE_LAYERS['GEO_ZONE']['layer'],
                                           'OUTPUT': 'TEMPORARY_OUTPUT'})['OUTPUT']

        DANUBE_LAYERS[lay_name]['layer'] = output_extracted

        print_fields(output_extracted)









        add_layer_gui(DANUBE_LAYERS[lay_name]['layer'], lay_name + '_dc3_after_zone_selection')

    return DANUBE_LAYERS


if __name__ == '__console__':

    from config_show import DANUBE_LAYERS

    DANUBE_LAYERS = main_dc_2(DANUBE_LAYERS)
    DANUBE_LAYERS = main_dc_3(DANUBE_LAYERS)



