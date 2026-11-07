
import time
from pathlib import Path

import pandas as pd
import yfinance as yf

# 1. Investment Universe: 20 stocks + SPY
tickers = [
    # Technology & Communication
    "AAPL", "MSFT", "NVDA", "GOOGL", "META", "AMZN",

    # Financials
    "JPM", "BAC", "GS", "V", "MA",

    # Healthcare
    "JNJ", "UNH", "PFE", "LLY",

    # Consumer & Energy
    "WMT", "COST", "PG", "KO", "XOM"
]

all_tickers = tickers + ["SPY"]

# 2. Date range
START_DATE = "2014-01-01"
END_DATE = "2026-01-01"  # Exclusive

# 3. Google Drive directory
DATA_DIR = Path.home() / (
    "Library/CloudStorage/"
    "GoogleDrive-zhaozihe17@gmail.com/"
    "我的云端硬盘/momentum_research/data/raw"
)

DATA_DIR.mkdir(parents=True, exist_ok=True)

# 4. Download
download_log = []

for i, ticker in enumerate(all_tickers, start=1):
    print(f"[{i}/{len(all_tickers)}] Downloading {ticker}...")

    try:
        df = yf.download(
            ticker,
            start=START_DATE,
            end=END_DATE,
            auto_adjust=False,
            actions=True,
            multi_level_index=False,
            progress=False,
            threads=False
        )

        if df.empty:
            raise ValueError("Empty dataset")

        df.index.name = "Date"

        file_path = DATA_DIR / f"{ticker}.csv"
        df.to_csv(file_path)

        download_log.append({
            "Ticker": ticker,
            "Status": "Success",
            "Rows": len(df),
            "Start": df.index.min().date(),
            "End": df.index.max().date(),
            "Error": ""
        })

        print(f"  Saved {len(df)} rows")

    except Exception as e:
        download_log.append({
            "Ticker": ticker,
            "Status": "Failed",
            "Rows": 0,
            "Start": None,
            "End": None,
            "Error": str(e)
        })

        print(f"  Failed: {e}")

    time.sleep(1)

# 5. Save download summary
summary = pd.DataFrame(download_log)
summary.to_csv(DATA_DIR / "download_summary.csv", index=False)

print("\n=== Download Summary ===")
print(summary.to_string(index=False))

print("\nSuccessful:",
      (summary["Status"] == "Success").sum())
print("Failed:",
      (summary["Status"] == "Failed").sum())
print("Saved to:", DATA_DIR)
