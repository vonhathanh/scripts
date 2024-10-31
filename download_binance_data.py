import argparse
import os
import logging
import urllib.request
import urllib.error
import requests
from zipfile import ZipFile

DEFAULT_URL = "https://data.binance.vision/data/futures/um/monthly/markPriceKlines/"
logging.basicConfig(level=logging.INFO, encoding='utf-8')


def download_monthly_volume(token: str, tf: str, save_dir: str = ""):
    """
    Download historic price for 1 token pair
    :param save_dir: directory we want to save that data in disk
    :param tf: time frame
    :param token: name of the token
    """
    if save_dir:
        data_dir = save_dir
    else:
        data_dir = f"./data/{token}/{tf}"  # default directory is ./data/token name/time frame

    os.makedirs(data_dir, exist_ok=True)

    # download data from most recent n years
    # this could be parameterized, but I'm too lazy
    for year in range(2020, 2025):
        # months go from 1 to 12
        months = range(1, 13)
        for month in months:
            try:
                # need to add "0" padding to months that smaller than October
                month = "0" + str(month) if month < 10 else month

                full_url = f"{DEFAULT_URL}{token.upper()}USDT/{tf}/{token.upper()}USDT-{tf}-{year}-{month}.zip"

                filename = f"{data_dir}/{token}_{year}-{month}.zip"

                logging.info(f"download url is: {full_url}")

                response = requests.get(full_url)
                # save file
                if response.status_code == 200:
                    with open(filename, "wb") as f:
                        f.write(response.content)
                else:
                    logging.error(f"something's wrong with the response, {response.content}")
                    continue
                # unzip file
                with ZipFile(filename, 'r') as zp:
                    zp.extractall(data_dir)
                    zp.printdir()
            except Exception as e:
                logging.info(f"Error at token: {token}, date: {month}-{year}, error: {e}")


def main(args: dict):
    symbol = args["symbol"]
    tf = args["tf"]
    save_dir = args["save_dir"]

    download_monthly_volume(symbol, tf, save_dir)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("symbol", type=str, choices=["bnb", "eth", "btc", "matic"])
    ap.add_argument("tf", type=str, choices=["1m", "15m", "1h", "4h", "1d"])
    ap.add_argument("--save_dir", type=str, required=False)

    args = vars(ap.parse_args())

    main(args)