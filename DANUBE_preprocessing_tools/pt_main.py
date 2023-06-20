import logging
import time
from pathlib import Path
from qgis.core import QgsField, QgsProject, QgsVectorLayer, QgsVectorLayerJoinInfo
from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (Qgis,
                        QgsFeature,
                        QgsPoint,
                        QgsMessageLog,
                        QgsProcessing,
                        QgsFeatureSink,
                        QgsProcessingAlgorithm,
                        QgsProcessingParameterVectorDestination,
                        QgsProcessingParameterFile,
                        QgsProcessingParameterFeatureSource,
                        QgsProcessingParameterFeatureSink,
                        QgsProcessingParameterNumber,
                        QgsVectorLayer,
                        NULL
                       )
from PyQt5.QtCore import QVariant

import pandas as pd
import processing


from pt_1_initial_optimisation import main_1
from pt_2_danube_period import main_2
from pt_3_danube_typology import main_3
from pt_4_danube_usage import main_4
from pt_5_danube_territory import main_5
from pt_6_danube_archetype import main_6

# Follow the order developped in :
# https://docs.google.com/drawings/d/1A_RSbMU7G51n4TFwySDuVVkwZCd7xmHw1BfBvAM8XMU/edit
# https://docs.google.com/drawings/d/1HNO0qaXbwr79-My7-jhVK2m5iG-kdchw3ULO4ZmCtC4/edit

def timed_execution(func):
    start = time.time()
    func()
    end = time.time()
    total_time = end - start
    print('\n','_'*45)
    print(f"\n {func.__name__} execution time \n{total_time:.2f} sec \nor\n{total_time/60:.2f} min \n")
    print('_'*45)

start = time.time()

# initial optimisations
# 3.13 min for Toulouse (part 1.1)
timed_execution(main_1)

# period
timed_execution(main_2)

# typologie
timed_execution(main_3)
#
# # usage
timed_execution(main_4)
#
# territory
timed_execution(main_5)

# archetype
timed_execution(main_6)


end = time.time()
total_time = end - start
print('\n','#'*60)
print(f"\n ---------- End of exectution of pre treatment module ----------")
print(f"\n Pre treatment module total execution time \n{total_time:.2f} sec \nor\n{total_time/60:.2f} min \n")
print('\n','#'*60)
