import logging
from datetime import datetime
from pathlib import Path
import processing
from qgis.core import QgsField, QgsProject, QgsVectorLayer, QgsVectorLayerJoinInfo
import pandas as pd

from dev_set_test import DEV_TEST, print_d, print_fields_d
if DEV_TEST:
    from dev_set_test import DANUBE_LAYERS
else:
    from DANUBE_config import DANUBE_LAYERS

def main_dc_4(DANUBE_LAYERS):
    print("*" * 100)
    print("Run step 4 of data consolidation : Spatially join TOPO_ACTIVITE and FILOSOFI to the building layer")
    print("*" * 100)

    print('TODO')
