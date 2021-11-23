from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from enum import Enum
from api import model

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
    prediction_results = model.make_prediction_withtime(instrument_id.value)
    return prediction_results