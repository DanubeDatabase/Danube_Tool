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

# Default DANUBE database local path (relative)
DEFAULT_DANUBE_PATH = '.DANUBE_database'
## All DANUBE database table names
DEFAUL_DANUBE_DATA_TABLES = ('CATALOGUE', 'DISPOSITIF_TOITS','DISPOSITIFS_MUR','PERIODES','PLANCHERS','ROUTES','TERRITOIRES_PERIODES','TERRITOIRES','TYPOLOGIES','USAGES','VENTILATION')

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
        return
    
    # DANUBE_load_database_core() : load DANUBE_core (tables)
    # Read all DANUBE tables (CATALOGUE, DISPOSITIF_TOITS, DISPOSITIFS_MUR, PERIOD, ...)
    def DANUBE_load_database_core(self):
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

if __name__ == '__main__':
    print("DANUBE_database " + __version__)
