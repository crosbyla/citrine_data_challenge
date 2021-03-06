from pandas_ingester.pandas_ingester import main, load_data, make_pif, parse_cli
import argparse
import pytest
import pandas as pd
import re
import os
from os.path import dirname, join, abspath, isfile
import pypif.pif as pif
from pypif.obj import System

pat = re.compile(r'_(\d+).xyz')
base_dir = dirname(abspath(__file__)) + os.path.sep

def test_make_pif():
    data_dir = join(base_dir, '..', 'data')
    data_files = [
            'dsgdb9nsd_067017.xyz',
            'dsgdb9nsd_017001.xyz',
            'dsgdb9nsd_129001.xyz'
            ]
    for data_file in data_files:
        pif_data = make_pif(load_data(join(data_dir, data_file)))
        assert isinstance(pif_data, System), 'Could not create PIF object'

def test_load_data():
    data_dir = join(base_dir, '..', 'data')
    data_files = [
            'dsgdb9nsd_067017.xyz',
            'dsgdb9nsd_017001.xyz',
            'dsgdb9nsd_129001.xyz'
            ]
    for data_file in data_files:
        df = load_data(join(data_dir, data_file))
        assert isinstance(df, pd.DataFrame), 'Could not create Pandas DataFrame'


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
        assert isfile(join(os.curdir,'{}.json'.format(file_id))), 'Could not write JSON file'

def test_parse_cli():
    test_args = '123abc.xyz -o data/dir/fname.json'.split()
    assert isinstance(parse_cli(test_args), argparse.Namespace)

    test_args = '124abc.txt'.split()
    with pytest.raises(ValueError) as excinfo:
        parse_cli(test_args)
    assert str(excinfo.value) == 'Must be XYZ file!'
