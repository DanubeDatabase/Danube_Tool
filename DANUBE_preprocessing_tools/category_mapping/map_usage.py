from pathlib import Path
from qgis.core import QgsField, QgsProject
from qgis.core import (NULL
                       )
from PyQt5.QtCore import QVariant

import pandas as pd
import processing




def usage_from_topo(bati, activ):

    #___________________Open Danube association files to BDTOPO categories___________________
    # charge pandas layer

    path_relation_activ_usage = r"C:\Users\lorena.carvalho\Documents\Develop_outil\auxiliary_tables\associations_activ_nature_usage_danube.xlsx"
    relation_activ_usage = pd.read_excel(path_relation_activ_usage, usecols=[0,1])
    printd(relation_activ_usage.columns)
    printd(relation_activ_usage.head())

    path_relation_bati_usage = r"C:\Users\lorena.carvalho\Documents\Develop_outil\auxiliary_tables\associations_bati_usage1_nature_usage_danube.xlsx"
    relation_bati_usage = pd.read_excel(path_relation_bati_usage, usecols=[0,1,2,3])
    printd(relation_bati_usage.columns)
    printd(relation_bati_usage.head())



    #___________________Associate Danube usage to the"batiment" layer___________________

    def associate_usage_from_bati(relation_bati_usage, layer_bati):
        # make a layer copy
        bati_copy = copy_layer(layer_bati)
        bati_copy.startEditing()

        # define the parameters of new fields
        field_name = ['usage_from_bati_usage1', 'usage_from_bati_nature']
        field_type = QVariant.String
        field_length = 255
        # create new field
        new_field0 = QgsField(field_name[0], field_type, '', field_length)
        new_field1 = QgsField(field_name[1], field_type, '', field_length)

        layer_provider = bati_copy.dataProvider()
        layer_provider.addAttributes([new_field0, new_field1])
        bati_copy.updateFields()

        # Get the index of the new column in the attribute table
        new_column_index0 = bati_copy.fields().indexFromName(field_name[0])
        new_column_index1 = bati_copy.fields().indexFromName(field_name[1])

        for feature in bati_copy.getFeatures():
            # Get the value from the DataFrame based on a unique identifier in the layer
            value0 = relation_bati_usage.loc[relation_bati_usage['USAGE1'] == feature['USAGE1'], 'ASSOCIATION_USAGE1_DAN'].values[0]
            value1 = relation_bati_usage.loc[relation_bati_usage['NATURE'] == feature['NATURE'], 'ASSOCIATION_NATURE_DAN'].values[0]
            if not pd.isna(value0):
                bati_copy.changeAttributeValue(feature.id(), new_column_index0, value0)
            if not pd.isna(value1):
                bati_copy.changeAttributeValue(feature.id(), new_column_index1, value1)
        bati_copy.commitChanges()

        return bati_copy

    # Apply the function => create a usage field using the relation from NATURE from the layer 'activ' and the Danube usage categories
    bati_copy = associate_usage_from_bati(relation_bati_usage, bati)
    # print("\nBATI COPY FIELDS:\n", bati_copy.fields().names())


    #___________________Associate Danube usage into the "surface activité" layer___________________

    def associate_usage_from_activity(relation_activ_usage, layer_activ):

        # make a copy of a layer without saving any reference to the parent layer
        activ_copy = copy_layer(layer_activ)
        activ_copy.startEditing()

        # define the parameters of new fields
        field_name = 'usage_from_activ'
        field_type = QVariant.String
        field_length = 255
        # create new field
        new_field = QgsField(field_name, field_type, 'varchar', field_length)
        layer_provider = activ_copy.dataProvider()
        layer_provider.addAttributes([new_field])
        activ_copy.updateFields()

        # Get the index of the new column in the attribute table
        new_column_index = activ_copy.fields().indexFromName(field_name)

        for feature in activ_copy.getFeatures():
            # Get the value from the DataFrame based on a unique identifier in the layer
            value = relation_activ_usage.loc[relation_activ_usage['NATURE'] == feature['NATURE'], 'Association_Danube'].values[0]

            # Update the new column with the condition value
            activ_copy.changeAttributeValue(feature.id(), new_column_index, value)

        activ_copy.commitChanges()

        return activ_copy

    # Apply the function => create a usage field using the relation from NATURE from the layer 'activ' and the Danube usage categories

    activ_copy = associate_usage_from_activity(relation_activ_usage, activ)
    # print("\nACTIV COPY FIELDS:\n", activ_copy.fields().names())


    # #___________________Join "activ" and "bati" layers per location by largest intersection area_________________

    outputs = {}
    # join with the biggest intersect with the layer activity
    outputs['activ_bati_junction'] = processing.run("native:joinattributesbylocation",
                            {'INPUT':bati_copy,
                            'JOIN': activ_copy,
                            'PREDICATE':[0], # intersect
                            'JOIN_FIELDS':['usage_from_activ', 'ID_2','fid_2'],
                            'METHOD':2, # select just the feature with the largest matching area
                            'DISCARD_NONMATCHING':False,
                            'PREFIX':'',
                            'OUTPUT':'TEMPORARY_OUTPUT'})

    outputs['activ_bati_junction']['OUTPUT'].setName("usage_option_1_2")
    QgsProject.instance().addMapLayer(outputs['activ_bati_junction']['OUTPUT']) # comment later, just for test


    # # #___________________defines the usage from opt 1 and 2 develop_________________

    layer = outputs['activ_bati_junction']['OUTPUT']


    # Add a new field to the layer
    usage_danube_field = QgsField('Usage_Danube', QVariant.String, 'varchar', 255)
    source_usage_field = QgsField('Source_Usage', QVariant.String, 'varchar', 255)

    layer_provider = layer.dataProvider()
    layer_provider.addAttributes([source_usage_field, usage_danube_field ])
    layer.updateFields()

    # # Iterate over the features and update the new field based on the condition
    layer.startEditing()
    for feature in layer.getFeatures():
        feature['Usage_Danube'] = feature['usage_from_bati_usage1']
        feature['Source_Usage'] = 'bati_usage'
        # if feature['Usage_Danube'] == qgis.core.NULL:
        if feature['Usage_Danube'] == NULL:
            feature['Usage_Danube'] = feature['usage_from_bati_nature']
            feature['Source_Usage'] = 'bati_nature'
            # if feature['Usage_Danube'] == qgis.core.NULL:
            if feature['Usage_Danube'] == NULL:
                feature['Usage_Danube'] = feature['usage_from_activ']
                feature['Source_Usage'] = 'activ_nature'
                if feature['Usage_Danube'] == NULL:
                    feature['Source_Usage'] = NULL
        # print( feature['Usage_Danube'] , "--", type(feature['Usage_Danube']),"--", type(feature['usage_from_bati_nature']),"--", type(feature['usage_from_activ']),  )
        layer.updateFeature(feature)
    layer.commitChanges()

    return layer


def main_cm_usage():
    print("*" * 100)
    print("Run category_mapping - main_cm_usage : mapping Danube usage")
    print("*" * 100)

    print('TODO')

    #
    #
    # project = QgsProject.instance()
    # #___________________Open layers___________________
    # # Define path of samples for testing
    # folder_sample = Path(r"C:\Users\lorena.carvalho\Documents\Develop_outil\data\small_sample")
    # # path_bati = str(folder_sample / 'sample_topo_bati.gpkg')
    # # path_activ = str(folder_sample / 'sample_topo_activite.gpkg')
    # path_bati = str(folder_sample / 'small_bati.gpkg')
    # path_activ = str(folder_sample / 'small_activ.gpkg')
    #
    # # # Define path for Toulouse city testing
    # # folder_topo_toulouse = r"C:\Users\lorena.carvalho\Documents\Develop_outil\data\Haute_Garonne\BDTOPO\V3\BDTOPO_3-0_TOUSTHEMES_SHP_LAMB93_D031_2022-03-15\BDTOPO\1_DONNEES_LIVRAISON_2022-03-00081\BDT_3-0_SHP_LAMB93_D031-ED2022-03-15"
    # # path_bati = str(folder_topo_toulouse / Path(r'BATI\BATIMENT.shp'))
    # # path_activ = str(folder_topo_toulouse / Path(r'SERVICES_ET_ACTIVITES\ZONE_D_ACTIVITE_OU_D_INTERET.shp'))
    #
    # bati = open_layer(path_bati)
    # activ = open_layer(path_activ)
    # # bati = open_layer("sample_topo_bati")
    # # activ = open_layer("sample_topo_activite")
    #
    # printd("\nBATI FIELDS:\n", bati.fields().names())
    # printd("\nACTIV FIELDS:\n", activ.fields().names())
    #
    # #___________________Usage from BD TOPO___________________
    # layer = usage_from_topo(bati, activ)
    #
    # #___________________Usage from populatinal density___________________
    # dens_pop()

if __name__ == '__console__':
    main_cm_usage()
