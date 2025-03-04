import argparse
import glob
import os
import re

import pandas as pd


final_columns = ["Open time", "Open", "High", "Low", "Close", "Close time"]
columns = ["Open time", "Open", "High", "Low", "Close", "Volume", "Close time", "Quote asset volume",
               "Number of trades", "Taker buy base asset volume", "Taker buy quote asset volume", "Ignore"]


def is_header(strings: list[str]) -> bool:
    # header is a list of strings that can't be parsed to integer
    try:
        int(strings[0])
    except ValueError:
        return True
    return False


def merge(path: str, output_file: str = "final.csv", start_month="", end_month=""):

    files = glob.glob(os.path.join(path, "*.csv"))
    files = sorted(files)

    dfs = []
    # merge method: read all csv files, save the dataframes to an array and then use pd.concat to merge them
    # the loop below is the reading data part
    for file in files:
        # skip result file
        if file.find(output_file) != -1:
            continue

        date_match = re.search(r'\d{4}-\d{2}', file)
        date = date_match.group() if date_match else ""

        if (start_month and date < start_month) or (end_month and date > end_month):
            continue

        print("processing file: ", file)

        with open(file, "r") as f:
            first_line = f.readline().strip().split(",")

        if is_header(first_line):
            df = pd.read_csv(file)
        else:
            df = pd.read_csv(file, names=columns)
        # assign columns header for files that doesn't have the header
        df.columns = columns
        dfs.append(df)

    # actually merge data happens here
    df = pd.concat(dfs, ignore_index=True)

    # df may contains redundant columns so columns=final_columns is required
    df.to_csv(os.path.join(path, output_file), index=False, columns=final_columns)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("symbol", type=str, choices=["bnb", "eth", "btc", "matic"])
    ap.add_argument("tf", type=str, choices=["1m", "15m", "1h", "4h", "1d"])
    ap.add_argument("--start", type=str, required=False, default="",
                    help="string indicate starting year and month of the merge, must be in the form yyyy-mm")
    ap.add_argument("--end", type=str, required=False,
                    default="",
                    help="string indicate ending year and month of the merge, must be in the form yyyy-mm")

    args = vars(ap.parse_args())

    symbol = args["symbol"]
    tf = args["tf"]
    start_month = args["start"]
    end_month = args["end"]

    merge(f"./data/{symbol}/{tf}", output_file=f"final_{tf}.csv",
          start_month=start_month, end_month=end_month)
