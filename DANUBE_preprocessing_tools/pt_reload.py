import imp
# import pt_main
import pt_basic_functions
import pt_1_initial_optimisation
import pt_2_danube_period
import pt_3_danube_typology
import pt_4_danube_usage
import pt_5_danube_territory
import pt_6_danube_archetype


# imp.reload(pt_main)
imp.reload(pt_basic_functions)
imp.reload(pt_1_initial_optimisation)
imp.reload(pt_2_danube_period)
imp.reload(pt_3_danube_typology)
imp.reload(pt_4_danube_usage)
imp.reload(pt_5_danube_territory)
imp.reload(pt_6_danube_archetype)

# from pt_main import *
from pt_basic_functions import *
from pt_1_initial_optimisation import *
from pt_2_danube_period import *
from pt_3_danube_typology import *
from pt_4_danube_usage import *
from pt_5_danube_territory import *
from pt_6_danube_archetype import *


#
# # file to reload
#
# import imp, pt_main
# imp.reload(pt_main)
# from pt_main import *
#
# import imp, pt_basic_functions
# imp.reload(pt_basic_functions)
# from pt_basic_functions import *
#
# import imp, pt_1_initial_optimisation
# imp.reload(pt_1_initial_optimisation)
# from pt_1_initial_optimisation import *
#
#
# import imp, pt_2_danube_period
# imp.reload(pt_2_danube_period)
# from pt_2_danube_period import *
#
#
# from pt_1_initial_optimisation import main_1
# from pt_2_danube_period import main_2
# from pt_3_danube_typology import main_3
# from pt_4_danube_usage import main_4
# from pt_5_danube_territory import main_5
# from pt_6_danube_archetype import main_6


# change "pt_open_layer" by any file bugging to reload

# ____________________random things to keep______________________
# QgsProject.instance().removeMapLayer(result_layer.id())



# values = [feature['column_name'] for feature in layer.getFeatures()]



## check specific features in a column
# # Specify the field name and the value to check
# field_name = 'your_field'  # Replace 'your_field' with the actual field name
# value_to_check = 'your_value'  # Replace 'your_value' with the value to check
#
# # Filter the features based on the condition
# filtered_features = [feature for feature in layer.getFeatures() if feature[field_name] == value_to_check]
#
# # Access the filtered features
# for feature in filtered_features:
#     # Access feature attributes or perform other operations
#     print(feature.attributes())
