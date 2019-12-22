
import pandas as pd
import pandas_datareader.data as web
from pandas.tseries.offsets import MonthEnd
import numpy as np


def get_factor_model(exp_affine=True, weighting="VW"):
    if exp_affine:
        return_type = 'exp'
    else:
        return_type = 'lin'
    assert weighting in ['EW', 'VW'], 'unknown weighting used: {}'.format(weighting)

    url = 'https://raw.githubusercontent.com/quant-unit/sdf_private_equity/master/resi/df_resi_{}_{}.csv'.format(return_type, weighting)
    df_model = pd.read_csv(url)

    df_model = df_model[df_model.Horizon >= 120]
    df_model = df_model[df_model.Horizon <= 180]

    df_model.set_index(['Horizon', 'Fund.Type', 'Max.Vin','Model'], inplace=True)
    df_model = df_model[['One', 'Mkt.RF', 'HML', 'SMB', 'RMW', 'CMA']]
    df_model['RF'] = 1

    return df_model

def inner_assert(df):
    shape = df.shape
    assert shape[1] == 7

    existing_cols = df.columns
    expected_cols = ['One', 'Mkt.RF', 'HML', 'SMB', 'RMW', 'CMA', 'RF']
    for col in expected_cols:
        assert col in existing_cols, col

def test_get_factor_model():
    df = get_factor_model()
    inner_assert(df)

def get_fama_french():
    '''
    factor_model intercept is estimated for monthly returns
    assert fama_french data is on a monthly interval
    '''
    ds = web.DataReader('F-F_Research_Data_5_Factors_2x3', 'famafrench', '1960-01-31')
    df_ff = ds[0]
    df_ff.index = df_ff.index.to_timestamp() + MonthEnd(0)
    df_ff = round(df_ff / 100.0, 4) # convert percentage returns
    df_ff['One'] = 1
    df_ff.rename(columns={'Mkt-RF': 'Mkt.RF'}, inplace=True)

    df_ff.to_csv('data/ff_returns.csv')

    return df_ff

def test_get_fama_french():
    df = get_fama_french()
    inner_assert(df)

    from pandas_datareader.famafrench import get_available_datasets
    data_sets = get_available_datasets()
    assert 'F-F_Research_Data_5_Factors_2x3' in data_sets

def total_return_index(df_model, df_ff, exp_affine=True):
    df_ff = df_ff[df_model.columns]

    df = np.dot(df_ff, df_model.transpose())
    df = pd.DataFrame(df, index=df_ff.index, columns=df_model.index)

    if not exp_affine: # simple linear model
        df = np.log(1 + df)
    df = df.cumsum(axis=0)
    df = np.exp(df)
    return df

def test_total_return_index():
    df_model = get_factor_model()
    df_ff = get_fama_french()
    df = total_return_index(df_model, df_ff)
    assert df_ff.shape[0] == df.shape[0]

if __name__ == "__main__":
    #print(get_available_datasets())

    df_model = get_factor_model()
    df_ff = get_fama_french()
    df = total_return_index(df_model, df_ff)

