# -*- coding: utf-8 -*-

"""
/***************************************************************************
 DANUBEtool
                                 A QGIS plugin
 DANUBE Tool plugin allows you to generate spatialized buildings' material informations from DANUBE database and urban scale typomorphological informations (IGN BDTOPO data and Geoclimate tool's outputs)  
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2023-03-31
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
__all__ = ["DANUBE_LAYERS"]

__author__ = 'Serge Faraut - (C) LRA - ENSA Toulouse'
__date__ = '2023-06-19'
__copyright__ = '(C) 2023 by (C) LRA - ENSA Toulouse / LMDC - INSA Toulouse / LISST - UT2J'

OUTPUT = 'OUTPUT'
INPUT = 'INPUT'
INPUT_BUILDINGS = 'INPUT_BUILDINGS'
INPUT_PREPROCESSED = 'INPUT_PREPROCESSED'
GEOCLIMATE_INPUT_BUILDINGS_UTRF = 'GEOCLIMATE_INPUT_BUILDINGS_UTRF'
FILOSOFI = 'FILOSOFI'

DANUBE_LAYERS = {
    "TOPO_BATI" : { "id": "TOPO_BATI" , "file_id": "BATIMENT.shp", "type" : "INPUT", "layer" : None },
    "TOPO_ACTIVITE" : { "id": "TOPO_ACTIVITE", "file_id": "ZONE_D_ACTIVITE_OU_D_INTERET.shp", "type" : "INPUT", "layer" : None } ,
    "GEO_RSU_UTRF_FLOOR_AREA" : { "id": "GEO_RSU_UTRF_FLOOR_AREA", "file_id": "rsu_utrf_floor_area.geojson", "type" : "INPUT", "layer" : None } ,
    "GEO_BUILD_URTF" : { "id": "GEO_BUILD_URTF", "file_id": "building_utrf.geojson", "type" : "INPUT", "layer" : None } ,
    "GEO_ZONE" : { "id": "GEO_ZONE", "file_id": "zone.geoson", "type" : "INPUT", "layer" : None } ,
    "GEO_BUILD_IND" : { "id": "GEO_BUILD_IND", "file_id": "building_indicators.geojson", "type" : "INPUT", "layer" : None } ,
    "DANUBE_FILO" : { "id": "FILO", "file_id": "Filosofi2017_carreaux_nivNaturel_met.shp", "type" : "INPUT", "layer" : None } ,
    "DANUBE_BUILD_PREPROCESS" : { "id": "DANUBE_BUILD_PREPROCESS", "file_id": "DANUBE_building_preprocessed.dpkg", "type" : "OUTPUT", "layer" : None } ,
    "DANUBE_BUILD_DATA" : { "id": "DANUBE_BUILD_DATA", "file_id": "DANUBE_building_data.dpkg", "type" : "OUTPUT", "layer" : None } ,
}