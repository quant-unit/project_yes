
from mypkg import random_stock_invest
import numpy as np
import pandas as pd

class TestClass():
    def test_load_stock_data(self):
        df = random_stock_invest.load_stock_data()
        assert isinstance(df, pd.DataFrame)
        for col in ['WILL5000INDFC', 'DATE']:
            assert col in df.columns, col

    def test_make_some_investments(self):
        np.random.seed(123)
        df = random_stock_invest.make_some_investments(random_stock_invest.load_stock_data(), 100)
        multiple = df.cash_flow[df.cash_flow > 0].sum() / - df.cash_flow[df.cash_flow < 0].sum()
        assert round(multiple, 2) == 2.33, 'np.random.seed() does not work'
        #print(r'Our sophisticated AI/ML strategy made a multiple of {}.'.format(round(multiple, 2)))

if __name__ == "__main__":
    tc = TestClass()
    tc.test_load_stock_data()
    tc.test_make_some_investments()