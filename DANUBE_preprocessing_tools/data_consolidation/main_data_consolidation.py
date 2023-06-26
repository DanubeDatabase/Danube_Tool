import gc
from dev_set_test import print_d, print_memory_use, timed_execution_d, print_fields_d, SHOW_GUI_LAY, add_layer_gui
from data_consolidation.building_base_layer import main_dc_1
from data_consolidation.create_spatial_index import main_dc_2
from data_consolidation.select_zone import main_dc_3
from data_consolidation.spatial_joins import main_dc_4

# TODO #############################################
# # define log file
#   # for Python3
# name_executed = 'TEST'
# name_log = f'myLog_{name_executed}_{datetime.now().strftime("%m-%d-%Y_%Hh%Mmin")}.log'
# handlers = [logging.FileHandler(name_log), logging.StreamHandler()]
# logging.basicConfig(level = logging.INFO,
#                     format = '  %(message)s',
#                     handlers = handlers)
# log_dir = r"C:\Users\lorena.carvalho\Documents\Develop_outil\code\pyqgis\logging info test"
# os.chmod(log_dir, 0o777)


def main_dc_data_consolidation(DANUBE_LAYERS):
    """provide all relevant variables to calculate Danube 4 inputs"""
    print("+" * 100)
    print("--------------- START DATA CONSOLIDATION -----------------")
    print("+" * 100)
    print_memory_use()
    # ____________________________________________________________________________________________________________
    # step 1  - construct building base layer with algorithms independent of spatial attributes
    DANUBE_LAYERS = timed_execution_d(main_dc_1)
    add_layer_gui(DANUBE_LAYERS['DANUBE_BUILD_PREPROCESS']['layer'])


    # TODO #############################################
    def delete_dc1_used_layers(DANUBE_LAYERS):
        print_d("\nBefore deleting layers")
        print_d("DANUBE_LAYERS", DANUBE_LAYERS.keys())
        print_memory_use()

        del DANUBE_LAYERS['GEO_BUILD_URTF']
        del DANUBE_LAYERS['GEO_BUILD_IND']
        del DANUBE_LAYERS['TOPO_BATI']

        gc.collect()

        print_d("\nAfter deleting layers")
        print_d("DANUBE_LAYERS.keys", DANUBE_LAYERS.keys())
        print_memory_use()

    # comment the line below if you want to keep the layers which will not be further used
    # delete_dc1_used_layers(DANUBE_LAYERS)

    # ____________________________________________________________________________________________________________
    # step 2  - create spatial index to optimize pp3 and pp4, which need spatial actions
    DANUBE_LAYERS = timed_execution_d(main_dc_2, DANUBE_LAYERS)
    print_memory_use()
    # ____________________________________________________________________________________________________________
    # step 3 - select zone by location
    DANUBE_LAYERS = main_dc_3(DANUBE_LAYERS)
    print_memory_use()
    # ____________________________________________________________________________________________________________
    # pp4 - join attributes from FILOSOFI and TOPO_ACTIVITE using spatial attributes
    DANUBE_LAYERS =  main_dc_4(DANUBE_LAYERS)
    print_memory_use()
    # ____________________________________________________________________________________________________________

    print("+" * 100)
    print("--------------- END DATA CONSOLIDATION -----------------")
    print("+" * 100)

    return DANUBE_LAYERS

if __name__ == '__console__':

    DANUBE_LAYERS = main_dc_data_consolidation(DANUBE_LAYERS)
