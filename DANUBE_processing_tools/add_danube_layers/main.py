from config_show import timed_execution, print_log

from add_danube_layers.create_base_layer import provide_geometry_for_danube_layers
from add_danube_layers.danube_wall_layer import get_wall_output_layer
from add_danube_layers.danube_roof_layer import get_roof_output_layer
from add_danube_layers.danube_floor_layer import get_floor_output_layer
from add_danube_layers.danube_window_layer import get_window_output_layer


def main_add_danube_layers(df, DANUBE_LAYERS, location):
    print_log("+" * 100)
    print_log("--------------- START DANUBE LAYERS -----------------")
    print_log("+" * 100)
    print_log(f"\nBuild danube layers considering {location} territories\n")

    # ---------- provide layers with danube information
    # base layer to join danube layers
    base_layer = provide_geometry_for_danube_layers(DANUBE_LAYERS)
    # wall
    DANUBE_LAYERS['DANUBE_MUR'] = {"id": "DANUBE_MUR", "type": "OUTPUT", 'layer': None}
    DANUBE_LAYERS['DANUBE_MUR']['layer'] = get_wall_output_layer(df, base_layer, location)
    DANUBE_LAYERS['DANUBE_MUR']['layer'].setName('DANUBE_MUR')
    print_log('\nDANUBE_LAYERS.keys(): ', DANUBE_LAYERS.keys())
    # roof
    DANUBE_LAYERS['DANUBE_TOIT'] = {"id": "DANUBE_TOIT", "type": "OUTPUT", 'layer': None}
    DANUBE_LAYERS['DANUBE_TOIT']['layer'] = get_roof_output_layer(df, base_layer, location)
    DANUBE_LAYERS['DANUBE_TOIT']['layer'].setName('DANUBE_TOIT')
    print_log('\nDANUBE_LAYERS.keys(): ', DANUBE_LAYERS.keys())
    # floor
    DANUBE_LAYERS['DANUBE_PLANCHER'] = {"id": "DANUBE_PLANCHER", "type": "OUTPUT", 'layer': None}
    DANUBE_LAYERS['DANUBE_PLANCHER']['layer'] = get_floor_output_layer(df, base_layer, location)
    DANUBE_LAYERS['DANUBE_PLANCHER']['layer'].setName('DANUBE_PLANCHER')
    print_log('\nDANUBE_LAYERS.keys(): ', DANUBE_LAYERS.keys())
    # window
    DANUBE_LAYERS['DANUBE_VITRAGE'] = {"id": "DANUBE_VITRAGE", "type": "OUTPUT", 'layer': None}
    DANUBE_LAYERS['DANUBE_VITRAGE']['layer'] = get_window_output_layer(df, base_layer, location)
    DANUBE_LAYERS['DANUBE_VITRAGE']['layer'].setName('DANUBE_VITRAGE')
    print_log('\nDANUBE_LAYERS.keys(): ', DANUBE_LAYERS.keys())

    print_log("+" * 100)
    print_log("--------------- END DANUBE LAYERS -----------------")
    print_log("+" * 100)

    return DANUBE_LAYERS
