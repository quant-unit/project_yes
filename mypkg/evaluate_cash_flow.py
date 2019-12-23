from mypkg import factor_model, random_stock_invest
import numpy as np

#np.random.seed(126)

# simulate cash_flow
def simulate_cash_flow(no_investments = 5):
    df_stock_data = random_stock_invest.load_stock_data()
    df_cash_flow = random_stock_invest.make_some_investments(df_stock_data, no_investments)
    return df_cash_flow

# select SDF models
def select_sdf(fund_type = 'VC'):
    df_model = factor_model.get_factor_model()
    df_ff = factor_model.get_fama_french()
    df_sdf = factor_model.sdf(df_model, df_ff)
    df_sdf = df_sdf.iloc[:, df_sdf.columns.get_level_values('Fund.Type') == fund_type]
    return df_sdf

# calc and analyze NPV
def analyze_npv(df_sdf, df_cash_flow):
    df_sdf = df_sdf.loc[df_cash_flow.index]
    assert len(df_sdf) == len(df_cash_flow)
    npv = np.dot(df_sdf.transpose(), df_cash_flow)

    dict_summary = {
        'mean': np.mean(npv),
        'prob_of_outperformance': sum([1 for x in npv if x > 0]) / len(npv),
    }

    quantiles = [0.1, 0.25, 0.5, 0.75, 0.9]
    for q in quantiles:
        dict_summary['quantile_' + str(q)] = np.quantile(npv, q)

    for k, v in dict_summary.items():
        dict_summary[k] = round(v, 2)

    return dict_summary

if __name__ == "__main__":
    n = 10
    df_cash_flow = simulate_cash_flow(n)
    multiple = random_stock_invest.calc_multiple(df_cash_flow)
    print('{} random investments in US stock market result in a multiple of {}.'.format(n, multiple))
    print('How are the chances that we got outperformed by private equity investments?')

    for fund_type in ['VC', 'BO', 'PE']:
        print('*** SDF for fund_type:', fund_type)
        df_sdf = select_sdf(fund_type)
        dict_summary = analyze_npv(df_sdf, df_cash_flow.copy())
        for k, v in dict_summary.items():
            print('   ', k, ':', v)