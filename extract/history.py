import json, math
import requests

from typing import Dict

from utils.format import transform_str_to_float
from datatype.stock import StockHistoryDetail

def request_history_data_of_stock(code: str) -> list:
  url = "https://statusinvest.com.br/acao/indicatorhistoricallist"

  payload = f"codes%5B%5D={code}&time=7&byQuarter=false&futureData=false"
  headers = {
      "cookie": "_adasys=0dbe9eb1-4a0e-4e12-8d04-e336f25f7ea4; G_ENABLED_IDPS=google; .StatusAdThin=1; __cf_bm=uvFR6bsxBeFU8SfHMr8ezVI190PVYs5IRA43lULuhos-1680380152-0-ATGTZdttvwTz5A6g2hQsG42s6Ykgx9ppbUr29nVBUO+fMz7lYDk5ejeyrJxImPyCs3hjsh6BX5XQUuGLle+luY8LkDQpbNK5rmnvpcG6vbrHcML01jTEfz5ygP60fYaaXA==",
      "authority": "statusinvest.com.br",
      "accept": "*/*",
      "accept-language": "pt-BR,pt;q=0.8",
      "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
      "origin": "https://statusinvest.com.br",
      "referer": f"https://statusinvest.com.br/acoes/{code}",
      "sec-ch-ua": '"Brave";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
      "sec-ch-ua-mobile": "?1",
      "sec-ch-ua-platform": "Android",
      "sec-fetch-dest": "empty",
      "sec-fetch-mode": "cors",
      "sec-fetch-site": "same-origin",
      "sec-gpc": "1",
      "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36"
  }

  response = requests.request("POST", url, data=payload, headers=headers)

  return json.loads(response.text)["data"][code]


def get_history_data_of_stock(code: str) -> Dict[str, StockHistoryDetail]:
  data = request_history_data_of_stock(code)

  assert len(data) > 0, "The paper doesnt have history."

  years = {y: StockHistoryDetail() for y in range(2024 - len(data[0]["ranks"]), 2024)}

  for info in data:
    key = info["key"]
    for year in info["ranks"]:
      try:
        value = transform_str_to_float(year["value_F"])
      except:
        value = math.inf

      years[year["rank"]].setattribute(key, value)

  
  return years