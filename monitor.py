import os
import re
import json
import requests
from bs4 import BeautifulSoup

URL = "https://thepaan.co.kr/board/watch"
BASE = "https://thepaan.co.kr"

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

DATA_FILE = "seen.json"
LISTING = re.compile(r"/listings/([0-9a-f]{12})/")


def get_seen():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def save_seen(seen):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(seen[:1000], f, ensure_ascii=False)


def send_telegram(text):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": text},
        timeout=20,
    ).raise_for_status()


def get_posts():
    r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    posts = {}
    for a in soup.find_all("a", href=True):
        m = LISTING.search(a["href"])
        if not m:
            continue
        text = a.get_text(" ", strip=True)
        if not text or m.group(1) in posts:
            continue
        href = a["href"]
        posts[m.group(1)] = {
            "text": text,
            "url": href if href.startswith("http") else BASE + href,
        }
    return posts


def main():
    posts = get_posts()
    if not posts:
        raise SystemExit("매물을 0개 찾음 - 사이트 구조 확인 필요")

    seen = get_se
