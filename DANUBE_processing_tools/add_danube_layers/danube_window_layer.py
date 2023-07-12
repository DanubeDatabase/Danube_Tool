import pandas as pd

from config_show import print_log, print_fields
from category_mapping.map_reference.shared_ref import PATH_DANUBE_TABLES_FOLDER
from add_danube_layers.shared_functions import convert_danube_df_to_layer, join_danube_layer_base


def prepare_danube_window_fields(df, PATH_DANUBE_TABLES_FOLDER, loc):
    # open danube tables
    path_cat = PATH_DANUBE_TABLES_FOLDER / "CATALOGUE-export.csv"
    cat = pd.read_csv(path_cat)
    print("\nDanube catalogue:\n", cat.columns)

    path_renov = PATH_DANUBE_TABLES_FOLDER / "RENOVATION-complete_study.csv"
    ren = pd.read_csv(path_renov)
    print("\nDanube renovation:\n", ren.columns)

    path_window = PATH_DANUBE_TABLES_FOLDER / "DISPOSITIF_TOITS-export.csv"
    window = pd.read_csv(path_window)
    print("\nDanube window:\n", window.columns)

    # get fields related to window inside danube tables
    cat_window = cat[["ID_ARCHETYPE",
                      'VENTILATION',  # do not remove or comment this line.
                                      # It adds a not useful field to be removed later in
                      'POURCENTAGE_VITRAGE',
                      'PROTECTIONS_SOLAIRES',
                      'TYPE_VITRAGE'
                      ]]
    print("\nDanube cat_window:\n", cat_window.columns)

    ren_window = ren[['ID_ARCHETYPE',
                      'perc_simple_vit_3CL',
                      'perc_double_vit_3CL',
                      'perc_triple_vit_3CL',
                      'main_vit_3CL',
                      # 'main_vit_Danube',
                      'Danube_equal_3CL']]
    print("\nDanube ren_window:\n", ren_window.columns)

    cat_ren_window = cat_window.merge(ren_window, how='left', on='ID_ARCHETYPE')
    print("\nDanube cat_ren_window:\n", cat_ren_window.columns)

    # merge with preprocess df
    df_window = df[['ID_BUILD', f'arch_{loc}', f'arch_{loc}_id']
    ].merge(cat_ren_window, left_on=f'arch_{loc}_id', right_on='ID_ARCHETYPE', how='left')
    print("\ndf_window:\n", df_window.columns)

    return df_window


def get_window_output_layer(df, base_layer, location):
    print_log("+" * 100)
    print_log("Run step 5 of add danube layers : get_window_output_layer - Join danube fields for window to base layer")
    print_log("+" * 100)

    # merge relevant fields from df and danube tables into one df
    window1_df = prepare_danube_window_fields(df, PATH_DANUBE_TABLES_FOLDER, location)
    prefix_name = "DANUBE_window"

    # convert relevant df to QgsVectorLayer
    window_layer_from_csv, window_csv_path = convert_danube_df_to_layer(window1_df, prefix_name)
    print_fields(window_layer_from_csv)

    # join previous layer with the base_layer
    window_layer = join_danube_layer_base(window_layer_from_csv, base_layer)
    print_fields(window_layer)

    return window_layer
