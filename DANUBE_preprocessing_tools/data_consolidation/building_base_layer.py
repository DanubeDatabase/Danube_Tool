import processing

from dev_set_test import DANUBE_LAYERS, print_d, print_fields_d


def building_base_layer(DANUBE_LAYERS):
    """Define building base layer with only non spatial field value joins"""

    print_d("Join building layers : geo_build_utrf, geo_build_ind, topo_bati")

    print_fields_d(DANUBE_LAYERS['GEO_BUILD_URTF']['layer'])
    print_fields_d(DANUBE_LAYERS['GEO_BUILD_IND']['layer'])

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

    print_fields_d(joined_geo_utrf_ind)
    print_fields_d(DANUBE_LAYERS['TOPO_BATI']['layer'])

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
    print_fields_d(joined_buildgeo_bdtopo)

    print_fields_d(joined_buildgeo_bdtopo)

    return joined_buildgeo_bdtopo

def main_dc_1():
    """Create first layer for 'DANUBE_BUILD_PREPROCESS' from building base layer"""
    print("\n")
    print("*" * 100)
    print("Run step 1 of data consolidation : Define building base layer with field value joins from:\
                        \nGeoclimate building utrf and building indicator and BD TOPO building layer")
    print("*" * 100)

    DANUBE_LAYERS['DANUBE_BUILD_PREPROCESS']['layer'] = building_base_layer(DANUBE_LAYERS)
    DANUBE_LAYERS['DANUBE_BUILD_PREPROCESS']['layer'].setName('DANUBE_BUILD_PREPROCESS_out1dc_build_base')

    return DANUBE_LAYERS


if __name__ == '__console__':

    main_dc_1()
