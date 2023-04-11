import os
import pandas as pd
import yfinance as yf

def get_price_stocks(ticker: str, start_date = "2013-01-01", end_date = "2023-03-31"):
  return yf.download(f"{ticker}.SA", start=start_date, end=end_date)


def get_price_by_year(cotations: pd.DataFrame, year: int) -> float:
  day = 20
  for d in range(day, 31):
    try:
      return cotations["Close"][f"{year}-03-{d}"]
    except KeyError:
      continue

if __name__ == "__main__":
  stocks = pd.read_csv("stocks.csv")["papel"]

  for paper in stocks.values[:10]:
    filename = f"database/{paper}.csv"
    
    if not os.path.exists(filename): continue
    data = pd.read_csv(filename, index_col=0)

    cotations = []
    info = get_price_stocks(paper)
    for year in data.index:
      print(year)
      cotations.append(get_price_by_year(info, year))

    print(cotations)
