import processing
from config_show import print_log, print_fields, add_layer_gui


def building_base_layer(DANUBE_LAYERS):
    """Define building base layer with only non spatial field value joins"""

    print_log("Join building layers : geo_build_utrf, geo_build_ind, topo_bati")

    print_fields(DANUBE_LAYERS['GEO_BUILD_URTF']['layer'])
    print_fields(DANUBE_LAYERS['GEO_BUILD_IND']['layer'])

    joined_geo_utrf_ind = processing.run("native:joinattributestable",
                                                {'INPUT':DANUBE_LAYERS['GEO_BUILD_URTF']['layer'],
                                                'FIELD':'ID_BUILD',
                                                'INPUT_2':DANUBE_LAYERS['GEO_BUILD_IND']['layer'],
                                                'FIELD_2':'ID_BUILD',
                                                'FIELDS_TO_COPY':['ID_SOURCE','MAIN_USE','FLOOR_AREA'],
                                                'METHOD':1,
                                                'DISCARD_NONMATCHING':True,
                                                'PREFIX':'',
                                                'OUTPUT':'TEMPORARY_OUTPUT'})['OUTPUT']

    print_fields(joined_geo_utrf_ind)
    print_fields(DANUBE_LAYERS['TOPO_BATI']['layer'])

    # previous layers and topo bati by field value
    joined_buildgeo_bdtopo = processing.run('native:joinattributestable',
                                             {
                                                'INPUT': joined_geo_utrf_ind,
                                                'FIELD': 'ID_SOURCE',
                                                'INPUT_2': DANUBE_LAYERS['TOPO_BATI']['layer'],
                                                'FIELD_2': 'ID',
                                                'FIELDS_TO_COPY': ["ID","NATURE","USAGE1","USAGE2","DATE_APP"],
                                                'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
                                                'DISCARD_NONMATCHING': True,
                                                'PREFIX': "topo_",
                                                'OUTPUT':'TEMPORARY_OUTPUT'})['OUTPUT']
    print_fields(joined_buildgeo_bdtopo)

    print_fields(joined_buildgeo_bdtopo)

    return joined_buildgeo_bdtopo

def main_dc_1(DANUBE_LAYERS):
    """Create first layer for 'DANUBE_BUILD_PREPROCESS' from building base layer"""
    print_log("\n")
    print_log("*" * 100)
    print_log("Run step 1 of data consolidation : Define building base layer with field value joins from:\
                        \nGeoclimate building utrf and building indicator and BD TOPO building layer")
    print_log("*" * 100)

    DANUBE_LAYERS['DANUBE_BUILD_PREPROCESS']['layer'] = building_base_layer(DANUBE_LAYERS)
    add_layer_gui(DANUBE_LAYERS['DANUBE_BUILD_PREPROCESS']['layer'], 'DANUBE_BUILD_PREPROCESS_dc1_building_base')

    return DANUBE_LAYERS


if __name__ == '__console__':

    main_dc_1(DANUBE_LAYERS)
