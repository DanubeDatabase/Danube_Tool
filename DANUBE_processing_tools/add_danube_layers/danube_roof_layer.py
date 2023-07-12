import pandas as pd

from config_show import print_log, print_fields
from category_mapping.map_reference.shared_ref import PATH_DANUBE_TABLES_FOLDER
from add_danube_layers.shared_functions import convert_danube_df_to_layer, join_danube_layer_base


def prepare_danube_roof1_fields(df, PATH_DANUBE_TABLES_FOLDER, loc):
    # open danube tables
    path_cat = PATH_DANUBE_TABLES_FOLDER / "CATALOGUE-export.csv"
    cat = pd.read_csv(path_cat)
    print("\nDanube catalogue:\n", cat.columns)

    path_renov = PATH_DANUBE_TABLES_FOLDER / "RENOVATION-complete_study.csv"
    ren = pd.read_csv(path_renov)
    print("\nDanube renovation:\n", ren.columns)

    path_roof = PATH_DANUBE_TABLES_FOLDER / "DISPOSITIF_TOITS-export.csv"
    roof = pd.read_csv(path_roof)
    print("\nDanube roof:\n", roof.columns)

    # get fields related to roof 1 inside danube tables
    cat_roof = cat[["ID_ARCHETYPE",
                    "DISPOSITIF_TOIT_OPTION1"]].merge(roof.add_suffix('_T1'), left_on='DISPOSITIF_TOIT_OPTION1',
                                                     right_on='DISPOSITIF_T1',
                                                     how='left')
    print("\nDanube cat_roof:\n", cat_roof.columns)

    ren_roof = ren[['ID_ARCHETYPE'] + [el for el in ren.columns if ('roof' in el)]]
    print("\nDanube ren_roof:\n", ren_roof.columns)

    cat_ren_roof = cat_roof.merge(ren_roof, how='left', on='ID_ARCHETYPE')
    print("\nDanube cat_ren_roof:\n", cat_ren_roof.columns)

    # merge with preprocess df
    df_roof = df[['ID_BUILD', f'arch_{loc}', f'arch_{loc}_id']
    ].merge(cat_ren_roof, left_on=f'arch_{loc}_id', right_on='ID_ARCHETYPE', how='left')
    print("\ndf_roof:\n", df_roof.columns)

    return df_roof


def get_roof_output_layer(df, base_layer, location):
    print_log("+" * 100)
    print_log("Run step 3 of add danube layers : get_roof_layer - Join danube fields for roof to base layer")
    print_log("+" * 100)

    # merge relevant fields from df and danube tables into one df
    roof1_df = prepare_danube_roof1_fields(df, PATH_DANUBE_TABLES_FOLDER, location)
    prefix_name = "DANUBE_roof"

    # convert relevant df to QgsVectorLayer
    roof_layer_from_csv, roof_csv_path = convert_danube_df_to_layer(roof1_df, prefix_name)
    print_fields(roof_layer_from_csv)

    # join previous layer with the base_layer
    roof_layer = join_danube_layer_base(roof_layer_from_csv, base_layer)
    print_fields(roof_layer)

    return roof_layer
