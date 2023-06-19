import logging
from datetime import datetime
from pathlib import Path
import processing
from qgis.core import QgsField, QgsProject, QgsVectorLayer, QgsVectorLayerJoinInfo
import pandas as pd

from pt_basic_functions import DEBUG

def main_2():
    print("\n")
    print("#" * 60)
    print("Run main 2 : Period definition")
    print("#" * 60)
