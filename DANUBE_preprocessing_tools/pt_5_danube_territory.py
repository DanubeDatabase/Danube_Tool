import logging
from datetime import datetime
from pathlib import Path
import processing
from qgis.core import QgsField, QgsProject, QgsVectorLayer, QgsVectorLayerJoinInfo
import pandas as pd

from pt_basic_functions import DEBUG

def main_5():
    print("#" * 60)
    print("Run main 5 : Territory definition")
    print("#" * 60)
