import processing
from qgis.core import QgsProcessing

from config_show import print_log, print_fields, add_layer_gui

def add_filo_dens_pop(DANUBE_LAYERS):
    print_log("*" * 100)
    print_log("Run step 5 of data consolidation : Spatially join FILOSOFI to the building layer and calculate populational density")
    print_log("*" * 100)
    outputs = {}


    print_log("\n ______Centroids of BUILD_BASE______\n")
    # Centroids
    alg_params = {
        'ALL_PARTS': False,
        'INPUT': DANUBE_LAYERS['BUILD_BASE']['layer'],
        'OUTPUT': 'TEMPORARY_OUTPUT'
    }
    outputs['Centroids'] = processing.run('native:centroids', alg_params)


    print_log("\n ______Join attributes by location (summary) - floor area______\n")
    # Join attributes by location (summary) - floor area
    alg_params = {
        'DISCARD_NONMATCHING': False,
        'INPUT': DANUBE_LAYERS['FILOSOFI']['layer'],
        'JOIN': outputs['Centroids']['OUTPUT'],
        'JOIN_FIELDS': ['FLOOR_AREA'],
        'PREDICATE': [1],  # contains
        'SUMMARIES': [5],  # sum
        'OUTPUT': 'TEMPORARY_OUTPUT'
    }
    outputs['JoinAttributesByLocationSummaryFloorArea'] = processing.run('qgis:joinbylocationsummary', alg_params)


    print_log("\n ______Field calculator - dens_pop______\n")
    # Field calculator - dens_pop
    alg_params = {
        'FIELD_LENGTH': 10,
        'FIELD_NAME': 'dens_pop',
        'FIELD_PRECISION': 3,
        'FIELD_TYPE': 0,  # Float
        'FORMULA': '"Ind" / "FLOOR_AREA_sum"',
        'INPUT': outputs['JoinAttributesByLocationSummaryFloorArea']['OUTPUT'],
        'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
    }
    outputs['FieldCalculatorDens_pop'] = processing.run('native:fieldcalculator', alg_params)

    print_log("Fields after run FieldCalculatorDens_pop")
    print_fields(outputs['FieldCalculatorDens_pop']['OUTPUT'])

    print_log("\n ______Join attributes by location _ filosofi squares into centroids______ \n")

    fields_filo_to_join = ['Idcar_nat','Ind','Men', 'Log_av45', 'Log_45_70', 'Log_70_90', 'Log_ap90', 'Log_inc']

    # Join attributes by location _ just the pure data from filosofi
    alg_params = {
        'DISCARD_NONMATCHING': False,
        'INPUT': outputs['Centroids']['OUTPUT'],
        'JOIN': outputs['FieldCalculatorDens_pop']['OUTPUT'],
        'JOIN_FIELDS': fields_filo_to_join,
        'METHOD': 0,  # Create separate feature for each matching feature (one-to-many)
        'PREDICATE': [5],  # within
        'PREFIX': 'filo_',
        'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
    }
    outputs['JoinAttributesByLocation_SquaresIntoCentroids_1'] = processing.run('native:joinattributesbylocation', alg_params)

    # Join attributes by location _ The calculated data: populations density
    alg_params = {
        'DISCARD_NONMATCHING': False,
        'INPUT': outputs['JoinAttributesByLocation_SquaresIntoCentroids_1']['OUTPUT'],
        'JOIN': outputs['FieldCalculatorDens_pop']['OUTPUT'],
        'JOIN_FIELDS': ['dens_pop'],
        'METHOD': 0,  # Create separate feature for each matching feature (one-to-many)
        'PREDICATE': [5],  # within
        'PREFIX': '',
        'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
    }
    outputs['JoinAttributesByLocation_SquaresIntoCentroids_2'] = processing.run('native:joinattributesbylocation', alg_params)

    print_log("Fields after run JoinAttributesByLocation_SquaresIntoCentroids")
    print_fields(outputs['JoinAttributesByLocation_SquaresIntoCentroids_2']['OUTPUT'])

    fields_filo_to_join = ["filo_" + elem for elem in fields_filo_to_join]
    fields_filo_to_join.append('dens_pop')

    print(fields_filo_to_join)

    print_log("\n ______Join attributes by field value - centroids and buildings______\n")
    # Join attributes by field value - centroids and buildings
    alg_params = {
        'DISCARD_NONMATCHING': False,
        'FIELD': 'fid',
        'FIELDS_TO_COPY': fields_filo_to_join,
        'FIELD_2': 'fid',
        'INPUT': DANUBE_LAYERS['BUILD_BASE']['layer'],
        'INPUT_2': outputs['JoinAttributesByLocation_SquaresIntoCentroids_2']['OUTPUT'],
        'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
        'PREFIX': '',
        'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
    }
    outputs['Building_with_filo_dens_pop'] = processing.run('native:joinattributestable', alg_params)


    DANUBE_LAYERS['BUILD_BASE']['layer'] = outputs['Building_with_filo_dens_pop']['OUTPUT']

    print_log("\nAfter join dens pop - BUILD_BASE fields")
    print_fields(DANUBE_LAYERS['BUILD_BASE']['layer'])
    add_layer_gui(DANUBE_LAYERS['BUILD_BASE']['layer'], 'BUILD_BASE_dc5_filo_dens_pop')

    return DANUBE_LAYERS
