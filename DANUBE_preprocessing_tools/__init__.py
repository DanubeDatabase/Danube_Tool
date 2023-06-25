# -*- coding: utf-8 -*-

"""
/***************************************************************************
 DANUBE preprocessing tools
        Match Danube archetypes with BDTOPO buildings of a city.
        -------------------
        begin                : 2023-04-29
        author               : Lorena de Carvalho Araujo - LRA - ENSA Toulouse
        maintainer           : Serge Faraut - LRA - ENSA Toulouse
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

__author__ = 'Lorena de Carvalho Araujo - (C) LRA - ENSA Toulouse / LMDC - INSA Toulouse / LISST - UT2J'
__maintainer__ = 'Serge Faraut - (C) LRA - ENSA Toulouse / LMDC - INSA Toulouse / LISST - UT2J'
__date__ = '2023-06-19'
__copyright__ = '(C) 2023 by (C) LRA - ENSA Toulouse / LMDC - INSA Toulouse / LISST - UT2J'
__version__ = 'v0.0.7'
__all__ = [
    "preprocess_function_sample", "preprocess_function_launch", 
    "open_layer", "check_validity",
]

#from .DANUBE_constants import OUTPUT,FILOSOFI,GEOCLIMATE_INPUT_BUILDINGS_UTRF
from .danube_preprocess_sample import preprocess_function_sample
from .danube_preprocess_launch import preprocess_function_launch
from .pt_basic_functions import open_layer, check_validity