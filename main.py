import requests
import random
from typing import Union, Dict, List, Any


def generate_vcard() -> List[str]:
    dummy_datas = fetch_dummy_data()
    vcard = []
    for dummy_data in dummy_datas:
        vcard.append(make_vcard(dummy_data["first_name"], dummy_data["last_name"], dummy_data["phone_number"], dummy_data["address"]))

    return vcard

def fetch_dummy_data() -> List[Dict[str, str]]:
    session = requests.Session()
    res = session.get("https://testdata.userlocal.jp/", headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0"})
    authenticity_token = res.text.split("name=\"authenticity_token\" value=\"")[1].split("\" autocomplete")[0]

    payload = {
        "authenticity_token": authenticity_token,
        "button": "",
        "dummy[filetype]": "csv",
        "dummy[lines]": random.randint(10, 30),
        "dummy[fields][]": [
            "name",
            "mobile_phone_number",
            "address"
        ],
        "dummy[name][char][]": [
            "kanji",
            "hiragana"
        ],
        "dummy[name][delimiter]": "han",
        "dummy[age][lower_limit]": "19",
        "dummy[age][upper_limit]": "50",
        "dummy[birthday][delimiter]": "ja",
        "dummy[gender][fmt]": "ja_s",
        "dummy[company][lower_limit]": "0",
        "dummy[company][upper_limit]": "0",
        "dummy[company][employed_ratio]": "0"
    }
    dummy_csv = session.post(
        "https://testdata.userlocal.jp/dummy",
        headers={
            "Accept-Encoding": "gzip",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0",
            "Content-Type": "application/x-www-form-urlencoded"
        },
        data=payload
    ).content.decode("utf-8-sig").splitlines()[1:]

    dummy = []
    for dummy_line in dummy_csv:
        dummy_ = dummy_line.split("\"")
        dummy.append({
            "first_name": dummy_[1].split(" ")[0],
            "last_name": dummy_[1].split(" ")[1],
            "phone_number": dummy_[5],
            "address": dummy_[7]
        })
        
    # print(dummy)
    return dummy


def make_vcard(first_name: str, last_name: str, phone: str, address: str) -> List[str]:
    address_formatted = ';'.join([p.strip() for p in address.split(',')])
    return [
        'BEGIN:VCARD',
        'VERSION:2.1',
        f'N:{last_name};{first_name}',
        f'FN:{first_name} {last_name}',
        # f'ORG:',
        # f'TITLE:',
        # f'EMAIL;PREF;INTERNET:',
        f'TEL;MAIN;VOICE:{phone}',
        f'ADR;MAIN;PREF:;;{address_formatted}',
        f'REV:1',
        'END:VCARD'
    ]


if __name__ == "__main__":
    result = generate_vcard()
    with open("./output.vcf", "w", encoding="utf-8") as f:
        for data in result:
            f.writelines([i + "\n" for i in data])

    print("done")
    input()

