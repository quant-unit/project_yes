
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
        assert random_stock_invest.calc_multiple(df) == 2.70

if __name__ == "__main__":
    tc = TestClass()
    tc.test_load_stock_data()
    tc.test_make_some_investments()