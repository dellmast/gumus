"""Gram gümüş (TL) takipçisi: her saat başı ve her 1 TL artışta Telegram'dan haber verir."""
import json
import os
import urllib.parse
import urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo

STATE_FILE = "state.json"
STEP_TL = 1.0                  # kaç TL artışta bildirim gelsin
OUNCE_GRAMS = 31.1034768       # 1 troy ons = kaç gram
TZ = ZoneInfo("Europe/Istanbul")


def get_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "silver-bot"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def gram_silver_try():
    xag_usd = get_json("https://api.gold-api.com/price/XAG")["price"]
    usd_try = get_json("https://open.er-api.com/v6/latest/USD")["rates"]["TRY"]
    return xag_usd / OUNCE_GRAMS * usd_try


def send(text):
    token = os.environ["TELEGRAM_BOT_TOKEN"].strip()
   chat_id = os.environ["TELEGRAM_CHAT_ID"].strip()
    data = urllib.parse.urlencode({"chat_id": chat_id, "text": text}).encode()
    urllib.request.urlopen(
        f"https://api.telegram.org/bot{token}/sendMessage", data=data, timeout=20
    ).read()


def load_state():
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def main():
    price = gram_silver_try()
    hour_key = datetime.now(TZ).strftime("%Y-%m-%d %H")
      grams = float((os.environ.get("GRAMS") or "0").strip() or 0)

    def price_text(p):
        text = f"Gram gümüş: {p:.2f} TL"
        if grams:
            text += f"\nToplam değer ({grams:g} g): {p * grams:,.0f} TL"
        return text

    state = load_state()
    old_state = dict(state)

    # İlk çalıştırma: başlangıç noktasını kaydet
    if not state:
        state = {"anchor": price, "hour_key": hour_key, "hour_price": price}
        send("✅ Gümüş takibi başladı.\n" + price_text(price))
        save_state(state)
        return

    lines = []

    # 1 TL artış kontrolü (referans fiyat düşüşü takip eder, yükselişte 1 TL aşılınca bildirim gelir)
    if price >= state["anchor"] + STEP_TL:
        lines.append(f"📈 {price - state['anchor']:.2f} TL arttı")
        state["anchor"] = price
    elif price < state["anchor"]:
        state["anchor"] = price

    # Saat başı kontrolü
    if hour_key != state["hour_key"]:
        diff = price - state["hour_price"]
        sign = "+" if diff >= 0 else ""
        lines.append(f"🕘 Saatlik özet (son saate göre {sign}{diff:.2f} TL)")
        state["hour_key"] = hour_key
        state["hour_price"] = price

    if lines:
        send("\n".join(lines) + "\n" + price_text(price))

    if state != old_state:
        save_state(state)


if __name__ == "__main__":
    main()
