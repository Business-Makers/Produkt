import requests

# Ihr CoinMarketCap API-Schlüssel
api_key = 'cbaddffd-6adb-4cb4-81fa-7cb8421b5011'

# URL zur Abrufung der Top 100 Kryptowährungen
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
    'start':'1',
    'limit':'100',
    'convert':'USD'
}
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': api_key,
}

try:
    # API-Anfrage senden
    response = requests.get(url, headers=headers, params=parameters)
    data = response.json()

    # Überprüfen Sie, ob die Anfrage erfolgreich war
    if response.status_code == 200:
        # Die Daten der Top 100 Kryptowährungen befinden sich in data['data']
        for crypto in data['data']:
            name = crypto['name']
            symbol = crypto['symbol']
            rank = crypto['cmc_rank']
            print(f"Rang {rank}: {name} ({symbol})")

    else:
        print(f"Fehler bei der API-Anfrage. Statuscode: {response.status_code}")

except Exception as e:
    print(f"Fehler: {e}")
