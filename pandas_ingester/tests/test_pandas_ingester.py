from pandas_ingester.pandas_ingester import main, load_data, save_pif

import pandas as pd
import re
import os
from os.path import dirname, join, abspath, isfile
import pypif.pif as pif

pat = re.compile(r'_(\d+).xyz')
base_dir = dirname(abspath(__file__)) + os.path.sep

def test_load_data():
    data_dir = join(base_dir, '..', 'data')
    data_files = [
            'dsgdb9nsd_067017.xyz',
            'dsgdb9nsd_017001.xyz',
            'dsgdb9nsd_129001.xyz'
            ]
    for data_file in data_files:
        df = load_data(join(data_dir, data_file))
        assert isinstance(df, pd.DataFrame)


def test_main():
    data_dir = join(base_dir, '..', 'data')
    data_files = [
            'dsgdb9nsd_067017.xyz',
            'dsgdb9nsd_017001.xyz',
            'dsgdb9nsd_129001.xyz'
            ]
    for data_file in data_files:
        main(join(data_dir, data_file))
        file_id = int(re.search(pat, data_file).group(1))
        print(file_id)
        assert isfile(join(os.curdir,'{}.json'.format(file_id)))
