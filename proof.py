"""
This script compares the predictions of dew point temperature using two methods: 
1) Magnus-Tetens formula, and 
2) XGBoost Regression. 

The input data are two CSV files containing weather observations, and the output is a plot and a CSV file 
comparing the predicted and actual dew point temperatures. 

Functions:
----------
- get_r2_score(y_true, y_pred):
    Calculates and returns the R-squared score of the predicted values `y_pred` compared to the actual 
    values `y_true`.

- get_rmse(y_true, y_pred):
    Calculates and returns the root mean squared error (RMSE) of the predicted values `y_pred` compared 
    to the actual values `y_true`.

- preproc(_df):
    Preprocesses the input DataFrame `_df` by filling NaN values and dropping rows with missing data.

- calc_by_MagnusTetens(air_temperature, humidity, atm_pressure):
    Calculates the dew point temperature using the Magnus-Tetens formula based on the input air temperature, 
    humidity, and atmospheric pressure.

Input data:
-----------
- Two CSV files containing weather observations: "OBS_ASOS_TIM_20230318155150.csv" and 
  "OBS_ASOS_TIM_20230317173225.csv".

Output files:
-------------
- "compare.png": a 3D scatter plot comparing the predicted and actual dew point temperatures using the 
  Magnus-Tetens formula and XGBoost Regression.

- "compare.csv": a CSV file containing the actual dew point temperature, the predicted dew point temperature 
  using the Magnus-Tetens formula, and the predicted dew point temperature using XGBoost Regression.

Dependencies:
-------------
- pandas, math, numpy, matplotlib, mpl_toolkits.mplot3d, and sklearn.metrics from scikit-learn.
- xgboost.XGBRegressor from XGBoost.

""" 

from xgboost import XGBRegressor as XGBR
import pandas as pd
import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def get_r2_score(y_true, y_pred):
    from sklearn.metrics import r2_score

    return r2_score(y_true, y_pred)


def get_rmse(y_true, y_pred):
    from sklearn.metrics import mean_squared_error

    return np.sqrt(mean_squared_error(y_true, y_pred))


def preproc(_df):
    _df["강수량(mm)"] = _df["강수량(mm)"].fillna(0)
    _df["적설(cm)"] = _df["적설(cm)"].fillna(0)
    _df = _df.dropna(axis=0)
    return _df


def calc_by_MagnusTetens(air_temperature, humidity, atm_pressure):
    alpha = 17.27
    beta = 237.7
    gamma = ((alpha * air_temperature) / (beta + air_temperature)) + math.log(
        humidity / 100.0
    )
    es = (
        6.112
        * math.exp(gamma)
        * (atm_pressure / 1013.25) ** (1.0 - 0.00075 * air_temperature)
    )
    gamma_dp = math.log(es / 6.112)
    dew_point = (beta * gamma_dp) / (alpha - gamma_dp)
    return dew_point


df = pd.read_csv("OBS_ASOS_TIM_20230318155150.csv", encoding="cp949")
df2 = pd.read_csv("OBS_ASOS_TIM_20230317173225.csv", encoding="cp949")
df = preproc(df)
df2 = preproc(df2)

xgbr = XGBR()
xgbr.fit(
    df[["기온(°C)", "강수량(mm)", "습도(%)", "현지기압(hPa)", "적설(cm)", "지면온도(°C)"]],
    df["이슬점온도(°C)"],
)
xgbr.score(
    df2[["기온(°C)", "강수량(mm)", "습도(%)", "현지기압(hPa)", "적설(cm)", "지면온도(°C)"]],
    df2["이슬점온도(°C)"],
)

df2["out_MT"] = df2.apply(
    lambda x: calc_by_MagnusTetens(x["기온(°C)"], x["습도(%)"], x["현지기압(hPa)"]), axis=1
)
df2["out_XGBR"] = xgbr.predict(
    df2[["기온(°C)", "강수량(mm)", "습도(%)", "현지기압(hPa)", "적설(cm)", "지면온도(°C)"]]
)

fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection="3d")

plt.scatter(df2["out_MT"], df2["기온(°C)"], df2["습도(%)"], c="g", alpha=0.2)
plt.scatter(df2["out_XGBR"], df2["기온(°C)"], df2["습도(%)"], c="b", alpha=0.2)
plt.scatter(df2["이슬점온도(°C)"], df2["기온(°C)"], df2["습도(%)"], c="r")
plt.savefig("compare.png")

print("R2 MT: ", get_r2_score(df2["이슬점온도(°C)"], df2["out_MT"]))
print("R2 XGGR: ", get_r2_score(df2["이슬점온도(°C)"], df2["out_XGBR"]))
print("RMSE MT: ", get_rmse(df2["이슬점온도(°C)"], df2["out_MT"]))
print("RMSE XGGR: ", get_rmse(df2["이슬점온도(°C)"], df2["out_XGBR"]))
print("MAX ABS ERROR MT: ", abs(df2["out_MT"] - df2["이슬점온도(°C)"]).max())
print("MAX ABS ERROR XGGR: ", abs(df2["out_XGBR"] - df2["이슬점온도(°C)"]).max())

df2[["이슬점온도(°C)", "out_MT", "out_XGBR"]].to_csv(
    "compare.csv", index=False
)
