
import pandas as pd
import numpy as np

import os
dir_path = os.path.dirname(os.path.realpath(__file__))

def load_stock_data():
    # https://fred.stlouisfed.org/series/WILL5000INDFC
    path = os.path.join(dir_path, 'data', 'WILL5000INDFC.csv')
    df = pd.read_csv(path, na_values='.')
    df.WILL5000INDFC.fillna(method='ffill', inplace=True)
    df.DATE = pd.to_datetime(df.DATE)
    return df

def simulate_entry_to_exit(df):
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
    sim_list = [simulate_entry_to_exit(df_stock_index) for x in range(0,n)]
    df = pd.concat(sim_list).reset_index(drop=True)
    df.sort_values('DATE', inplace=True)

    path = os.path.join(dir_path, 'data', 'cash_flows_to_evaluate.csv')
    df.to_csv(path)

    return df

if __name__ == "__main__":
    df = load_stock_data()
    simulate_entry_to_exit(df)
    df = make_some_investments(df)