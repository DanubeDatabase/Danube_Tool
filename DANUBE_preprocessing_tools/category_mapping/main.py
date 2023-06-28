


from config_show import print_log
from category_mapping.map_period import main_cm_period
from category_mapping.map_territory import main_cm_territory
from category_mapping.map_typology import main_cm_typology
from category_mapping.map_usage import main_cm_usage


def main_cm_category_mapping(df):
    print_log("+" * 100)
    print_log("--------------- START MAPPING DANUBE CATEGORIES -----------------")
    print_log("+" * 100)

    print_log("\nCheck input data\n")
    print_log("len(df): ", len(df))
    print_log("df.columns: ",df.columns)
    print_log("df.head(): ",df.head())

    main_cm_typology(df)
    main_cm_usage(df)
    main_cm_period(df)
    main_cm_territory(df)

    print_log("+" * 100)
    print_log("--------------- END MAPPING DANUBE CATEGORIES -----------------")
    print_log("+" * 100)

if __name__ == '__console__':
    main_cm_category_mapping()
