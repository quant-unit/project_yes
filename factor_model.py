
import pandas as pd
from pandas_datareader.famafrench import get_available_datasets
import pandas_datareader.data as web
from pandas.tseries.offsets import MonthEnd

def get_factor_model(exp_affine=True, weighting="VW"):
    if exp_affine:
        return_type = 'exp'
    else:
        return_type = 'lin'
    assert weighting in ['EW', 'VW'], 'unknown weighting used: {}'.format(weighting)

    url = 'https://raw.githubusercontent.com/quant-unit/sdf_private_equity/master/resi/df_resi_{}_{}.csv'.format(return_type, weighting)
    df_model = pd.read_csv(url)

    df_model.set_index(['Horizon', 'Fund.Type', 'Max.Vin','Model'], inplace=True)
    df_model = df_model[['One', 'Mkt.RF', 'HML', 'SMB', 'RMW', 'CMA']]
    df_model['RF'] = 1

    print(df_model.columns)
    print(df_model.index)

    return df_model


def get_fama_french():
    ds = web.DataReader('F-F_Research_Data_5_Factors_2x3', 'famafrench', '1960-01-31')
    df_ff = ds[0]
    df_ff.index = df_ff.index.to_timestamp() + MonthEnd(0)
    df_ff['One'] = 1
    df_ff.rename(columns={'Mkt-RF': 'Mkt.RF'})
    print(df_ff.columns)
    print(df_ff.index)
    return df_ff


if __name__ == "__main__":
    #print(get_available_datasets())

    df_model = get_factor_model()
    df_ff = get_fama_french()

