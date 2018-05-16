from pandas_ingester.pandas_ingester import main, load_data, save_pif

import pandas as pd
import pypif.pif as pif


def test_load_data():
    df = load_data('../data/dsgdb9nsd_067017.xyz')
    assert isinstance(df, pd.DataFrame)
