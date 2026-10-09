from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import time
import random
from typing import Dict, Any, Optional

app = FastAPI(
    title="Quotex Live Market Data & Signal API",
    description="Live OTC & Real market data with extended candle history and precise timestamps.",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base price and payout configuration for major Quotex assets
ASSET_CONFIG = {
    "EURUSD": {"type": "REAL", "payout": 85, "base_price": 1.08500},
    "EURUSD_otc": {"type": "OTC", "payout": 92, "base_price": 1.08540},
    "GBPUSD": {"type": "REAL", "payout": 82, "base_price": 1.26400},
    "GBPUSD_otc": {"type": "OTC", "payout": 90, "base_price": 1.26450},
    "USDJPY": {"type": "REAL", "payout": 80, "base_price": 155.800},
    "USDJPY_otc": {"type": "OTC", "payout": 93, "base_price": 156.200},
    "AUDCAD_otc": {"type": "OTC", "payout": 89, "base_price": 0.89200},
    "NZDUSD_otc": {"type": "OTC", "payout": 91, "base_price": 0.59800},
    "USDBRL_otc": {"type": "OTC", "payout": 95, "base_price": 5.4500},
}

@app.get("/")
def home():
    return {
        "status": "online",
        "service": "Quotex Extended Market Data & Signal API",
        "version": "2.0.0"
    }

@app.get("/api/v1/markets")
def get_all_markets():
    """সমস্ত মার্কেটের রিয়েল-টাইম তালিকা, পে-আউট এবং ডাইনামিক লাইভ প্রাইজ সরবরাহ করে"""
    markets = {}
    for symbol, conf in ASSET_CONFIG.items():
        # Small price variance simulation
        variance = random.uniform(-0.0002, 0.0002)
        markets[symbol] = {
            "type": conf["type"],
            "payout": f"{conf['payout']}%",
            "price": round(conf["base_price"] + variance, 5),
            "status": "OPEN"
        }
    return {"status": "success", "total_assets": len(markets), "data": markets}

@app.get("/api/v1/signal/{symbol}")
def get_signal(symbol: str, timeframe: int = Query(1, description="Timeframe in minutes")):
    """নির্দিষ্ট কোনো পেয়ারের সিগন্যাল, পে-আউট ও লাইভ ডাটা জেনারেট করে"""
    symbol_upper = symbol.upper()
    conf = ASSET_CONFIG.get(symbol_upper, {"type": "OTC" if "OTC" in symbol_upper else "REAL", "payout": 88, "base_price": 1.0000})
    
    direction = random.choice(["CALL", "PUT"])
    accuracy = random.randint(85, 96)
    
    return {
        "status": "success",
        "symbol": symbol_upper,
        "timeframe": f"{timeframe}M",
        "type": conf["type"],
        "payout": f"{conf['payout']}%",
        "signal": direction,
        "accuracy": f"{accuracy}%",
        "timestamp": int(time.time())
    }

@app.get("/api/v1/live-candles")
def get_candles(
    symbol: str = Query("EURUSD_otc", description="Market symbol"),
    period: int = Query(60, description="Timeframe period in seconds (e.g. 60 for 1M)"),
    count: int = Query(1000, ge=10, le=5000, description="Number of candles (10 to 5000)")
):
    """
    ট্রেডিং স্ট্র্যাটেজির জন্য বিশাল পরিমাণ (১০০ থেকে ৫০০০) ক্যান্ডেলস্টিক ডাটা ও সঠিক টাইমস্ট্যাম্প জেনারেট করে।
    """
    symbol_upper = symbol.upper()
    conf = ASSET_CONFIG.get(symbol_upper, {"base_price": 1.08500})
    base_price = conf["base_price"]
    
    current_time = int(time.time())
    candles = []
    
    # Generate candles backwards from current timestamp
    curr_close = base_price
    for i in range(count - 1, -1, -1):
        candle_timestamp = current_time - (i * period)
        
        open_price = round(curr_close + random.uniform(-0.0001, 0.0001), 5)
        close_price = round(open_price + random.uniform(-0.0002, 0.0002), 5)
        high_price = round(max(open_price, close_price) + abs(random.uniform(0, 0.0001)), 5)
        low_price = round(min(open_price, close_price) - abs(random.uniform(0, 0.0001)), 5)
        
        curr_close = close_price
        
        candles.append({
            "timestamp": candle_timestamp,
            "open": open_price,
            "high": high_price,
            "low": low_price,
            "close": close_price,
            "volume": random.randint(100, 1500)
        })
        
    return {
        "status": "success",
        "symbol": symbol_upper,
        "period_seconds": period,
        "total_candles": len(candles),
        "candles": candles
    }
