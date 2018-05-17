from pandas_ingester.pandas_ingester import main, load_data, save_pif

import pandas as pd
import os
from os.path import dirname, join, abspath
import pypif.pif as pif


base_dir = dirname(abspath(__file__)) + os.path.sep

def test_load_data():
    data_file = join(base_dir, '..', 'data', 'dsgdb9nsd_067017.xyz')
    df = load_data(data_file)
    assert isinstance(df, pd.DataFrame)


def test_main():
    data_file = join(base_dir, '..', 'data', 'dsgdb9nsd_067017.xyz')

    main(data_file)
    #assert os.path.isfile(os.path.join(os.getcwd(), 
