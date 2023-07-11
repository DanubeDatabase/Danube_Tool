from config_show import print_log, print_memory_use, timed_execution, add_layer_gui
from data_consolidation.dc1_building_base_layer import main_dc_1
from data_consolidation.dc2_create_spatial_index import main_dc_2
from data_consolidation.dc3_select_zone import main_dc_3
from data_consolidation.dc4_add_topo_activ import main_topo_activ
from data_consolidation.dc5_add_filosofi import add_filo
from data_consolidation.dc6_convert_to_df import main_dc6_convert_to_df


DELETE_KEYS = False
if DELETE_KEYS:
    import gc




def main_dc_data_consolidation(DANUBE_LAYERS):
    """provide all relevant variables to calculate Danube 4 inputs"""
    print_log("+" * 100)
    print_log("--------------- START DATA CONSOLIDATION -----------------")
    print_log("+" * 100)
    print_memory_use()
    # ____________________________________________________________________________________________________________

    # step 1  - construct building base layer with algorithms independent of spatial attributes
    DANUBE_LAYERS = timed_execution(main_dc_1, DANUBE_LAYERS)

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

    # ____________________________________________________________________________________________________________

    # step 5 - calculate and add attributes from filosofi: dens_pop, and all log (period of construction)
    DANUBE_LAYERS =  timed_execution(add_filo, DANUBE_LAYERS)
    print_memory_use()

    # ____________________________________________________________________________________________________________

    # step 6 - convert DANUBE_BUILD_PREPROCESS to DataFrame and add city dept info

    DANUBE_LAYERS, df_output_dc = timed_execution(main_dc6_convert_to_df, DANUBE_LAYERS)


    print_log("+" * 100)
    print_log("--------------- END DATA CONSOLIDATION -----------------")
    print_log("+" * 100)

    return DANUBE_LAYERS, df_output_dc

if __name__ == '__console__':

    df_output_dc = main_dc_data_consolidation(DANUBE_LAYERS)
