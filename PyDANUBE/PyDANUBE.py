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

# Define DANUBE Database class

# Default DANUBE database local folder path (relative)
DEFAULT_DANUBE_PATH = 'DANUBE_database'
## All DANUBE database table names
DEFAULT_DANUBE_DATA_TABLES = ('CATALOGUE', 'DISPOSITIF_TOITS','DISPOSITIFS_MUR','PERIODES','PLANCHERS','ROUTES','TERRITOIRES_PERIODES','TERRITOIRES','TYPOLOGIES','USAGES','VENTILATION')

class DANUBE_database:
    
    __author__ = 'Serge Faraut - (C) LRA - ENSA Toulouse / LMDC - INSA Toulouse / LISST - UT2J'
    __date__ = '2023-04-19'
    __version__ = '0.0.1'
    __copyright__ = '(C) 2023 by (C) LRA - ENSA Toulouse / LMDC - INSA Toulouse / LISST - UT2J'
    
    def __init__(self, path=''):
        if (path !=''):
            self.path = path 
        else:
            self.path = DEFAULT_DANUBE_PATH
        self.DANUBE_tables = {}
        return
    
    # DANUBE_load_database_core() : load DANUBE_core (tables)
    # Read all DANUBE tables (CATALOGUE, DISPOSITIF_TOITS, DISPOSITIFS_MUR, PERIOD, ...)
    def DANUBE_load_database_core(self):
        danube_data_path =  os.path.join(os.path.dirname(__file__), DEFAULT_DANUBE_PATH)
        print("Current Database path:"+danube_data_path)
        for table_name in DEFAULT_DANUBE_DATA_TABLES:
            #process reading table
            cvs_filename = os.path.join(danube_data_path, table_name+'-export.csv')
            print("Reading DANUBE table:"+table_name+" filename:"+cvs_filename)
            df = pd.read_csv(cvs_filename)
            self.DANUBE_tables[table_name] = df
        return
    
    # Generate DANUBE_extended (one table form)
    def DANUBE_generate_extended(self):
        return
    
    # Generate DANUBE_generalized (généralized version for all input values PERIOD, USAGE, TYPOLOGY, TERRITORY)
    def DANUBE_generate_generalized(self):
        return
    
    def load_database(self):
        # Read data from self.path
        DANUBE_load_database_core(self)
        # Generate DANUBE_extended (one table form)
        DANUBE_generate_extended(self)
        # Generate DANUBE_generalizd (généralized version for all input values PERIOD, USAGE, TYPOLOGY, TERRITORY)
        DANUBE_generate_generalized(self)
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
    
    # Return DANUBE Material Territory from building's location (DEPARTEMENT) and Period - TODO: Use same at commune's scale
    # Territory is distinct for P1 period and P2-P7 period
    def DANUBE_get_territory(self, building_location = '31', construction_period = 'P7'):
        danube_territory = 'FRANCE'
        territoires_periodes = self.DANUBE_tables["TERRITOIRES_PERIODES"]
        territoire = territoires_periodes.loc[territoires_periodes['CODE_DEPT'] == building_location]
        if not territoire.empty:
            if construction_period == 'P1':
                danube_territory = territoire['TERR_P1'].values[0]
            else:
                ### All other P2-P7 Territories
                danube_territory = territoire['TERR_P2-P7'].values[0]
        else:
            print("Warning: territory for Period ",  construction_period, ' and Location DEPT: ', building_location, ' is not defined in DANUBE. Default territory FRANCE used')
        return danube_territory
    
    # Get DANUBE core archetype (only from Catalogue) from 4 main variables NOM_TYPOLOGIE, USAGE, CONSTRUCTION_DATE, LOCATION
    def DANUBE_get_core_archetype(self, Nom_typologie="P", Usage="HABITAT", Construction_date="2023", Location="31"):
        danube_archetype="HAB_P_P7_TF" # Default value
        danube_archetypes_all = self.DANUBE_tables["CATALOGUE"]
        periode  = self.DANUBE_get_period_from_date(Construction_date) # Get Period
        territoire = self.DANUBE_get_territory(Location, periode)      # Get Territory
        # Fetch archetype data from CATALOGUE
        archetype = danube_archetypes_all.loc[ (danube_archetypes_all['NOM_TYPOLOGIE'] == Nom_typologie) & (danube_archetypes_all['USAGE'] == Usage) &
            (danube_archetypes_all['NUMERO_PERIODE'] == periode) & (danube_archetypes_all['TERRITOIRE'] == territoire)]
        if not archetype.empty:
            danube_archetype = archetype['NUMERO_TYPOLOGIE'].values[0]
        else:
            print("Warning: Archetype for Period ",  construction_period, ' and Location DEPT: ', building_location, ' is not defined in DANUBE. Default Archetype ',danube_archetype, 'is used')
        return danube_archetype

if __name__ == '__main__':
    print("DANUBE_database " + __version__)
