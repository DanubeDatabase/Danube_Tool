import pandas as pd

from config_show import print_log, print_fields
from category_mapping.map_reference.shared_ref import PATH_DANUBE_TABLES_FOLDER
from add_danube_layers.shared_functions import convert_danube_df_to_layer, join_danube_layer_base


def prepare_danube_wall1_fields(df, PATH_DANUBE_TABLES_FOLDER, loc):
    # open danube tables
    path_cat = PATH_DANUBE_TABLES_FOLDER / "CATALOGUE-export.csv"
    cat = pd.read_csv(path_cat)
    print("\nDanube catalogue:\n", cat.columns)

    path_renov = PATH_DANUBE_TABLES_FOLDER / "RENOVATION-complete_study.csv"
    ren = pd.read_csv(path_renov)
    print("\nDanube renovation:\n", ren.columns)

    path_wall = PATH_DANUBE_TABLES_FOLDER / "DISPOSITIFS_MUR-export.csv"
    wall = pd.read_csv(path_wall)
    print("\nDanube wall:\n", wall.columns)

    # get fields related to wall 1 inside danube tables
    cat_wall = cat[["ID_ARCHETYPE",
                    "DISPOSITIF_MUR_OPTION1"]].merge(wall.add_suffix('_M1'), left_on='DISPOSITIF_MUR_OPTION1',
                                                     right_on='DISPOSITIF_M1',
                                                     how='left')
    print("\nDanube cat_wall:\n", cat_wall.columns)

    ren_wall = ren[['ID_ARCHETYPE'] + [el for el in ren.columns if ('wall' in el)]]
    print("\nDanube ren_wall:\n", ren_wall.columns)

    cat_ren_wall = cat_wall.merge(ren_wall, how='left', on='ID_ARCHETYPE')
    print("\nDanube cat_ren_wall:\n", cat_ren_wall.columns)

    # merge with preprocess df
    df_wall = df[['ID_BUILD', f'arch_{loc}', f'arch_{loc}_id']
    ].merge(cat_ren_wall, left_on=f'arch_{loc}_id', right_on='ID_ARCHETYPE', how='left')
    print("\ndf_wall:\n", df_wall.columns)

    return df_wall


def get_wall_output_layer(df, base_layer, location):
    print_log("+" * 100)
    print_log("Run step 2 of add danube layers : get_wall_output_layer - Join danube fields for wall to base layer")
    print_log("+" * 100)

    # merge relevant fields from df and danube tables into one df
    wall1_df = prepare_danube_wall1_fields(df, PATH_DANUBE_TABLES_FOLDER, location)
    prefix_name = "DANUBE_WALL"

    # convert relevant df to QgsVectorLayer
    wall_layer_from_csv, wall_csv_path = convert_danube_df_to_layer(wall1_df, prefix_name)
    print_fields(wall_layer_from_csv)

    # join previous layer with the base_layer
    wall_layer = join_danube_layer_base(wall_layer_from_csv, base_layer)
    print_fields(wall_layer)

    return wall_layer
