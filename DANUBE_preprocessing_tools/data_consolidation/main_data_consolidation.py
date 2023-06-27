from config_show import print_log, print_memory_use, timed_execution, add_layer_gui
from data_consolidation.dc1_building_base_layer import main_dc_1
from data_consolidation.dc2_create_spatial_index import main_dc_2
from data_consolidation.dc3_select_zone import main_dc_3
from data_consolidation.dc4_add_topo_activ import main_topo_activ
from data_consolidation.dc5_add_filosofi_denspop import add_filo_dens_pop

DELETE_KEYS = False
if DELETE_KEYS:
    import gc

def delete_non_used_layers(DANUBE_LAYERS, keys_to_delete):
    print_log("\nBefore deleting layers")
    print_log("DANUBE_LAYERS", DANUBE_LAYERS.keys())
    print_memory_use()

    for key in keys_to_delete:
        del DANUBE_LAYERS[key]
    gc.collect()

    print_log("\nAfter deleting layers")
    print_log("DANUBE_LAYERS.keys", DANUBE_LAYERS.keys())
    print_memory_use()


def main_dc_data_consolidation(DANUBE_LAYERS):
    """provide all relevant variables to calculate Danube 4 inputs"""
    print_log("+" * 100)
    print_log("--------------- START DATA CONSOLIDATION -----------------")
    print_log("+" * 100)
    print_memory_use()
    # ____________________________________________________________________________________________________________

    # step 1  - construct building base layer with algorithms independent of spatial attributes
    DANUBE_LAYERS = timed_execution(main_dc_1, DANUBE_LAYERS)

    if DELETE_KEYS:
        delete_non_used_layers(DANUBE_LAYERS, ['GEO_BUILD_URTF','GEO_BUILD_IND','TOPO_BATI'] )

    # ____________________________________________________________________________________________________________

    # step 2  - create spatial index to optimize pp3 and pp4, which need spatial actions
    DANUBE_LAYERS = timed_execution(main_dc_2, DANUBE_LAYERS)
    print_memory_use()

    # ____________________________________________________________________________________________________________

    # step 3 - select zone by location
    DANUBE_LAYERS = timed_execution(main_dc_3, DANUBE_LAYERS)
    print_memory_use()

    # ____________________________________________________________________________________________________________

    # step 4 - join attributes from TOPO_ACTIVITE
    DANUBE_LAYERS =  timed_execution(main_topo_activ, DANUBE_LAYERS)
    print_memory_use()

    if DELETE_KEYS:
        delete_non_used_layers(DANUBE_LAYERS, ['TOPO_ACTIVITE'] )

    # ____________________________________________________________________________________________________________

    # step 5 - calculate and add attributes from filosofi: dens_pop, and all log (period of construction)
    DANUBE_LAYERS =  timed_execution(add_filo_dens_pop, DANUBE_LAYERS)
    print_memory_use()

    if DELETE_KEYS:
        delete_non_used_layers(DANUBE_LAYERS, ['FILOSOFI'] )
    # ____________________________________________________________________________________________________________

    print_log("+" * 100)
    print_log("--------------- END DATA CONSOLIDATION -----------------")
    print_log("+" * 100)

    return DANUBE_LAYERS

if __name__ == '__console__':

    DANUBE_LAYERS = main_dc_data_consolidation(DANUBE_LAYERS)
