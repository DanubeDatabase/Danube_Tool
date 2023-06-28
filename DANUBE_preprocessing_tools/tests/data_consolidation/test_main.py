
from config_show import timed_execution
from tests.test_main_preprocess import SMALL_SAMPLE, open_local_data_sample

from data_consolidation.main import main_dc_data_consolidation


if __name__ == '__console__':
    print("RUNNING TEST DATA CONSOLIDATION")
    DANUBE_LAYERS = timed_execution(open_local_data_sample, SMALL_SAMPLE)
    DANUBE_LAYERS = main_dc_data_consolidation(DANUBE_LAYERS)
