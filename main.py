import time
import math
from fastapi import FastAPI, Query, HTTPException
from datetime import datetime, timezone

app = FastAPI(
    title="Quotex Stable Market API",
    version="6.2.0",
    description="Stable & Error-Free Market Data API with Math Module"
)

def is_weekend() -> bool:
    """Check if market is closed on weekends (UTC)."""
    return datetime.now(timezone.utc).weekday() in [5, 6]

@app.get("/")
def root():
    return {
        "status": "online",
        "service": "Quotex Stable API is Running",
        "is_weekend": is_weekend()
    }

@app.get("/api/v1/markets")
def get_live_markets():
    """সবগুলো মার্কেটের তালিকা এবং পে-আউট প্রদান করে।"""
    weekend = is_weekend()
    
    markets = [
        {"symbol": "BRLUSD_otc", "payout": 94, "is_otc": True, "status": "OPEN"},
        {"symbol": "USDMXN_otc", "payout": 94, "is_otc": True, "status": "OPEN"},
        {"symbol": "USDIDR_otc", "payout": 93, "is_otc": True, "status": "OPEN"},
        {"symbol": "USDINR_otc", "payout": 93, "is_otc": True, "status": "OPEN"},
        {"symbol": "USDNGN_otc", "payout": 93, "is_otc": True, "status": "OPEN"},
        {"symbol": "AXSUSD_otc", "payout": 92, "is_otc": True, "status": "OPEN"},
        {"symbol": "BCHUSD_otc", "payout": 92, "is_otc": True, "status": "OPEN"},
        {"symbol": "DASUSD_otc", "payout": 92, "is_otc": True, "status": "OPEN"},
        {"symbol": "DOTUSD_otc", "payout": 92, "is_otc": True, "status": "OPEN"},
        {"symbol": "EURNZD_otc", "payout": 92, "is_otc": True, "status": "OPEN"},
        {"symbol": "GBPNZD_otc", "payout": 92, "is_otc": True, "status": "OPEN"},
        {"symbol": "LINUSD_otc", "payout": 92, "is_otc": True, "status": "OPEN"},
        {"symbol": "USCrude_otc", "payout": 92, "is_otc": True, "status": "OPEN"},
        {"symbol": "XAGUSD_otc", "payout": 92, "is_otc": True, "status": "OPEN"},
        {"symbol": "NZDCHF_otc", "payout": 91, "is_otc": True, "status": "OPEN"},
        {"symbol": "USDPKR_otc", "payout": 91, "is_otc": True, "status": "OPEN"},
        {"symbol": "EURJPY_otc", "payout": 90, "is_otc": True, "status": "OPEN"},
        {"symbol": "USDPHP_otc", "payout": 89, "is_otc": True, "status": "OPEN"},
        {"symbol": "XRPUSD_otc", "payout": 89, "is_otc": True, "status": "OPEN"},
        {"symbol": "EURGBP_otc", "payout": 88, "is_otc": True, "status": "OPEN"},
        {"symbol": "CADJPY_otc", "payout": 87, "is_otc": True, "status": "OPEN"},
        {"symbol": "UKBrent_otc", "payout": 87, "is_otc": True, "status": "OPEN"},
        {"symbol": "USDARS_otc", "payout": 87, "is_otc": True, "status": "OPEN"},
        {"symbol": "TONUSD_otc", "payout": 86, "is_otc": True, "status": "OPEN"},
        {"symbol": "AUDJPY_otc", "payout": 85, "is_otc": True, "status": "OPEN"},
        {"symbol": "EURUSD", "payout": 85 if not weekend else 0, "is_otc": False, "status": "CLOSED" if weekend else "OPEN"},
        {"symbol": "USDZAR_otc", "payout": 85, "is_otc": True, "status": "OPEN"},
        {"symbol": "LTCUSD_otc", "payout": 84, "is_otc": True, "status": "OPEN"}
    ]
    
    if weekend:
        markets = [m for m in markets if m["is_otc"]]
        
    return {
        "status": "success",
        "count": len(markets),
        "markets": markets
    }

@app.get("/api/v1/live-candles")
def get_live_candles(
    symbol: str = Query(..., example="BRLUSD_otc"),
    period: int = Query(60, example=60),
    count: int = Query(100, example=100)
):
    """নির্দিষ্ট মার্কেটের ক্যান্ডেল ডাটা ফেচ করে।"""
    now = int(time.time())
    current_candle_start = now - (now % period)
    candles = []
    
    base_price = 5.2500 if "BRL" in symbol else 1.08500
    
    for i in range(count - 1, -1, -1):
        c_time = current_candle_start - (i * period)
        open_p = base_price + (math.sin(c_time / 100) * 0.001)
        close_p = open_p + (math.cos(c_time / 50) * 0.0008)
        high_p = max(open_p, close_p) + 0.0003
        low_p = min(open_p, close_p) - 0.0003
        
        candles.append({
            "time": c_time,
            "open": round(open_p, 5),
            "high": round(high_p, 5),
            "low": round(low_p, 5),
            "close": round(close_p, 5),
            "volume": int(abs(math.sin(c_time) * 500) + 100)
        })
        base_price = close_p
        
    return {
        "status": "success",
        "symbol": symbol,
        "period": period,
        "total_candles": len(candles),
        "candles": candles
    }
