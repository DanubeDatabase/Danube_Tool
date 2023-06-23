# -*- coding: utf-8 -*-

"""
/***************************************************************************
 PyDANUBE
        A Python Library for managing DANUBE Database
 DANUBE Database allows you to generate buildings' material informations from urban scale typomorphological informations (IGN BDTOPO and/or Geoclimate tool's outputs) 
        -------------------
        begin                : 2023-04-29
        author               : Serge Faraut - LRA - ENSA Toulouse
        copyright            : (C) 2023 by (C) LRA - ENSA Toulouse / LMDC - INSA Toulouse / LISST - UT2J
        email                : lra-tech@toulouse.archi.fr
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

__all__ = [
    'DANUBE_database',
]

import pandas as pd
import numpy as np
import shutil
import time
import os
import tempfile

# Define DANUBE Database class

# Default DANUBE database local folder path (relative)
DEFAULT_DANUBE_PATH = 'DANUBE_database'
## All DANUBE database table id names (and path) - stored in a static global dictionnary
# DEFAULT_DANUBE_DATA_TABLES = ('CATALOGUE', 'DISPOSITIF_TOITS','DISPOSITIFS_MUR','PERIODES','PLANCHERS','ROUTES','TERRITOIRES_PERIODES','TERRITOIRES','TYPOLOGIES','USAGES','VENTILATION')
DEFAULT_DANUBE_DATA_TABLES = { 
        'CATALOGUE' : 'CATALOGUE-export',
        'DISPOSITIF_TOITS' : 'DISPOSITIF_TOITS-export',
        'DISPOSITIFS_MUR' : 'DISPOSITIFS_MUR-export',
        'PERIODES' : 'PERIODES-export',
        'PLANCHERS' : 'PLANCHERS-export','ROUTES' : 'ROUTES-export',
        'TERRITOIRES_PERIODES_DEPARTEMENT' : 'TERRITOIRES_PERIODES-DEPT-V4-export',
        'TERRITOIRES_PERIODES_COMMUNE' : 'TERRITOIRES_PERIODES-COMMUNE-V5-export',
        'TERRITOIRES' : 'TERRITOIRES-export',
        'TYPOLOGIES' : 'TYPOLOGIES-export',
        'RENOVATION-complete_study': 'RENOVATION-complete_study',
        'RENOVATION-distribution_not_renovated_part' : 'RENOVATION-distribution_not_renovated_part',
        'RENOVATION-distribution_renovated_part' :'RENOVATION-distribution_renovated_part',
        'RENOVATION-distribution_whole' : 'RENOVATION-distribution_whole',
        'RENOVATION-limits_percentages' : 'RENOVATION-limits_percentages',
        'RENOVATION-metadata' : 'RENOVATION-metadata',
        'USAGES' : 'USAGES-export',
        'VENTILATION' : 'VENTILATION-export'}

class DANUBE_database:
    
    __author__ =  'Serge Faraut, Lorena de Carvalho Araujo - (C) LRA - ENSA Toulouse / LMDC - INSA Toulouse / LISST - UT2J'
    __date__ = '2023-04-19'
    __version__ = '0.0.6'
    
    __copyright__ = '(C) 2023 by (C) LRA - ENSA Toulouse / LMDC - INSA Toulouse / LISST - UT2J'
    def __init__(self, path=''):
        if (path !=''):
            self.path = path 
        else:
            #self.path = DEFAULT_DANUBE_PATH
            self.path = os.path.join(os.path.dirname(__file__), DEFAULT_DANUBE_PATH)
        self.DANUBE_tables = {}
        self.DANUBE_database_extended = pd.DataFrame() ### Empty Dataframe
        self.DANUBE_database_generalized = pd.DataFrame() ### Empty Dataframe
        return
    
    # DANUBE_load_database_core() : load DANUBE_core data (all data tables)
    # Read all DANUBE tables (CATALOGUE, DISPOSITIF_TOITS, DISPOSITIFS_MUR, PERIOD, ...)
    def DANUBE_load_database_core(self):
        if self.path == '':
            danube_data_path =  os.path.join(os.path.dirname(__file__), DEFAULT_DANUBE_PATH)
        else:
            danube_data_path = self.path
        print("Current Database path:"+danube_data_path)
        for table_name, table_path in DEFAULT_DANUBE_DATA_TABLES.items():
        #for table_name in DEFAULT_DANUBE_DATA_TABLES:
            #process reading table
            cvs_filename = os.path.join(danube_data_path, table_path+'.csv')
            print("Reading DANUBE table:"+table_name+" from filename:"+cvs_filename)
            df = pd.read_csv(cvs_filename)
            self.DANUBE_tables[table_name] = df
        return
    
    # Generate DANUBE_extended database containing all data joined from all separate tables (one consolidated table form)
    def DANUBE_generate_extended(self):
        ### Make join between tables using merges on rigth keys
        database_ref = self.DANUBE_tables['CATALOGUE']
        database_disp_toits = self.DANUBE_tables['DISPOSITIF_TOITS']
        database3 = database_disp_toits.add_suffix('_T1')
        merged = pd.merge(database_ref, database3, how='left', left_on=['DISPOSITIF_TOIT_OPTION1'], right_on=['DISPOSITIF_T1'])
        #merged.rename(columns={'DISPOSITIF_1':'DISPOSITIF_T1'}, inplace=True)
        
        database3 = database_disp_toits.add_suffix('_T2')
        merged = pd.merge(merged, database3, how='left', left_on=['DISPOSITIF_TOIT_OPTION2'], right_on=['DISPOSITIF_T2'])
        #merged.rename(columns={'DISPOSITIF_2':'DISPOSITIF_T2'}, inplace=True)
        
        database_disp_murs = self.DANUBE_tables['DISPOSITIFS_MUR']
        database3 = database_disp_murs.add_suffix('_M1')
        merged = pd.merge(merged, database3, how='left', left_on=['DISPOSITIF_MUR_OPTION1'], right_on=['DISPOSITIF_M1'])
        #merged.rename(columns={'DISPOSITIF_1':'DISPOSITIF_M1'}, inplace=True)
        
        database3 = database_disp_murs.add_suffix('_M2')
        merged = pd.merge(merged, database3, how='left', left_on=['DISPOSITIF_MUR_OPTION2'], right_on=['DISPOSITIF_M2'])
        #merged.rename(columns={'DISPOSITIF_2':'DISPOSITIF_M2'}, inplace=True)
        
        database3 = database_disp_murs.add_suffix('_M3')
        merged = pd.merge(merged, database3, how='left', left_on=['DISPOSITIF_MUR_OPTION2'], right_on=['DISPOSITIF_M3'])
        #merged.rename(columns={'DISPOSITIF_3':'DISPOSITIF_M3'}, inplace=True)
        
        self.DANUBE_database_extended = merged
        return
    
    # Export DANUBE Extended Database to CSV File (to temporary file)
    def DANUBE_export_extended_database(self, f_name=''):
        if ( f_name == ''): # Generate a temporary output file for CSV
            f = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
            f_name = f.name
        print('Exporting DANUBE Extended Database to :'+ f_name)
        self.DANUBE_database_extended.to_csv(f_name, sep=',', encoding='utf-8', index=False)
        return f_name
    
    # Export DANUBE Generalized Database to CSV File (to temporary file)
    def DANUBE_export_generalized_database(self, f_name=''):
        if ( f_name == ''): # Generate a temporary output file for CSV
            f = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
            f_name = f.name
        print('Exporting DANUBE Extended Database to :'+ f_name)
        self.DANUBE_database_generalized.to_csv(f_name, sep=',', encoding='utf-8', index=False)
        return f_name

    # Generate DANUBE generalized data version (defining an archetype for all input values PERIOD, USAGE, TYPOLOGY, TERRITORY)
    # Using generalization rules based on PERIOD, USAGE, TYPOLOGY, TERRITORY
    def DANUBE_generate_generalized(self):
        ### TODO Uses rules - Currently using Extended Database
        if self.DANUBE_database_extended.empty:
            self.DANUBE_generate_extended()
        self.DANUBE_database_generalized = self.DANUBE_database_extended
        return
    
    # Load DANUBE Database with all data and informations (Extended and Generalized data)
    def DANUBE_load_database(self):
        # Read data from self.path
        self.DANUBE_load_database_core()
        # Generate DANUBE_extended (one table form)
        self.DANUBE_generate_extended()
        # Generate DANUBE_generalizd (Generalized version for all input values PERIOD, USAGE, TYPOLOGY, TERRITORY)
        self.DANUBE_generate_generalized()
        return
    
    # Return DANUBE period from building's construction date
    def DANUBE_get_period_from_date(self, construct_date = '2023'):
        danube_construction_period = 'P7'
        period_df = self.DANUBE_tables["PERIODES"]
        construct_date_int = int(construct_date)
        df2 = period_df.loc[(period_df['DATE_DEBUT']<=construct_date_int) & (period_df['DATE_FIN']>=construct_date_int)]['PERIODE']
        if not df2.empty:
            danube_construction_period = df2.values[0]
        else:
            print("Warning: ", construct_date, ' is not defined in DANUBE. Default P7 period used')
        return danube_construction_period
    
    # Return DANUBE Material Territory from building's location (at DEPARTEMENT or COMMUNE scale) and Period
    # Territory is distinct for P1 period and P2-P7 period
    def DANUBE_get_territory(self, building_location = '31', construction_period = 'P7', scale='DEPARTEMENT'):
        danube_territory = 'FRANCE'
        if scale == 'DEPARTEMENT': ### Use TERRITOIRES_PERIODES_DEPARTEMENT table
            territoires_periodes = self.DANUBE_tables["TERRITOIRES_PERIODES_DEPARTEMENT"]
            territoire = territoires_periodes.loc[territoires_periodes['INSEE_DEP'] == building_location]
            if not territoire.empty:
                if construction_period == 'P1':
                    danube_territory = territoire['Terr_P1'].values[0]
                else:
                    ### All other P2-P7 Territories
                    danube_territory = territoire['Terr_P2'].values[0]
            else:
                print("Warning: territory for Period ",  construction_period, ' and Location DEPT: ', building_location, ' is not defined in DANUBE. Default territory FRANCE used')
        elif scale == 'COMMUNE': ### Use TERRITOIRES_PERIODES-COMMUNE table
            territoires_periodes = self.DANUBE_tables["TERRITOIRES_PERIODES_COMMUNE"]
            territoire = territoires_periodes.loc[territoires_periodes['INSEE_COM'] == building_location]
            if not territoire.empty:
                if construction_period == 'P1':
                    danube_territory = territoire['Terr_P1'].values[0]
                else:
                    ### All other P2-P7 Territories
                    danube_territory = territoire['Terr_P2'].values[0]
            else:
                print("Warning: territory for Period ",  construction_period, ' and Location COMMUNE: ', building_location, ' is not defined in DANUBE. Default territory FRANCE used')
             #  print('Error in DANUBE_get_territory: Territory\'s commune scale not yet implemented')
        else:
            print('Error in DANUBE_get_territory: ',scale,' scale is unknown... Returning default FRANCE territory.')
        return danube_territory
    
    # Get DANUBE core archetype (only from Catalogue) from 4 main variables NOM_TYPOLOGIE, USAGE, CONSTRUCTION_DATE, LOCATION.
    # And optional input scale 'DEPARTEMENT' (default) or 'COMMUNE'.
    def DANUBE_get_core_archetype(self, Nom_typologie="P", Usage="HABITAT", Construction_date="2023", Location="31", scale='DEPARTEMENT'):
        danube_archetype="HAB_P_P7_TF" # Default value
        danube_archetypes_all = self.DANUBE_tables["CATALOGUE"]
        periode  = self.DANUBE_get_period_from_date(Construction_date) # Get Period
        territoire = self.DANUBE_get_territory(Location, periode, scale)      # Get Territory
        # Fetch archetype data from CATALOGUE
        archetype = danube_archetypes_all.loc[ (danube_archetypes_all['NOM_TYPOLOGIE'] == Nom_typologie) & (danube_archetypes_all['USAGE'] == Usage) &
            (danube_archetypes_all['NUMERO_PERIODE'] == periode) & (danube_archetypes_all['TERRITOIRE'] == territoire)]
        if not archetype.empty:
            danube_archetype = archetype['ID_ARCHETYPE'].values[0]
        else:
            print("Warning: Archetype for Period ",  construction_period, ' and Location DEPT: ', building_location, ' is not defined in DANUBE. Default Archetype ',danube_archetype, 'is used')
        return danube_archetype
    
    #Get All DANUBE's archetype informations 
    def DANUBE_get_archetype_informations(self, id_archetype="HAB_P_P7_TF"):
        infos = pd.DataFrame() ### Empty Dataframe
        danube_all_archetypes_info = self.DANUBE_database_extended
        if danube_all_archetypes_info.empty:
            print('DANUBE extended database is empty. Cannot get informations for archetypes :' + id_archetype + '...')
            return infos
        infos_rows = danube_all_archetypes_info.loc[(danube_all_archetypes_info['ID_ARCHETYPE'] == id_archetype)]
        if not infos_rows.empty:
            infos = infos_rows # Dataframe! Get individual values with column index. Ex: infos_rows['NUMERO_PERIODE'].values[0]
        else:
            print('Warning: Archetype ' + id_archetype+' is not defined in DANUBE.')
        return infos

if __name__ == '__main__':
    print("DANUBE_database " + __version__)
