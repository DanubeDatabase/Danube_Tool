# -*- coding: utf-8 -*-

"""
/***************************************************************************
 DANUBE processing tools
        Match Danube archetypes with BDTOPO buildings of a city.
        -------------------
        begin                : 2023-04-29
        author               : Lorena de Carvalho Araujo, Serge Faraut - LRA - ENSA Toulouse
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

__author__ = 'Lorena de Carvalho Araujo, Serge Faraut - (C) LRA - ENSA Toulouse'
__maintainer__ = 'Serge Faraut - (C) LRA - ENSA Toulouse'
__date__ = '2023-06-19'
__copyright__ = '(C) 2023 by (C) LRA - ENSA Toulouse / LMDC - INSA Toulouse / LISST - UT2J'
__version__ = 'v0.9b'
__all__ = [
    "process_function_sample", "process_function_launch", "process_function_launch",
]

#from .DANUBE_constants import OUTPUT,FILOSOFI,GEOCLIMATE_INPUT_BUILDINGS_UTRF
from .danube_process_sample import process_function_sample
from .danube_process_launch import process_function_launch
from .danube_process_launch_old import process_function_launch