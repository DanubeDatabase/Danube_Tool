import pandas as pd
import numpy as np

from config_show import print_log
from category_mapping.map_reference.shared_ref import dataframe_to_dictionary, PATH_REF_FOLDER


def usage_option1(df, PATH_REF_FOLDER):
    """Defines the usage from 2 variables in the layer 'BATIMENT' from the BDTOPO"""
    # Independent files which describes the relation between the categories in BDTOPO BATIMENT and Danube
    path_association_usage_bati = PATH_REF_FOLDER / "associations_bati_usage1_nature_usage_danube.xlsx"
    usage_bati_association = pd.read_excel(path_association_usage_bati)
    usage1_topo_map_dict = dataframe_to_dictionary(usage_bati_association, "USAGE1", "ASSOCIATION_USAGE1_DAN")
    print_log("\nusage1_topo_map_dict :", usage1_topo_map_dict)
    nature_topo_map_dict = dataframe_to_dictionary(usage_bati_association, "NATURE", "ASSOCIATION_NATURE_DAN")
    print_log("\nnature_topo_map_dict :", nature_topo_map_dict)

    df['usage_bati_conv'] = df.topo_USAGE1.map(usage1_topo_map_dict)
    df['nature_bati_conv'] = df.topo_NATURE.map(nature_topo_map_dict)

    df['usage_option1'] = df['usage_bati_conv'].fillna(df['nature_bati_conv'])


def usage_option2(df, PATH_REF_FOLDER):
    """Defines the usage from 1 variable in the layer 'ZONE DE ACTIVITE' from the BDTOPO"""
    path_association_nature_activ = PATH_REF_FOLDER / "associations_activ_nature_usage_danube.xlsx"
    nature_bati_association = pd.read_excel(path_association_nature_activ)
    nature_activ_map_dict = dataframe_to_dictionary(nature_bati_association, "NATURE", "Association_Danube")
    print_log("\nnature_activ_map_dict :", nature_activ_map_dict)

    df['usage_option2'] = df.activ_NATURE.map(nature_activ_map_dict)


def usage_option3(df):
    print_log('\n_____Calculation of populational density_____')
    ### Calculate the populational density of the filosofi squares
    # groupby filosofi square
    gb = df.groupby('filo_Idcar_nat')
    # calculate populational density
    df['dens_pers_m2build'] = df['filo_Ind'] / gb['FLOOR_AREA'].transform('sum')
    # Set the values of 'dens_pers_m2build' for building without a filosofi squares with 0
    df.dens_pers_m2build = df.dens_pers_m2build.fillna(0)
    print_log(df.sort_values("filo_Idcar_nat")[["filo_Idcar_nat", "filo_Ind", "FLOOR_AREA", "dens_pers_m2build"]])

    ### Classify the density
    # redo groupby filosofi square to include 'dens_pers_m2build' values
    gb = df.groupby('filo_Idcar_nat')
    # order groups by 'dens_pers_m2build'
    dens_pers_m2build_gb_sorted = gb['dens_pers_m2build'].mean().sort_values()
    # Classify the 'dens_pers_m2build' by percentual ascending order provide a mapping dictionnary
    dens_quantile = (dens_pers_m2build_gb_sorted.reset_index().index + 1) / len(gb)
    map_dens_quantile = dict(zip(list(dens_pers_m2build_gb_sorted.index), dens_quantile))
    print_log('\nmap_dens_quantile \n', map_dens_quantile)
    # Map the order in the original df data
    df["dens_quantile"] = df.filo_Idcar_nat.map(map_dens_quantile)
    df.dens_quantile = df.dens_quantile.fillna(0)
    print_log(df.sort_values("dens_pers_m2build")[["filo_Idcar_nat", "dens_pers_m2build", "dens_quantile"]])

    print_log('\n_____Definition of usage option 3_____')

    # to define threshold of populational density quantile to distinguish between 'habitat' and 'tertiaire'
    threshold = 0.25

    df['usage_option3'] = np.where(df['dens_quantile'] > threshold,
                                   'habitat', 'tertiaire')

    df['usage_option3'] = np.where(df['typology_map'] == 'P', 'habitat', df['usage_option3'])

    df['usage_option3'] = np.where(df['typology_map'] == 'BA', 'bâtiment industriel', df['usage_option3'])


def main_cm_usage(df, PATH_REF_FOLDER):
    print_log("*" * 100)
    print_log("Run category_mapping - main_cm_usage : mapping Danube usage")
    print_log("*" * 100)

    print_log("Before map usage- df.head() \n", df.head())
    print_log("df.columns ", df.columns)

    usage_option1(df, PATH_REF_FOLDER)
    print_log("\nAfter map usage1 \n", df[['topo_USAGE1', 'topo_NATURE', 'usage_option1']])
    print_log("df.columns ", df.columns)

    usage_option2(df, PATH_REF_FOLDER)
    print_log("\nAfter map usage2 \n", df[['activ_NATURE', 'usage_option2']])
    print_log("df.columns ", df.columns)

    usage_option3(df)
    print_log("\nAfter define usage3  \n", df[['dens_quantile', 'usage_option3']])
    print_log("df.columns ", df.columns)

    # Choose the final usage
    df['usage_map'] = df['usage_option1'].fillna(
        df['usage_option2']).fillna(
        df['usage_option3'])

    df['usage_source'] = df.apply(lambda row: 'topo_bati' if pd.notnull(row['usage_option1']) else
    ('topo_activ' if pd.notnull(row['usage_option2']) else 'dens_pers_m2build'),
                                  axis=1)

    df['usage_quality'] = df.apply(lambda row: 'A' if pd.notnull(row['usage_option1']) else
    ('B' if pd.notnull(row['usage_option2']) else 'C'),
                                   axis=1)

    print_log("\nAfter define final usage  \n", df[['typology_map', 'usage_map', 'usage_source', 'usage_quality']])

    print_log("df.columns ", df.columns)

    return df
