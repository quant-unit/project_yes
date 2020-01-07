# investment object class
from mypkg import evaluate_cash_flow as ecf


class investment(object):
    def __init__(self, name, manager, fund_type, df_cfs):
        self.name = name
        self.manager = manager
        self.fund_type = fund_type
        self.df_cfs = df_cfs

        self.assert_validity()

    def assert_validity(self):
        assert self.df_cfs.columns == ['cash_flow']
        assert self.fund_type in ['BO', 'VC', 'PE']
        print('*** investment object is valid ***')

    def evaluate_investment_performance(self):
        df_sdf = ecf.select_sdf(self.fund_type)
        dict_summary = ecf.analyze_npv(df_sdf, self.df_cfs)

        print('Summary statistics of investment performance:')
        for k, v in dict_summary.items():
            print('___ {}: {}'.format(k,v))

        if dict_summary['mean'] > 0:
            assesment = 'great'
        else:
            assesment = 'poor'
        print('To conclude: {} you did a {} investment job with your {}.'.format(self.manager, assesment, self.name))

if __name__ == "__main__":
    import numpy as np
    np.random.seed(123)

    dict_in = {
        'name': 'PureAlphaPremiumStrategy',
        'manager': 'Chris Tausch',
        'fund_type': 'VC',
        'df_cfs': ecf.simulate_cash_flow(100),
    }

    inv = investment(**dict_in)
    inv.evaluate_investment_performance()