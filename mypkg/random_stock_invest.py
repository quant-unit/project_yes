
import pandas as pd
import numpy as np
import pandas_datareader.data as web
from pandas.tseries.offsets import MonthEnd

import os
dir_path = os.path.dirname(os.path.realpath(__file__))

def load_stock_data(data_set = 'WILL5000INDFC', start_date = '1960-01-31'):
    '''
    Download Wilshire 5000 Total Market Full Cap Index (Full US Stock Market Proxy)
    https://fred.stlouisfed.org/series/WILL5000INDFC
    '''
    df = web.DataReader(data_set, 'fred', start_date)
    df.WILL5000INDFC.fillna(method='ffill', inplace=True)
    df['DATE'] = pd.to_datetime(df.index)
    return df

def simulate_entry_to_exit(df):
    '''
    Make one randomly timed investment in the US stock market
    And generate several (one-many) associated divestment cash flows
    '''
    use_first_dates = 0.5
    invest_period = np.rint(len(df) * use_first_dates).astype(int)
    investment_date = np.random.choice(df.DATE.iloc[:invest_period])
    df = df.loc[df.DATE >= investment_date, :].copy()
    df.WILL5000INDFC = df.WILL5000INDFC / df.WILL5000INDFC.iloc[0]

    shape = 2.0
    scale = 2.0
    no_exits = range(1,5)
    days_in_year = 365.25
    size = np.random.choice(no_exits)

    # gamma distribution mean = shape * scale (i.e., average holding period in years)
    r_gamma = np.rint(np.minimum(len(df)-1, np.random.gamma(shape, scale, size) * days_in_year)).astype(int)
    r_gamma = np.append([0], r_gamma)
    df = df.iloc[r_gamma]

    r_diri = np.random.dirichlet(np.repeat(1, size), size=1)
    weight = np.append([-1], r_diri[0] / sum(r_diri[0]))
    df['cash_flow'] = df.WILL5000INDFC * weight
    del df['WILL5000INDFC']
    return df

def make_some_investments(df_stock_index, n=10):
    '''
    Wrapper to n-times iterate simulate_entry_to_exit() function
    Concat and format output
    Save output as .csv file
    '''
    sim_list = [simulate_entry_to_exit(df_stock_index) for x in range(0,n)]
    df = pd.concat(sim_list).reset_index(drop=True)
    df.DATE = df.DATE + MonthEnd(0)
    df = df.groupby('DATE').sum()
    df.sort_values('DATE', inplace=True)

    path = os.path.join(dir_path, 'data', 'cash_flows_to_evaluate.csv')
    df.to_csv(path)

    return df

def calc_multiple(df):
    '''
    Calc cumulative divestment to investment multiple
    '''
    multiple = df.cash_flow[df.cash_flow > 0].sum() / - df.cash_flow[df.cash_flow < 0].sum()
    return round(multiple, 2)

if __name__ == "__main__":
    df = load_stock_data()
    simulate_entry_to_exit(df)
    df = make_some_investments(df)
    print(df)