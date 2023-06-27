import time
from pathlib import Path

from qgis.core import Qgis, QgsMessageLog, QgsVectorLayer, QgsProject

# ___________________Define variables of test and debug to run the workflow___________________

PRINT_LOG = True  # if True, print in the console steps of the process

SHOW_GUI_LAY = True  # if True add intermediate layers to QGIS GUI to check

TIME_MEMORY = False  # import module (to be installed first) which allows showing memory use


# ___________________Functions in developing and debug mode___________________


def print_log(*args):
    """Print if the 'debug_print' variable is True"""
    if PRINT_LOG:
        print(*args)

        for arg in args:
            QgsMessageLog.logMessage(str(arg), 'DANUBE tool', level=Qgis.Info)


def print_fields(layer):
    """Print the fields of a layer if the 'debug_print' variable is True"""
    print_log(f"\n{layer.name()}:\n", layer.fields().names())


def timed_execution(func, *args, **kwargs):
    """Run a function and print its execution time if the 'debug_print' variable is True"""
    start = time.time()
    result = func(*args, **kwargs)
    end = time.time()
    total_time = end - start
    print_log("_" * 25)
    print_log(f"\n{func.__name__} \nexecution time \n{total_time:.2f} sec or {total_time / 60:.2f} min")
    print_log("_" * 25)
    return result


if TIME_MEMORY:
    import psutil
def print_memory_use():
    """Print memory use if the 'time_memory' variable is True"""
    if TIME_MEMORY:
        print_log('psutil RAM memory % used:', psutil.virtual_memory()[2])
        print_log('psutil RAM Used (GB):', psutil.virtual_memory()[3] / 1000000000)
    else:
        pass


def add_layer_gui(layer, layer_name=None):
    """Add the layer to the QGIS GUI if the 'SHOW_GUI_LAY' variable is True"""
    if SHOW_GUI_LAY:
        # add layer to open project in QGIS
        if layer_name:
            layer.setName(layer_name)
        QgsProject.instance().addMapLayer(layer)


# ___________________Open layers functions___________________

def check_validity(layer):
    """Check if the layer is valid"""
    if layer.isValid():
        print_log(f"\nLayer '{layer.name()}' is valid. \n")
        # Perform the required operations on the layer
        layer.startEditing()  # Start editing the layer
        layer.triggerRepaint()  # Refresh the layer to show changes
        layer.commitChanges()  # Save the changes to the layer
    else:
        print_log(f"\nLayer '{layer.name()}' is NOT valid!\n")


def open_layer(layer_path_or_name):
    """ Get the layer by its name or ID"""

    if type(layer_path_or_name) is str:
        if Path(layer_path_or_name).is_file():
            layer = QgsVectorLayer(layer_path_or_name, Path(layer_path_or_name).stem, 'ogr')  # open layer from path
            check_validity(layer)
            return layer

        else:
            if layer_path_or_name in [vectl.name() for vectl in
                                      list(QgsProject.instance().mapLayers().values())]:  # test if the layer_path_or_name is an open layer
                layer = QgsProject.instance().mapLayersByName(layer_path_or_name)[
                    0]  # Retrieves the first open layer with the given name
                check_validity(layer)
                return layer

            else:
                print_log('name layer not recognized')
    else:
        print_log('Please enter a string type')



if __name__ == '__console__':
    def test_open_layer():
        folder = Path(r"C:\Users\lorena.carvalho\Documents\Develop_outil\data\outil_danube_dev_test_data")
        path_or_layer = str(folder / "small_bati.gpkg")
        layer_names = [layer.name() for layer in QgsProject.instance().mapLayers().values()]
        layer_from_path = open_layer(path_or_layer)
        print("open_layer from path is working!")
        print(layer_from_path.fields().names())

        if len(layer_names) > 0:
            layer_name = layer_names[0]
            layer_from_name = open_layer(layer_name)
            print("open_layer from layer name is working!")
            print(layer_from_name.fields().names())
        else:
            print('No layers are presently open in QGIS. Open a layer in the GIU to test this function')

    print_log("That ", "is ", "a ", "test!")
    test_open_layer()


