import json
import os
import re
import sys

import requests
from bs4 import BeautifulSoup

URL = "https://thepaan.co.kr/board/watch"
BASE = "https://thepaan.co.kr"
SEEN_FILE = "seen.json"
TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]


def fetch_items():
    r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    items = {}
    for a in soup.select('a[href*="/listings/"]'):
        m = re.search(r"/listings/([0-9a-f]{12})", a["href"])
        if not m:
            continue
        text = a.get_text(" ", strip=True)
        price = re.search(r"([\d,]+)\s*원", text)
        if not price:
            continue
        title = text[price.end():]
        title = re.sub(r"\s*(끌올\s*\d+회)?\s*조회수.*$", "", title).strip()
        items[m.group(1)] = {
            "title": title,
            "price": price.group(1) + "원",
            "sold": text.startswith("판매완료"),
            "url": BASE + a["href"] if a["href"].startswith("/") else a["href"],
        }
    return items


def send(text):
    r = requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": text},
        timeout=30,
    )
    r.raise_for_status()


def main():
    items = fetch_items()
    if not items:
        sys.exit("매물을 하나도 못 가져옴 (HTML 구조 바뀌었는지 확인)")

    first_run = not os.path.exists(SEEN_FILE)
    seen = set()
    if not first_run:
        with open(SEEN_FILE, encoding="utf-8") as f:
            seen = set(json.load(f))

    if not first_run:
        for id_, it in items.items():
            if id_ in seen or it["sold"]:
                continue
            send(f"🆕 {it['title']}\n💰 {it['price']}\n{it['url']}")

    seen |= set(items)
    with open(SEEN_FILE, "w", encoding="utf-8") as f:
        json.dump(sorted(seen), f)


if __name__ == "__main__":
    main()
