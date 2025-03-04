import argparse

import pandas as pd

def verify_df(df: pd.DataFrame):
    last_close = 0
    i = 0
    for row in df.itertuples():
        i += 1
        open_time = int(row[1])
        if last_close == 0:
            last_close = int(row[6])
            continue
        if last_close + 1 != open_time:
            print(f"{i=}, {last_close=}, {open_time=}")
        last_close = int(row[6])


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("symbol", type=str, choices=["bnb", "eth", "btc", "matic"])
    ap.add_argument("tf", type=str, choices=["1m", "15m", "1h", "4h", "1d"])

    args = vars(ap.parse_args())

    symbol = args["symbol"]
    tf = args["tf"]

    df = pd.read_csv(f"./data/{symbol}/{tf}/final_{tf}.csv")

    verify_df(df)