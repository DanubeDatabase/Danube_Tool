import pandas as pd

from config_show import print_log, print_fields
from category_mapping.map_reference.shared_ref import PATH_DANUBE_TABLES_FOLDER
from add_danube_layers.shared_functions import convert_danube_df_to_layer, join_danube_layer_base


def prepare_danube_floor_fields(df, PATH_DANUBE_TABLES_FOLDER, loc):
    # open danube tables
    path_cat = PATH_DANUBE_TABLES_FOLDER / "CATALOGUE-export.csv"
    cat = pd.read_csv(path_cat)
    print("\nDanube catalogue:\n", cat.columns)

    path_floor = PATH_DANUBE_TABLES_FOLDER / "PLANCHERS-export.csv"
    floor = pd.read_csv(path_floor)
    print("\nDanube floor:\n", floor.columns)

    # get fields related to floor 1 inside danube tables
    cat_floor = cat[["ID_ARCHETYPE",
                     "PLANCHER"]].merge(floor, left_on='PLANCHER',
                                        right_on='ID_PLANCHER',
                                        how='left')
    print("\nDanube cat_floor:\n", cat_floor.columns)

    # merge with preprocess df
    df_floor = df[['ID_BUILD', f'arch_{loc}', f'arch_{loc}_id']
    ].merge(cat_floor, left_on=f'arch_{loc}_id', right_on='ID_ARCHETYPE', how='left')
    print("\ndf_floor:\n", df_floor.columns)

    return df_floor


def get_floor_output_layer(df, base_layer, location):
    print_log("+" * 100)
    print_log("Run step 4 of add danube layers : get_floor_output_layer - Join danube fields for floor to base layer")
    print_log("+" * 100)

    # merge relevant fields from df and danube tables into one df
    floor_df = prepare_danube_floor_fields(df, PATH_DANUBE_TABLES_FOLDER, location)
    prefix_name = "DANUBE_floor"

    # convert relevant df to QgsVectorLayer
    floor_layer_from_csv, floor_csv_path = convert_danube_df_to_layer(floor_df, prefix_name)
    print_fields(floor_layer_from_csv)

    # join previous layer with the base_layer
    floor_layer = join_danube_layer_base(floor_layer_from_csv, base_layer)
    print_fields(floor_layer)

    return floor_layer
