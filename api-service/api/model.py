import os
import json
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.python.keras import backend as K
from tensorflow.keras.models import Model
import tensorflow_hub as hub


AUTOTUNE = tf.data.experimental.AUTOTUNE
local_experiments_path = "/persistent/experiments/"


def make_prediction(instrument_id):
    model_fnn = tf.keras.models.load_model(local_experiments_path+'ffnn_model.h5')
    x_test = np.load(local_experiments_path+'ffnn_x_test_5steps.npy')
    data_array = np.load(local_experiments_path+'ffnn_data_array_bid_price1.npy')
    df_max = pd.read_csv(local_experiments_path+'ffnn_model_df_max.csv')
    df_min = pd.read_csv(local_experiments_path+'ffnn_model_df_min.csv')
    bid1max = float(df_max.iloc[7].values[0])
    bid1min = float(df_min.iloc[7].values[0])
    set_interval = 6000
    start_index = 5000
    n_train, n_test = 10000, 3000
    n_backward_input = 10

    ts_predict = np.zeros(5)

    if instrument_id == "BINANCE:BTC_USDT.SWAP":
        predict_detrend = model_fnn.predict(x_test)[:, 48]*(bid1max-bid1min)+bid1min
        ts_predict = data_array[start_index + n_backward_input+n_train:start_index +
                                n_backward_input + n_train+5, 48]*(bid1max-bid1min)+bid1min+predict_detrend[0:5]
    if instrument_id == "BINANCE:ETH_USDT.SWAP":
        predict_detrend = model_fnn.predict(
            x_test)[:, 66]*(bid1max-bid1min)+bid1min
        ts_predict = data_array[start_index + n_backward_input+n_train:start_index +
                                n_backward_input + n_train+5, 66]*(bid1max-bid1min)+bid1min+predict_detrend[0:5]
    ts_predict = np.around(ts_predict, decimals=4)
    return {
        "asset": instrument_id,
        "number of predicting time steps": str(5),
        "prediction": ts_predict.tolist()
    }

def make_prediction_withtime(instrument_id):
    model_fnn = tf.keras.models.load_model(
        local_experiments_path+'ffnn_model.h5')
    x_test = np.load(local_experiments_path+'ffnn_x_test_5steps.npy')
    data_array = np.load(local_experiments_path +
                         'ffnn_data_array_bid_price1.npy')
    df_max = pd.read_csv(local_experiments_path+'ffnn_model_df_max.csv')
    df_min = pd.read_csv(local_experiments_path+'ffnn_model_df_min.csv')
    bid1max = float(df_max.iloc[7].values[0])
    bid1min = float(df_min.iloc[7].values[0])
    set_interval = 6000
    start_index = 5000
    n_train, n_test = 10000, 3000
    n_backward_input = 10

    ts_predict = np.zeros(5)

    if instrument_id == "BINANCE:BTC_USDT.SWAP":
        predict_detrend = model_fnn.predict(
            x_test)[:, 48]*(bid1max-bid1min)+bid1min
        ts_predict = data_array[start_index + n_backward_input+n_train:start_index +
                                n_backward_input + n_train+5, 48]*(bid1max-bid1min)+bid1min+predict_detrend[0:5]
    if instrument_id == "BINANCE:ETH_USDT.SWAP":
        predict_detrend = model_fnn.predict(
            x_test)[:, 66]*(bid1max-bid1min)+bid1min
        ts_predict = data_array[start_index + n_backward_input+n_train:start_index +
                                n_backward_input + n_train+5, 66]*(bid1max-bid1min)+bid1min+predict_detrend[0:5]
    ts_predict = np.around(ts_predict, decimals=4)
    ts_predict_time = np.array(
        (1414368000000, 1414972800000, 1415577600000, 1416182400000,1416787200000))
    ts_predict_list = []
    for i in range(ts_predict.shape[0]):
        ts_predict_list.append([ts_predict_time.tolist()[i], ts_predict.tolist()[i]])
    return {
        "asset": instrument_id,
        "number of predicting time steps": str(5),
        #"prediction": ts_predict_list
        "prediction": ts_predict_list
    }
