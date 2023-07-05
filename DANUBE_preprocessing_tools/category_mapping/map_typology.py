import pandas as pd

from config_show import print_log
from category_mapping.map_reference.shared_ref import dataframe_to_dictionary

def main_cm_typology(df, PATH_REF_FOLDER):

    print_log("*" * 100)
    print_log("Run category_mapping - main_cm_typology : mapping Danube typology")
    print_log("*" * 100)

    # Independent file which describes the relation between the categories in geoclimate and Danube
    path_association_typo = PATH_REF_FOLDER / "associations_typo_geoclimate_danube.xlsx"
    typo_association = pd.read_excel(path_association_typo)
    typo_map_dict = dataframe_to_dictionary(typo_association, "typo_geoclimate", "typo_danube")

    print_log("Before map typology - df.head() ",df.head())

    df['typo_map'] = df['I_TYPO'].map(typo_map_dict)

    df['typo_source'] = 'geoclimate'

    df['typo_quality'] = 'C' # From geoclimate. It is estimated in geoclimate with their algorithm.

    print_log("\nAfter map typology  \n", df[['typo_map', 'typo_source', 'typo_quality']])
    print_log("df.columns ", df.columns)

    return df


