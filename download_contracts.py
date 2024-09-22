"""
Downloads all contracts from an Ethereum-like address using Etherscan API
"""
import argparse
import json
import os.path

import requests

URL = {
    "eth": "api.etherscan.io",
    "polygon": "api.polygonscan.io"
}

DOWNLOAD_URL = "https://{url}/api?module=contract&action=getsourcecode&address={address}&apikey={apikey}"

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("address",)
    parser.add_argument("network")
    parser.add_argument("apikey")
    parser.add_argument("--out_dir", help="output path (relative with current dir), default = ./out",
                        default="./out")

    args = vars(parser.parse_args())

    address = args["address"]
    network = args["network"]
    apikey = args["apikey"]
    out_dir = args["out_dir"]

    url = DOWNLOAD_URL.format(url=URL[network], address=address, apikey=apikey)

    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"download contract failed, reason: {response.reason}")

    data = json.loads(response.text)["result"][0]

    sources = json.loads(data["SourceCode"][1:-1])["sources"]

    os.makedirs(out_dir, exist_ok=True)

    for key, codes in sources.items():

        full_path = key.split("/")

        path, name = "/".join(full_path[0:-1]), full_path[-1]

        dest_path = os.path.join(out_dir, path)

        os.makedirs(dest_path, exist_ok=True)

        with open(os.path.join(dest_path, name), "w", encoding="utf-8") as f:
            f.write(codes["content"])
