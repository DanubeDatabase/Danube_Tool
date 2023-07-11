import pandas as pd
import numpy as np

from config_show import print_log, timed_execution
from category_mapping.map_reference.shared_ref import dataframe_to_dictionary, PATH_DANUBE_TABLES_FOLDER


def test_different_territory_comm_dept(df):
    """test if different territory in department and commune level"""
    df['territory_comm'] = df['territory_comm'].replace('nan', float('nan'))
    set_terr_comm = set(df.territory_comm.dropna().unique())
    print_log('Possible territories in commune', set_terr_comm)

    df['territory_dept'] = df['territory_dept'].replace('nan', float('nan'))
    set_terr_dept = set(df.territory_dept.dropna().unique())
    print_log('Possible territories in dept', set_terr_dept)

    if set_terr_comm == set_terr_dept:
        different_comm_dept = False
    else:
        different_comm_dept = True
    print_log("\ndifferent_comm_dept: ", different_comm_dept)

    return different_comm_dept


def get_dict_to_map_archetype_danube(path_danube_folder):
    """provide mapping dictionary for danube archetypes"""
    path_dan = path_danube_folder / "CATALOGUE-export.csv"
    dan = pd.read_csv(path_dan)
    dan['archetype_long'] = dan['USAGE'] + '-' + dan['NOM_TYPOLOGIE'] + '-' + dan['NUMERO_PERIODE'] + '-' + dan[
        'TERRITOIRE']
    mapping_dict = dataframe_to_dictionary(dan, "archetype_long", "ID_ARCHETYPE")
    return mapping_dict


def get_danube_archs_in_df(df, mapping_id_arch, location="dept"):
    # location  :  'comm' or 'dept'

    # archetype from concatenation of 4 danube entries
    df['usage_danube'] = df['usage_danube'].astype(str)
    df['typology_danube'] = df['typology_danube'].astype(str)
    df['period_danube'] = df['period_danube'].astype(str)

    nom_territory = f"territory_{location}"
    nom_archetype = f"arch_{location}"

    df[nom_territory] = df[nom_territory].astype(str)
    df[nom_archetype] = df['usage_danube'] + '-' + df['typology_danube'] + '-' + df['period_danube'] + '-' + df[
        nom_territory]

    print_log(df[[nom_archetype,
                  'usage_danube', 'typology_danube', 'period_danube', 'territory_dept', 'territory_comm']].head(2))

    # archetype if the territory is FRANCE
    nom_france_level = f"arch_{location}_if_france_level"
    df[nom_france_level] = df[nom_archetype].str.split('FRANCE').str[0] + 'FRANCE'

    # archetype if the territory is FRANCE_PIERRE_ARDOISE
    nom_pierre_ardoise = f"arch_{location}_if_pier_ard"
    df[nom_pierre_ardoise] = np.where(
        (df['territory_dept'].str.contains('PIERRE') & df['territory_dept'].str.contains('ARDOISE')),
        df[nom_archetype].str.split('PIERRE').str[0] + 'PIERRE_ARDOISE',
        np.nan)

    nom_archetype_loc_id = f"arch_{location}_id"
    df[nom_archetype_loc_id] = df[nom_archetype].map(mapping_id_arch).fillna(
        df[nom_france_level].map(mapping_id_arch)).fillna(
        df[nom_pierre_ardoise].map(mapping_id_arch))


def main_archetype(df, PATH_DANUBE_TABLES_FOLDER):
    print_log("*" * 100)
    print_log("Run archetype danube")
    print_log("*" * 100)

    mapping_id_arch = get_dict_to_map_archetype_danube(PATH_DANUBE_TABLES_FOLDER)

    get_danube_archs_in_df(df, mapping_id_arch, location='dept')
    # test if different territory in department and commune level
    different_comm_dept = test_different_territory_comm_dept(df)

    if different_comm_dept:
        get_danube_archs_in_df(df, mapping_id_arch, location='comm')
    else:
        df['arch_comm'] = df['arch_dept']
        df['arch_comm_id'] = df['arch_dept_id']

    print_log('\nArchetype dept id (%) \n', df.arch_dept_id.value_counts(normalize=True, dropna=False) * 100)

    print_log('\nArchetypes dept without corresponding category in danube '
              '(% of null before generalization)\n',
              df[df.arch_dept_id.isnull()]['arch_dept'].value_counts(normalize=True, dropna=False) * 100)
