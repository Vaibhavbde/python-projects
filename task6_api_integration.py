# ============================================================
# Level 2 - Task 3: API Integration
# Codveda Python Development Internship
#
# Fetches live weather data from Open-Meteo (free, no API key)
# and live crypto prices from CoinGecko (free, no API key).
#
# Install dependency:
#   pip install requests
# ============================================================

import sys
from datetime import datetime

try:
    import requests
except ImportError:
    sys.exit("[Error] 'requests' not installed.\nRun: pip install requests")

TIMEOUT = 10   # seconds

# ── Weather ──────────────────────────────────────────────────

def get_coordinates(city_name):
    """Use Open-Meteo geocoding to resolve a city name to lat/lon."""
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city_name, "count": 1, "language": "en", "format": "json"}
    resp = requests.get(url, params=params, timeout=TIMEOUT)
    resp.raise_for_status()
    data = resp.json()
    results = data.get("results")
    if not results:
        raise ValueError(f"City '{city_name}' not found.")
    r = results[0]
    return r["latitude"], r["longitude"], r.get("name", city_name), r.get("country", "")

def get_weather(city_name):
    """Fetch current weather for a city using Open-Meteo."""
    lat, lon, resolved_city, country = get_coordinates(city_name)
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude":  lat,
        "longitude": lon,
        "current":   "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
        "timezone":  "auto",
    }
    resp = requests.get(url, params=params, timeout=TIMEOUT)
    resp.raise_for_status()
    data = resp.json()

    current = data.get("current", {})
    wmo_codes = {
        0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
        45: "Foggy", 48: "Icy fog", 51: "Light drizzle", 53: "Drizzle",
        55: "Heavy drizzle", 61: "Light rain", 63: "Rain", 65: "Heavy rain",
        71: "Light snow", 73: "Snow", 75: "Heavy snow", 80: "Rain showers",
        85: "Snow showers", 95: "Thunderstorm", 99: "Thunderstorm with hail",
    }
    code = current.get("weather_code", 0)
    condition = wmo_codes.get(code, f"Code {code}")

    print(f"\n{'='*45}")
    print(f"  🌍  Weather — {resolved_city}, {country}")
    print(f"{'='*45}")
    print(f"  Condition   : {condition}")
    print(f"  Temperature : {current.get('temperature_2m', 'N/A')} °C")
    print(f"  Humidity    : {current.get('relative_humidity_2m', 'N/A')} %")
    print(f"  Wind speed  : {current.get('wind_speed_10m', 'N/A')} km/h")
    print(f"  Updated     : {current.get('time', 'N/A')}")
    print(f"{'='*45}")

# ── Crypto prices ────────────────────────────────────────────

COINS = ["bitcoin", "ethereum", "binancecoin", "solana", "cardano"]

def get_crypto_prices():
    """Fetch live prices for top coins from CoinGecko."""
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids":           ",".join(COINS),
        "vs_currencies": "usd",
        "include_24hr_change": "true",
    }
    resp = requests.get(url, params=params, timeout=TIMEOUT)
    resp.raise_for_status()
    data = resp.json()

    print(f"\n{'='*50}")
    print(f"  💰  Cryptocurrency Prices (USD)")
    print(f"  Source: CoinGecko  |  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}")
    print(f"  {'Coin':<14} {'Price (USD)':>14}  {'24h Change':>10}")
    print(f"  {'-'*44}")
    for coin in COINS:
        info = data.get(coin, {})
        price  = info.get("usd", "N/A")
        change = info.get("usd_24h_change", None)
        change_str = f"{change:+.2f}%" if change is not None else "N/A"
        arrow = "▲" if (change or 0) >= 0 else "▼"
        price_str = f"${price:,.2f}" if isinstance(price, (int, float)) else price
        print(f"  {coin.capitalize():<14} {price_str:>14}  {arrow} {change_str:>8}")
    print(f"{'='*50}")

# ── Entry point ───────────────────────────────────────────────

def main():
    print("=" * 50)
    print("     API Integration — Weather & Crypto")
    print("=" * 50)
    print("\nWhat would you like to fetch?")
    print("  1. Current weather for a city")
    print("  2. Live cryptocurrency prices")
    print("  3. Both")
    print("  4. Exit")

    choice = input("\nYour choice (1-4): ").strip()

    if choice in ("1", "3"):
        city = input("Enter city name: ").strip()
        try:
            get_weather(city)
        except ValueError as e:
            print(f"[Error] {e}")
        except requests.exceptions.ConnectionError:
            print("[Error] No internet connection or the weather API is unreachable.")
        except requests.exceptions.HTTPError as e:
            print(f"[Error] HTTP error from weather API: {e}")

    if choice in ("2", "3"):
        try:
            get_crypto_prices()
        except requests.exceptions.ConnectionError:
            print("[Error] No internet connection or the CoinGecko API is unreachable.")
        except requests.exceptions.HTTPError as e:
            print(f"[Error] HTTP error from crypto API: {e}")

    if choice == "4":
        print("Goodbye!")

    if choice not in ("1", "2", "3", "4"):
        print("Invalid choice.")

if __name__ == "__main__":
    main()
