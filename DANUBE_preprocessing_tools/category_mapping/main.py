from config_show import print_log
from category_mapping.map_year import main_cm_period
from category_mapping.map_dept_code_insee import main_cm_territory
from category_mapping.map_typology import main_cm_typology
from category_mapping.map_usage import main_cm_usage

from category_mapping.map_reference.shared_ref import PATH_REF_FOLDER

def main_cm_category_mapping(df, DANUBE_LAYERS):
    print_log("+" * 100)
    print_log("--------------- START MAPPING DANUBE CATEGORIES -----------------")
    print_log("+" * 100)

    print_log("\nCheck input DataFrame data\n")
    print_log("len(df): ", len(df))
    print_log("df.columns: ",df.columns)
    print_log("df.head(): ",df.head())

    main_cm_typology(df, PATH_REF_FOLDER)
    main_cm_usage(df, PATH_REF_FOLDER)
    main_cm_period(df)
    main_cm_territory(df, DANUBE_LAYERS)

    print_log("+" * 100)
    print_log("--------------- END MAPPING DANUBE CATEGORIES -----------------")
    print_log("+" * 100)

    return df

if __name__ == '__console__':
    main_cm_category_mapping(df)
