import requests
import pandas as pd

def fetch_moex_history(ticker, t_type, offset=0, start_date="2024-01-03", limit=100, cols="TRADEDATE,CLOSE,NUMTRADES"):
    if t_type=="stock":
        url = f"https://iss.moex.com/iss/history/engines/stock/markets/shares/boards/TQBR/securities/{ticker}.json"
    elif t_type=="currency":
        url = f"https://iss.moex.com/iss/history/engines/currency/markets/selt/boards/CETS/securities/{ticker}.json"
    else:
        raise Exception("something is wrong..")
    params = {
        "from": start_date,
        "start": 1+offset,
        "iss.meta": "off",
        "history.columns": cols,
        "limit": limit,
    }
    res = requests.get(url, params=params).json()
    df = pd.DataFrame(res["history"]["data"], columns=res["history"]["columns"])
    df["TRADEDATE"] = pd.to_datetime(df["TRADEDATE"])
    return df


def find_currencies(query) -> pd.DataFrame:
    url = "https://iss.moex.com/iss/securities.json"
    params = {
        "q" : query,
        "iss.meta": "off"
    }
    res = requests.get(url, params=params).json()
    columns = res["securities"]["columns"]
    data = res["securities"]["data"]

    df = pd.DataFrame(data, columns=columns)
    df = df[ (df['group']=='currency_selt') & (df["primary_boardid"]=='CETS') 
            & (df['is_traded'])]
    return df[['secid','shortname','name']]


def find_stocks(query: str) -> pd.DataFrame:
    url = "https://iss.moex.com/iss/securities.json"
    params = {
        "q": query,
        "iss.meta": "off"
    }
    res = requests.get(url, params=params).json()
    df = pd.DataFrame(res["securities"]["data"], columns=res["securities"]["columns"])
    return df[(df["group"]=="stock_shares") & df["is_traded"]  
          & (df["primary_boardid"]=="TQBR") & 
          (df["marketprice_boardid"]=="TQBR")][["secid","shortname","name"]]


def stock_exists(name):
    res = find_stocks(name)
    return res[ res['secid']==name ].shape[0] != 0


def currency_exists(name):
    res = find_currencies(name)
    return res[ res['secid']==name ].shape[0] != 0
