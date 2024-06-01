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

def should_buy_today(symbol, exchange_id='kucoin'):
    # Berechnen des Durchschnittspreises der letzten 360 Tage
    average_price_last_360_days = get_average_price(symbol, exchange_id)

    # Erhalten des aktuellen Schließkurses
    exchange_class = getattr(ccxt, exchange_id)
    exchange = exchange_class()
    ticker = exchange.fetch_ticker(symbol)
    current_close_price = ticker['close']

    # Prüfen, ob der aktuelle Schließkurs höher ist als der Durchschnittspreis der letzten 360 Tage
    if current_close_price > average_price_last_360_days:
        print(f"Kaufempfehlung für {symbol}: Der aktuelle Schließkurs ({current_close_price}) ist höher als der Durchschnittspreis der letzten 360 Tage ({average_price_last_360_days}).")
        return True
    else:
        print(f"Keine Kaufempfehlung für {symbol}: Der aktuelle Schließkurs ({current_close_price}) ist nicht höher als der Durchschnittspreis der letzten 360 Tage ({average_price_last_360_days}).")
        return False

# Verwenden der Funktion, um zu entscheiden, ob heute gekauft werden soll
should_buy = should_buy_today('BTC/USDT')
