# Project YES

## Summary
This python package demonstrates possible applications of Stochastic Discount Factors (SDFs) estimated for private equity fund data. The estimation methodology is explained [here](https://quant-unit.com/towards-public-market-equivalence/).
> How to apply an SDF ensemble to evaluate investment cash flows.

The general idea is to use an **ensemble of many SDF models** to obtain many reasonable net present value (NPV) estimates for a given payment stream. The empirical distribution of these NPVs allows you a probabilistic assessment of your investment success.

## Implementation
- **random_stock_invest.py** allows you to simulate a payment stream based on randomly timed investments and divestments in the US stock market.
- **factor_model.py** creates SDFs by combining the following [factor model estimates](https://github.com/quant-unit/sdf_private_equity) with the corresponding [Fama-French](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html) factor return data.
- **evaluate_cash_flow.py** evaluates the random cash flows by SDFs.

## TO DO
- create class for **random_stock_invest.py** and **factor_model.py**.