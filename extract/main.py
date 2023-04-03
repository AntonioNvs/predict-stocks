import json
import pandas as pd
from extract.history import get_history_data_of_stock

def execution():
  papers = pd.read_csv("data/stocks.csv")

  for idx, code in enumerate(papers["papel"].values):
    print(f"Getting {code} now: {idx} of {papers.shape[0]}")

    while True:
      try:
        history = get_history_data_of_stock(code.lower())
        df = pd.DataFrame.from_dict({year: vars(instance) for (year, instance) in history.items()})
        df.T.to_csv(f"database/{code}.csv")

        break

      except KeyError:
        print(f"The {code} doesn't exists on history.")
        break
      except json.decoder.JSONDecodeError:
        continue


