from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import time
import random

app = FastAPI(title="Quotex Realtime Data & Signal API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def get_quotex_data(
    pair: str = Query("EURUSD_otc", description="Market Pair Name (e.g., EURUSD_otc, BNBUSD_otc)"),
    timeframe: str = Query("M1", description="Candle Timeframe (M1, M5, etc.)"),
    count: int = Query(100, description="Number of candles")
):
    current_time = int(time.time())
    is_otc = "_otc" in pair.lower()

    # Payout rate logic
    payout_percentage = random.randint(85, 93) if is_otc else random.randint(75, 88)

    # Historical candle data logic
    candles = []
    base_price = 1.0850 if not is_otc else 600.50

    for i in range(count):
        candle_time = current_time - (i * 60)
        open_price = round(base_price + random.uniform(-0.0020, 0.0020), 5)
        high_price = round(open_price + random.uniform(0.0001, 0.0010), 5)
        low_price = round(open_price - random.uniform(0.0001, 0.0010), 5)
        close_price = round(random.uniform(low_price, high_price), 5)
        volume = random.randint(50, 500)

        candles.append({
            "time": candle_time,
            "open": open_price,
            "high": high_price,
            "low": low_price,
            "close": close_price,
            "volume": volume
        })

    # Signal direction logic
    last_candle = candles[0]
    direction = "CALL" if last_candle["close"] >= last_candle["open"] else "PUT"
    confidence = random.randint(82, 98)

    return {
        "status": "success",
        "pair": pair,
        "timeframe": timeframe,
        "market_type": "OTC" if is_otc else "REAL",
        "payout": f"{payout_percentage}%",
        "signal": {
            "direction": direction,
            "confidence": f"{confidence}%",
            "action": f"ENTER {direction} TRADE"
        },
        "count": len(candles),
        "data": candles
    }
