import os
import json
import requests
from bs4 import BeautifulSoup

URL = "https://thepaan.co.kr/board/watch"

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

DATA_FILE = "seen.json"


def get_seen():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    except:
        return set()


def save_seen(seen):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(list(seen), f, ensure_ascii=False)


def send_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": text,
            "disable_web_page_preview": False,
        },
        timeout=20,
    )


def get_posts():
    r = requests.get(
        URL,
        headers={
            "User-Agent": "Mozilla/5.0"
        },
        timeout=20,
    )

    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    posts = []

    for a in soup.find_all("a", href=True):
        href = a.get("href", "")

        if "/writing/" not in href:
            continue

        title = a.get_text(" ", strip=True)

        if not title:
            continue

        posts.append({
            "url": href if href.startswith("http") else "https://thepaan.co.kr" + href,
            "title": title,
        })

    return posts


def main():
    seen = get_seen()
    posts = get_posts()

    current = set()

    for post in posts:
        current.add(post["url"])

        if post["url"] not in seen:
            send_telegram(
                "🔔 더판 새 판매글\n\n"
                + post["title"]
                + "\n\n"
                + post["url"]
            )

    save_seen(current)


if __name__ == "__main__":
    main()
