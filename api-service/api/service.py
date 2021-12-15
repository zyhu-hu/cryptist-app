from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from api.tracker import TrackerService, TimeTracker
import asyncio
from enum import Enum
from api import model
import numpy as np
import tensorflow as tf
import json
from api import agent_btc, agent_eth


local_experiments_path = "/persistent/experiments/"

# Initialize Tracker Service
tracker_service = TrackerService()
time_tracker = TimeTracker()
detrend_data = np.load(local_experiments_path+'detrend_data_cryptist.npy')
undetrend_data = np.load(local_experiments_path+'undetrended_data_cryptist.npy')
model_c = tf.keras.models.load_model(
    local_experiments_path+'view_instrument_37_bid_and_ask')

class InstrumentIDs(str, Enum):
    btc_binance_usdt = "BINANCE:BTC_USDT.SWAP"
    eth_binance_usdt = "BINANCE:ETH_USDT.SWAP"
    ltc_binance_usdt = "BINANCE:LTC_USDT.SWAP"



# Setup FastAPI app
app = FastAPI(
    title="API Server",
    description="API Server",
    version="v1"
)

# Enable CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=False,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
@app.on_event("startup")
async def startup():
    # Startup tasks
    # Start the tracker service
    asyncio.create_task(tracker_service.track())
    asyncio.create_task(time_tracker.track())


@app.get("/")
async def get_index():
    return {
        "message": "Welcome to the API Service"
    }


@app.get("/predict/{instrument_id}")
async def predict(instrument_id: InstrumentIDs):
    prediction_results = model.make_prediction(instrument_id.value)
    return prediction_results


@app.get("/predict_withtime/{instrument_id}")
async def predict(instrument_id: InstrumentIDs):
    prediction_results = model.make_prediction_withtime(
        instrument_id.value, time_tracker.timeindex, detrend_data, model_c)
    return prediction_results

@app.post("/agent")
async def synthesize(json_arr: list):
    if json_arr[2]['value'] == 'BINANCE:BTC_USDT.SWAP':
        drl_agent = agent_btc.create_agent()
    if json_arr[2]['value'] == 'BINANCE:ETH_USDT.SWAP':
        drl_agent = agent_eth.create_agent()
    time_idx = json_arr[4]['value']
    total = json_arr[0]['value']
    balance = json_arr[1]['value']
    share = json_arr[3]['value']
    x = undetrend_data[:, time_idx:time_idx+10, :]

    if json_arr[2]['value'] == 'BINANCE:BTC_USDT.SWAP':
        tmp1, tmp2, tmp3 = agent_btc.trading_action(
            drl_agent, x, share, balance, total)
    if json_arr[2]['value'] == 'BINANCE:ETH_USDT.SWAP':
        tmp1, tmp2, tmp3 = agent_eth.trading_action(
            drl_agent, x, share, balance, total)
    return {
        'total': tmp1,
        "power": tmp2,
        "shares": tmp3.item()
    }
    
