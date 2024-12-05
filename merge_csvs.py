import argparse
import glob
import os
import re

import pandas as pd


def merge(path: str, useless_columns: list[str] = (), output_file: str = "final.csv", start_month="", end_month=""):
    files = glob.glob(os.path.join(path, "*.csv"))
    files = sorted(files)
    columns = ["Open time", "Open", "High", "Low", "Close", "Volume", "Close time", "Quote asset volume",
               "Number of trades", "Taker buy base asset volume", "Taker buy quote asset volume", "Ignore"]
    dfs = []
    # merge method: read all csv files, save the dataframes to an array and then use pd.concat to merge them
    # the loop below is the reading data part
    for file in files:
        # skip result file
        if file.find(output_file) != -1:
            continue

        date_match = re.search(r'\d{4}-\d{2}', file)
        date = date_match.group() if date_match else ""

        if date < start_month or date > end_month:
            continue

        print("processing file: ", file)
        df = pd.read_csv(file)
        # file has no column header, so we must add one before remove them
        df.columns = columns
        df.drop(columns=useless_columns,
                inplace=True)

        dfs.append(df)

        df.to_csv(file, index=False,
                  columns=["Open time", "Open", "High", "Low", "Close", "Close time"])

    # actually merge data happens here
    df = pd.concat(dfs, ignore_index=True)
    df.to_csv(os.path.join(path, output_file), index=False,
              columns=["Open time", "Open", "High", "Low", "Close", "Close time"])


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("symbol", type=str, choices=["bnb", "eth", "btc", "matic"])
    ap.add_argument("tf", type=str, choices=["1m", "15m", "1h", "4h", "1d"])
    ap.add_argument("--start", type=str, required=False,
                    help="string indicate starting year and month of the merge, must be in the form yyyy-mm")
    ap.add_argument("--end", type=str, required=False,
                    help="string indicate ending year and month of the merge, must be in the form yyyy-mm")

    args = vars(ap.parse_args())

    symbol = args["symbol"]
    tf = args["tf"]
    start_month = args["start"]
    end_month = args["end"]

    useless_columns = ["Volume",
                       "Quote asset volume",
                       "Number of trades",
                       "Taker buy base asset volume",
                       "Taker buy quote asset volume",
                       "Ignore"]

    merge(f"./data/{symbol}/{tf}", useless_columns=useless_columns, output_file=f"final_{tf}.csv",
          start_month=start_month, end_month=end_month)
