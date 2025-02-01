#
# read the readme.
#

import os
import sys
import web3
import json
import string
import random
import requests
import ua_generator
from datetime import datetime
from eth_account.messages import encode_defunct
from base64 import b64decode


def log(msg):
    now = datetime.now().isoformat(" ").split(".")[0]
    print(f"[{now}] {msg}")


def http(ses: requests.Session, url, data=None):
    attemp = 0
    while True:
        try:
            if attemp == 3:
                return None
            if data is None:
                res = ses.get(url=url)
            elif data == "":
                res = ses.post(url=url)
            else:
                res = ses.post(url=url, data=data)
            if "<title>502 Bad Gateway</title>" in res.text:
                log("error : 502 bad gateway !")
                time.sleep(3)
                continue
            if "<title>504 Gateway Time-out</title>" in res.text:
                log("error : 504 gateway timeout !")
                time.sleep(3)
                continue
            return res
        except (
            requests.exceptions.ConnectTimeout,
            requests.exceptions.ConnectionError,
            requests.exceptions.ReadTimeout,
            requests.exceptions.ProxyError,
        ):
            log(f"connection error !")
            attemp += 1


class Referral:
    def __init__(self, proxy):
        proxy = {"http": proxy, "https": proxy}
        self.ses = requests.Session()
        self.ses.proxies.update(proxy)
        headers = {
            "user-agent": ua_generator.generate().text,
        }

        self.ses.headers.update(headers)
        # self.wallet = eth_account.Account.create()
        self.wallet = web3.Account.create()
        self.hostname = b64decode("bGF5ZXJlZGdlLmlv").decode()

    def start(self, referral_code):
        try:
            res = http(ses=self.ses, url="https://ipv4.webshare.io")
            if res is None:
                return
            log(f"register with ip {res.text}")
            self.ses.headers.update(
                {
                    "host": f"referralapi.{self.hostname}",
                    "connection": "keep-alive",
                    "sec-ch-ua-platform": '"Windows"',
                    "accept": "application/json, text/plain, */*",
                    "content-type": "application/json",
                    "sec-ch-ua-mobile": "?0",
                    "origin": f"https://dashboard.{self.hostname}",
                    "sec-fetch-site": "same-site",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-dest": "empty",
                    "referer": f"https://dashboard.{self.hostname}/",
                    "accept-language": "en-US,en;q=0.9",
                }
            )
            verify_referral_code_url = (
                f"https://referralapi.{self.hostname}/api/referral/verify-referral-code"
            )

            data = {"invite_code": referral_code}
            res = http(
                ses=self.ses, url=verify_referral_code_url, data=json.dumps(data)
            )
            if res is None:
                return None
            if res.status_code != 200:
                log(f"http code : {res.status_code}")
                log(f"http response : {res.text}")
                return None
            if not res.json().get("data", {}).get("valid"):
                log("referral code is not valid !")
                log(f"http response : {res.text}")
                return None
            register_url = f"https://referralapi.{self.hostname}/api/referral/register-wallet/{referral_code}"
            data = {"walletAddress": self.wallet.address}
            res = http(ses=self.ses, url=register_url, data=json.dumps(data))
            if res is None:
                return None
            if not "registered wallet address successfully" in res.json().get(
                "message"
            ):
                log("failed register !")
                log(f"http response : {res.text} ")
                return None
            log("success register !")
            privatekey = f"0x{self.wallet.key.hex()}"
            with open("privatekeys.txt", "a") as w:
                w.write(f"{privatekey}\n")
            ref_code = res.json().get("data", {}).get("referralCode")
            node_status_url = f"https://referralapi.{self.hostname}/api/light-node/node-status/{self.wallet.address}"
            res = http(ses=self.ses, url=node_status_url)
            if res is None:
                return None
            start_time = res.json().get("data", {}).get("startTimestamp")
            if start_time is None:
                start_url = f"https://referralapi.{self.hostname}/api/light-node/node-action/{self.wallet.address}/start"
                timet = int(datetime.now().timestamp() * 1000)
                message = (
                    f"Node activation request for {self.wallet.address} at {timet}"
                )
                enmessage = encode_defunct(text=message)
                sign = web3.Account.sign_message(enmessage, private_key=self.wallet.key)
                signature = f"0x{sign.signature.hex()}"
                data = {
                    "sign": signature,
                    "timestamp": timet,
                }
                res = http(ses=self.ses, url=start_url, data=json.dumps(data))
                if res is None:
                    return None
                if not "node action executed successfully" in res.json().get("message"):
                    log(f"failed start node !")
                    log(f"http response : {res.text}")
                    return None
                log("success start node !")
                return True
            log("node already started !")
            return True
        except Exception as e:
            log(f"error : {e}")
            return None


def get_proxy(i, p):
    if len(p) <= 0:
        return None
    proxy = p[i % len(p)]
    return proxy


def main():
    os.system("cls" if os.name == "nt" else "clear")
    print(">\n> auto referrral l a y e r e d g e !\n>")
    print()
    proxies = open("proxies.txt").read().splitlines()
    print(f"total proxy : {len(proxies)}")
    referral_code = input("input referral code : ")
    total_referral = input("input total referral : ")
    if len(proxies) <= 0:
        q = input(f"Do you want to continue without a proxy? [y/n] ")
        if q.lower() == "n":
            sys.exit()
    print()
    for i in range(int(total_referral)):
        proxy = get_proxy(i, proxies)
        Referral(proxy=proxy).start(referral_code=referral_code)
        print("~" * 50)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
