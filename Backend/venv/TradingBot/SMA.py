import ccxt
import pandas as pd
from datetime import datetime, timedelta


def get_average_price(symbol, exchange_id='binance', days=360):
    # Erstellen eines Exchange-Objekts
    exchange_class = getattr(ccxt, exchange_id)
    exchange = exchange_class()

    # Berechnen des Datums 360 Tage zurück
    since = int((datetime.now() - timedelta(days=days)).timestamp()) * 1000

    # Abrufen der OHLCV-Daten (Open, High, Low, Close, Volume)
    ohlcv = exchange.fetch_ohlcv(symbol, '1d', since)

    # Umwandeln der Daten in ein DataFrame
    df = pd.DataFrame(ohlcv, columns=['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])
    df['Date'] = pd.to_datetime(df['Timestamp'], unit='ms')

    # Berechnen des Durchschnittspreises
    average_price = df['Close'].mean()

    return average_price


# Verwenden der Funktion, um den Durchschnittspreis für BTC/USDT auf Binance zu berechnen
average_price_btc_usdt = get_average_price('BTC/USDT')
print(f'Durchschnittspreis von BTC/USDT auf Binance über die letzten 360 Tage: {average_price_btc_usdt:.2f} USDT')
