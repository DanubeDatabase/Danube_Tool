import pandas as pd
import numpy as np
from config_show import print_log


def year_option1(df):
    """Converts date from 'topo_DATE_APP' into year"""
    df['year_option1'] = df.apply(lambda row: int(row['topo_DATE_APP'][:4]) if pd.notnull(row['topo_DATE_APP']) else np.nan, axis=1)

def year_option2(df):
    """Calculates the mean year in the rsu"""
    gb = df.groupby('ID_RSU')
    df['year_option2'] = gb['year_option1'].transform('mean')
    df['year_option2'] = df['year_option2'].round()


def year_option3(df):
    """Converts filosofi main construction period into a year corresponding to a period in Danube"""
    period_filo = ['filo_Log_av45', 'filo_Log_45_70', 'filo_Log_70_90', 'filo_Log_ap90']
    year_association = [1944, 1958, 1982, 2001]
    map_filo_year = dict(zip(period_filo, year_association))
    print(map_filo_year)
    df['max_filo_perc_year'] = df[period_filo].idxmax(axis=1)
    df['year_option3'] = df['max_filo_perc_year'].map(map_filo_year)

def main_cm_period(df):
    print_log("*" * 100)
    print_log("Run category_mapping - main_cm_period : mapping Danube period")
    print_log("*" * 100)

    print_log("Before map YEAR - df.head() \n",df.head())
    print_log("df.columns ",df.columns)

    year_option1(df)
    print_log("\nAfter map year_1 \n",  df[['topo_DATE_APP','year_option1']])
    print_log("df.columns ",df.columns)

    year_option2(df)
    print_log("\nAfter map year_2 \n",df[['ID_RSU', 'topo_DATE_APP','year_option2']])
    print_log("df.columns ",df.columns)

    year_option3(df)
    print_log("\nAfter define year_3  \n",df[['max_filo_perc_year','year_option3']])
    print_log("df.columns ",df.columns)


    # Choose the final year
    df['year_map'] = df['year_option1'].fillna(
                                             df['year_option2']).fillna(
                                                                     df['year_option3'])

    df['year_source'] = df.apply(lambda row: 'topo_bati' if pd.notnull(row['year_option1']) else
                                             ('topo_bati' if pd.notnull(row['year_option2']) else 'filosofi'),
                                                axis=1)

    df['year_quality'] = df.apply(lambda row: 'A' if pd.notnull(row['year_option1']) else
                                                ('B' if pd.notnull(row['year_option2']) else 'C'),
                                                 axis=1)

    print_log("\nAfter define final year  \n",df[['year_map','year_source', 'year_quality']])
    print_log("df.columns ",df.columns)

    return(df)