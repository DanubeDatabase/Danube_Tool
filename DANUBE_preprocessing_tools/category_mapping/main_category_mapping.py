from category_mapping.map_period import main_cm_period
from category_mapping.map_territory import main_cm_territory
from category_mapping.map_typology import main_cm_typology
from category_mapping.map_usage import main_cm_usage

def main_cm_category_mapping():
    print("+" * 100)
    print("--------------- START MAPPING DANUBE CATEGORIES -----------------")
    print("+" * 100)

    main_cm_period()
    main_cm_territory()
    main_cm_typology()
    main_cm_usage()

    print("+" * 100)
    print("--------------- END MAPPING DANUBE CATEGORIES -----------------")
    print("+" * 100)

if __name__ == '__console__':
    main_cm_category_mapping()
