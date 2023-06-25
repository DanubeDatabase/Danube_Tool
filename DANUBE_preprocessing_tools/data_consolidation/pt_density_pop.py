# from pt_basic_functions import DEBUG

def dens_pop():
    print("\n ______Function dens_pop______\n")

    # # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
    # # overall progress through the model
    # feedback = QgsProcessingMultiStepFeedback(7, model_feedback)
    # results = {}
    # outputs = {}
    #
    # # Centroids
    # alg_params = {
    #     'ALL_PARTS': False,
    #     'INPUT': parameters['buildingindicators'],
    #     'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
    # }
    # outputs['Centroids'] = processing.run('native:centroids', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
    #
    # feedback.setCurrentStep(1)
    # if feedback.isCanceled():
    #     return {}
    #
    # # Join attributes by location (summary) - floor area
    # alg_params = {
    #     'DISCARD_NONMATCHING': False,
    #     'INPUT': parameters['filosofi'],
    #     'JOIN': outputs['Centroids']['OUTPUT'],
    #     'JOIN_FIELDS': ['FLOOR_AREA'],
    #     'PREDICATE': [1],  # contains
    #     'SUMMARIES': [5],  # sum
    #     'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
    # }
    # outputs['JoinAttributesByLocationSummaryFloorArea'] = processing.run('qgis:joinbylocationsummary', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
    #
    # feedback.setCurrentStep(2)
    # if feedback.isCanceled():
    #     return {}
    #
    # # Refactor fields
    # alg_params = {
    #     'FIELDS_MAPPING': [{'expression': '"fid"','length': 0,'name': 'fid','precision': 0,'type': 4},{'expression': '"Ind"','length': 0,'name': 'Ind','precision': 0,'type': 6},{'expression': '"FLOOR_AREA_sum"','length': 20,'name': 'FLOOR_AREA_sum','precision': 6,'type': 6}],
    #     'INPUT': outputs['JoinAttributesByLocationSummaryFloorArea']['OUTPUT'],
    #     'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
    # }
    # outputs['RefactorFields'] = processing.run('native:refactorfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
    #
    # feedback.setCurrentStep(3)
    # if feedback.isCanceled():
    #     return {}
    #
    # # Field calculator - dens_pop
    # alg_params = {
    #     'FIELD_LENGTH': 10,
    #     'FIELD_NAME': 'dens_pop',
    #     'FIELD_PRECISION': 3,
    #     'FIELD_TYPE': 0,  # Float
    #     'FORMULA': '"Ind" / "FLOOR_AREA_sum"',
    #     'INPUT': outputs['RefactorFields']['OUTPUT'],
    #     'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
    # }
    # outputs['FieldCalculatorDens_pop'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
    #
    # feedback.setCurrentStep(4)
    # if feedback.isCanceled():
    #     return {}
    #
    # # Join attributes by location _ centroids into squares
    # alg_params = {
    #     'DISCARD_NONMATCHING': False,
    #     'INPUT': outputs['Centroids']['OUTPUT'],
    #     'JOIN': outputs['FieldCalculatorDens_pop']['OUTPUT'],
    #     'JOIN_FIELDS': ['dens_pop'],
    #     'METHOD': 0,  # Create separate feature for each matching feature (one-to-many)
    #     'PREDICATE': [5],  # within
    #     'PREFIX': '',
    #     'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
    # }
    # outputs['JoinAttributesByLocation_CentroidsIntoSquares'] = processing.run('native:joinattributesbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
    #
    # feedback.setCurrentStep(5)
    # if feedback.isCanceled():
    #     return {}
    #
    # # Join attributes by field value - centroids and buildings
    # alg_params = {
    #     'DISCARD_NONMATCHING': False,
    #     'FIELD': 'fid',
    #     'FIELDS_TO_COPY': ['dens_pop'],
    #     'FIELD_2': 'fid',
    #     'INPUT': parameters['buildingindicators'],
    #     'INPUT_2': outputs['JoinAttributesByLocation_CentroidsIntoSquares']['OUTPUT'],
    #     'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
    #     'PREFIX': '',
    #     'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
    # }
    # outputs['JoinAttributesByFieldValueCentroidsAndBuildings'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
    #
    # feedback.setCurrentStep(6)
    # if feedback.isCanceled():
    #     return {}
    #
    # # Join attributes by field value
    # alg_params = {
    #     'DISCARD_NONMATCHING': False,
    #     'FIELD': 'ID_BUILD',
    #     'FIELDS_TO_COPY': ['I_TYPO'],
    #     'FIELD_2': 'ID_BUILD',
    #     'INPUT': outputs['JoinAttributesByFieldValueCentroidsAndBuildings']['OUTPUT'],
    #     'INPUT_2': parameters['buildingutrf'],
    #     'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
    #     'PREFIX': '',
    #     'OUTPUT': parameters['Building_with_dens_and_typo']
    # }
    # outputs['JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
    # results['Building_with_dens_and_typo'] = outputs['JoinAttributesByFieldValue']['OUTPUT']
    # return results
