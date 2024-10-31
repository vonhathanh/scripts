import argparse
import os
import glob
import pandas as pd


def merge(path: str, useless_columns: list[str] = (), output_file: str = "final.csv"):
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
    df.to_csv(os.path.join(path, output_file), index=False, columns=["Open time", "Open", "High", "Low", "Close", "Close time"])


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("symbol", type=str, choices=["bnb", "eth", "btc", "matic"])
    ap.add_argument("tf", type=str, choices=["1m", "15m", "1h", "4h", "1d"])

    args = vars(ap.parse_args())

    symbol = args["symbol"]
    tf = args["tf"]

    useless_columns = ["Volume",
                       "Quote asset volume",
                       "Number of trades",
                       "Taker buy base asset volume",
                       "Taker buy quote asset volume",
                       "Ignore"]

    merge(f"./data/{symbol}/{tf}", useless_columns=useless_columns, output_file=f"final_{tf}.csv")