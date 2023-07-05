import pandas as pd

from config_show import print_log

def main_cm_territory(df, DANUBE_LAYERS):
    print_log("*" * 100)
    print_log("Run category_mapping - main_cm_territory : mapping Danube territory")
    print_log("*" * 100)

    city_id = [feature['ID_ZONE'] for feature in DANUBE_LAYERS['GEO_ZONE']['layer'].getFeatures()][0]
    print_log('_' * 21, 'city_id', '_' * 21, '\n')
    print_log(city_id)

    df["location_dept"] = city_id[:2]
    df["location_city"] = city_id

    df['location_source'] = 'geoclimate'

    df['location_quality'] = 'A' # From geoclimate. It comes directly from city location.


    print_log('\ndf.head(): ', df.head(), "\n")
    print_log('\ndf.columns: ', df.columns, "\n")