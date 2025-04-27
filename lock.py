import os
import sys
import time
import web3
import json
import string
import random
import requests
import ua_generator
from datetime import datetime, timedelta
from eth_account.messages import encode_defunct
from base64 import b64decode


def log(msg):
    now = datetime.now().isoformat(" ").split(".")[0]
    print(f"[{now}] {msg}")


def ipinfo(ses):
    try:
        res = http(ses=ses, url="https://api64.ipify.org")
        log(f"ip proxy : {res.text}")
    except:
        log("ip proxy : None")


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
            if (
                not os.path.exists("http.log")
                or os.path.getsize("http.log") / 1024 > 1024
            ):
                open("http.log", "a")
            open("http.log", "a").write(f"{res.status_code} {res.text}\n")
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
            log("connection error !")
            attemp += 1


def lock(privatekey, proxy=None):
    ses = requests.Session()
    ip = ipinfo(ses=ses)
    wallet = web3.Account.from_key(privatekey)
    address = wallet.address
    log(f"addr : {address}")
    data_lock = {
        "userId": "67975c953d8d8ab4310ed8af",
        "restakePoints": 480655,
        "sign": "0x7f7d7e4af7bb8945597eef4c1d4e4a9830377fef5c74c72f6bf7724a4eaf203d0c004762e538d7d02cd5a99e16371df42e360f6b9cd2cead705b560a676cb0291b",
        "timestamp": "1745657510009",
        "captchaToken": "03AFcWeA52dyLAIHTqCl1DDYtCPQEqJC5oTCi6rrlGjCrhqbfTM1SUh25a6_wgKx19PYQXT8bdmPCfK5jaEDIM5pYX9oi5XX7v2CSYig5b9EhH1FmaF2JIndjEeJRPHoTT2-hRlWrpCrG4CgOUYK9H53Y6vk1w51SkucFDs-D8_owMNE4szaBMic5ishkfj6Ttum0qi7DJlVc8KtWYLW6-uE_5OLuIiFNFwEf71q-dJdN34XjWc-QicSo7BaYvzbLrmbd34szDQkCLET2Ui9Wzl4g0i2Vpickua2zfgo1vJuv0A5QeRq_qNdmzogCJ83_9MjQRLKj7mwf_3Rnq9ukqO0Rj3o7ID-Xr_SJCFKYWPBD_pUTyyjcvF_mKFtoExpxZMJMY3ZlWNxBk6H5u7TVhUBUPxM_dRjvO_p77RWD2K7SSPVVR37zcFbUq7tZkCEWZ_S-2wqUkWVqqLmA8jSD4HGULas23nOEydJ4xoTfzDEqtG_FW5avjBwqXDPgPUjh5qtqtJx8UPgesIAu-j3Y8fH0Gryu5a9sDtKkGXsIi6Vgz3Uasny1pQ-llhMCJmoSaXcs7giTQiqbjyh-S8coYCS7TqfG-tV7YBOVXDYeXWGy585Hrb5KemcklieLXf4wZKOYw7X6mrdCrltS_9QClDAF1wYCc7nWxU2s2X0P6MWXjtMT0hA6ZX_U_wdSHQmkYLHokT4BV1UwIoGT7W0f0rbfY2RosvxW1Km8rqX64q-erd7XYu91PcUU92BTcp2jqSlgZTmA68QIipYWtOgk8xVuHc1Lw3G818zuD1LXo6pf72cPF3WSIPC8p8l3w2tOBHZX1MWifElH64BUgXoOPDY9BJiA88dz7LBXsasWMu5mfS64dbbeA4j79eyQ3Bpj6Qf5RTcidwblE_dFpstziEkQxVci177GOUzb5LzukC8ZOziTL-Q7yjnNF2Fq-RSH2juc95hQXme31Suyb30Pts4icbQfrwT2Sob_yrGPMpeSos8vOIHgWjnO2DgYJ7QJ6JiAYhhvEi64Xi-CGT18G6PtITFPNu3t0vHDezSmVOArDT6zwPMKO15E0Zil46p-cixuA0ShMRGt1deZG8Gx3IZ90VxMLhAofu2czHZOAygWvgVy836iNA5eu7WMlI6CAWTvFcvYIgJ4FR2QIIYIPULVH-m7FMELAHLmCGMNnPUfLbL6lY1M0w5RKDoAOcP6FjuCeoK8WG2QV_N3x0S0WAVRx_ei_lhaGj8Ux17CXP6f_CN1fPJZz0auW5lya2-vAbyw6XYSdvlXAXOQJcgJqKxQ_BiQxUiIYkw8PSofA5MXMDwxzJoeYngTSBRA7xOUS9VJjxzBeLhC7Y3eZKBq1aNMHOfAaw_izTgsRdrfF2p_bhicxARw_QLE4aEWmYHQ-SGTtJ3TjFwuBLTVZ6YMH4EPoNbpoRwMxYeaH0IjBOG28e4DYa3T51C48kaNHTx7O7C2tz0fA9r-6guNZiYTFCAsJNmUr7k6WWRd07gfhBh6oYrmMU_0usLw3fkrk35w3Tj63RSVKmfYJJ_oDgsR0FVSWM2ZFnN9iAwGR1aLTXWHgeeVKGRnP5z2qKQu477iV_GgZrJKQ9i96orTTMSineqtdlnbjtZoFY_GguE9ARNWL0nYeN4hZEmRHulPJVnrVfCaHZXAkhKHHSrRuEfs3JbwwHqfDTZkZ9QYCGmaCw1LSB48sGAvVixiKlBagYN_26TB3UlZvwQpbH13_Xo8vRh3lDyRsTqDr-ShDny4wDGFx61r_jfB2qF54YLMJioxojnjfSFUPNPWm5hCwVCsnfUV1tWy7WPuLzWfMv7rrB8RNwXfYXiAFgaL1a1mv1bf5arrDdz6ZZ8BZ-FBjB37_YuOQ94zOgA2b4vaDj0BWGwF8_B6J3q_ry7q4jPN6ENdcF-cB8no58tBw8rU1EqAJ-akiliK6thLwiH9Zys8h475HMBZqpfHo_1AqUlTAny3Xc9mzUV1yn-l9l1GcTQhVCex9Dgkg7Sf_ixowBYycdnHxSQdV5OH47awfKJ9MJv4_RKUBZU2vdnxSbSIi7OwHc-gdHi1U2cbpwgMaMcVCRhbYtG8KiumLDBO2aZANEPf9bAGYqLchrB-gll7vW38xvNyjVjEnbi2vimXgBAjfJDTkvQmeRO5VfBg3QkdB-3DrWHselSIpRQP7nCDuDJS6nWIgqqu3ha3AN5e_71DktGk8BruLtD-ufxo",
    }
    restake_url = "https://api.layeredge.io/api/epoch/restake-previous-epoch-points"
    wallet_detail_url = (
        f"https://api.layeredge.io/api/referral/wallet-details/{address}"
    )
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Host": "api.layeredge.io",
        "Origin": "https://dashboard.layeredge.io",
        "Referer": "https://dashboard.layeredge.io/",
        "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    }
    ses.headers.update(headers)
    ses.proxies.update({"http": proxy, "https": proxy})
    res = http(ses=ses, url=wallet_detail_url)
    userid = res.json().get("data", {}).get("id")
    poh_point = res.json().get("data", {}).get("pohPoints")
    if poh_point <= 0:
        log("not eligible for phase 1 & 2.")
    else:
        log("eligible for phase 1 & 2.")
        return True
    data_lock["userId"] = userid
    timestamp_now = int(datetime.now().timestamp() * 1000)
    data_lock["timestamp"] = str(timestamp_now)
    epoch_status_url = f"https://api.layeredge.io/api/epoch/epoch-stats/{userid}"
    res = http(ses=ses, url=epoch_status_url)
    total_point = res.json().get("data", {}).get("totalPoints")
    restake_point = res.json().get("data", {}).get("restakePoints")
    log(f"total point : {total_point}")
    if restake_point == total_point:
        log("already stake/lock point !")
        return True
    data_lock["restakePoints"] = total_point
    message_sign = (
        f"locking my points for my wallet {wallet.address} and {timestamp_now}"
    )
    encode_message_sign = encode_defunct(text=message_sign)
    sign = web3.Web3.to_hex(
        web3.Account.sign_message(encode_message_sign, private_key=wallet.key).signature
    )
    data_lock["sign"] = sign
    ses2 = requests.Session()
    headers2 = {
        "User-Agent": "SdsProject/7.7.7",
        "Connection": "keep-alive",
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded",
        "group": "t.me/sdsproject",
        "my-istri": "marinkitagawa",
    }
    ses2.headers.update(headers2)
    try:
        res = http(ses=ses2, url="https://tempgooglev3.sdsproject.org/", data="")
        error = res.json().get("error")
        token = res.json().get("token")
    except:
        log("failed get google captcha token !")
        return None
    if error is not None:
        log("failed get google captcha token !")
        return None
    data_lock["captchaToken"] = token
    ses.headers.update({"Content-Type": "application/json"})
    # print(data)
    res = http(ses=ses, url=restake_url, data=json.dumps(data_lock))
    message = res.json().get("message")
    if message == "Previous Epoch Points restaked successfully":
        log("success stake point !")
        return True
    else:
        log("failed stake point !")
        return False


def main():
    print("""
>
> Auto Stake Point Layeredge
> Join t.me/sdsproject
>
        """)

    pks = open("privatekeys.txt").read().splitlines()
    proxies = open("proxies.txt").read().splitlines()
    print(f"total privatekey : {len(pks)}")
    print(f"total proxy : {len(proxies)}")
    print()
    if len(pks) <= 0:
        print("total privatekey is 0, exit !")
        sys.exit()
    p = 0
    for pk in pks:
        print("~" * 50)
        proxy = None if len(proxies) <= 0 else proxies[p % len(proxies)]
        result = lock(privatekey=pk, proxy=proxy)
        if result:
            p += 1



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
