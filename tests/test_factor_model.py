
from mypkg import factor_model

def inner_assert(df):
    shape = df.shape
    assert shape[1] == 7

    existing_cols = df.columns
    expected_cols = ['One', 'Mkt.RF', 'HML', 'SMB', 'RMW', 'CMA', 'RF']
    for col in expected_cols:
        assert col in existing_cols, col

def test_get_factor_model():
    df = factor_model.get_factor_model()
    inner_assert(df)

def test_get_fama_french():
    data_set = 'F-F_Research_Data_5_Factors_2x3'
    from pandas_datareader.famafrench import get_available_datasets
    data_sets = get_available_datasets()
    assert data_set in data_sets

    df = factor_model.get_fama_french(data_set)
    inner_assert(df)

def test_total_return_index():
    df_model = factor_model.get_factor_model()
    df_ff = factor_model.get_fama_french()
    df = factor_model.total_return_index(df_model, df_ff)
    assert df_ff.shape[0] == df.shape[0]

if __name__ == "__main__":
    test_get_factor_model()
    test_get_fama_french()
    test_total_return_index()