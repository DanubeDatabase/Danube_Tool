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

__author__ =  'Serge Faraut, Lorena de Carvalho Araujo - (C) LRA - ENSA Toulouse / LMDC - INSA Toulouse / LISST - UT2J'
__date__ = '2023-06-15'
__copyright__ = '(C) 2023 by (C) LRA - ENSA Toulouse / LMDC - INSA Toulouse / LISST - UT2J'
__version__ = 'v0.9b'
__all__ = [
]

#from .DANUBE_constants import OUTPUT,FILOSOFI,GEOCLIMATE_INPUT_BUILDINGS_UTRF
from .DANUBE_config import DEBUG
from .DANUBE_config import OUTPUT,FILOSOFI,GEOCLIMATE_INPUT_BUILDINGS_UTRF
from .DANUBE_config import DANUBE_LAYERS