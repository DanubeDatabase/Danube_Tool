import pandas as pd
import numpy as np

from config_show import print_log, timed_execution
from category_mapping.map_reference.shared_ref import PATH_DANUBE_TABLES_FOLDER


def define_dep_city_data(DANUBE_LAYERS, PATH_DANUBE_TABLES_FOLDER):
    city_id = [feature['ID_ZONE'] for feature in DANUBE_LAYERS['GEO_ZONE']['layer'].getFeatures()][0]

    df_dep = pd.read_csv(PATH_DANUBE_TABLES_FOLDER / "TERRITOIRES_PERIODES-DEPT-V4-export.csv")
    df_com = pd.read_csv(PATH_DANUBE_TABLES_FOLDER / "TERRITOIRES_PERIODES-COMMUNE-V5-export.csv")

    df_dep_terr = df_dep[df_dep.INSEE_DEP == city_id[:2]]
    df_com_terr = df_com[df_com.INSEE_COM == city_id]
    print("\ndf_dep territories: \n", df_dep_terr[["Terr_P1", "Terr_P2"]])
    print("\ndf_com territories: \n", df_com_terr[["Terr_P1", "Terr_P2"]])

    ter_dep_p1 = df_dep_terr.Terr_P1
    ter_dep_p2 = df_dep_terr.Terr_P2
    ter_com_p1 = df_com_terr.Terr_P1
    ter_com_p2 = df_com_terr.Terr_P2

    return ter_dep_p1, ter_dep_p2, ter_com_p1, ter_com_p2


def define_territory(df, DANUBE_LAYERS, PATH_DANUBE_TABLES_FOLDER):
    ter_dep_p1, ter_dep_p2, ter_com_p1, ter_com_p2 = define_dep_city_data(DANUBE_LAYERS, PATH_DANUBE_TABLES_FOLDER)
    df["territory_comm"] = np.where(pd.isna(df['period_map']), np.nan,
                                    np.where(df['period_map'] == 'P1', ter_com_p1,
                                             ter_com_p2))

    nan_part = df[pd.isna(df['period_map'])][["period_map", "territory_comm"]]
    print_log("\nnan_part", nan_part.head(), "\n")
    print_log(df[["period_map", "territory_comm"]].tail())

    df["territory_dept"] = np.where(pd.isna(df['period_map']), np.nan,
                                    np.where(df['period_map'] == 'P1', ter_dep_p1,
                                             ter_dep_p2))
    df['territory_source'] = 'geoclimate'
    df['territory_quality'] = 'A'  # From geoclimate. It comes directly from city location.


def main_cm_territory(df, DANUBE_LAYERS):
    print_log("*" * 100)
    print_log("Run category_mapping - main_cm_territory : mapping Danube territory")
    print_log("*" * 100)

    city_id = [feature['ID_ZONE'] for feature in DANUBE_LAYERS['GEO_ZONE']['layer'].getFeatures()][0]
    print_log('_' * 21, 'city_id', '_' * 21, '\n')
    print_log(city_id)

    df["location_dept"] = city_id[:2]
    df["location_comm"] = city_id

    df['location_source'] = 'geoclimate'

    df['location_quality'] = 'A'  # From geoclimate. It comes directly from city location.

    timed_execution(define_territory, df, DANUBE_LAYERS, PATH_DANUBE_TABLES_FOLDER)

    print_log('\ndf.head(): ', df.head(), "\n")
    print_log('\ndf.columns: ', df.columns, "\n")
