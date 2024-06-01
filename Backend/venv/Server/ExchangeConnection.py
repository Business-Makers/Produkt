from fastapi import FastAPI, Depends, HTTPException
from schemas import ApiKeyCreation
import ccxt


def connect_to_exchange(exchange_info: ApiKeyCreation):
    """
      Connects to a cryptocurrency exchange using the provided API key information.

      Args:
          exchange_info (ApiKeyCreation): An object containing the necessary information to connect to the exchange.
              - exchange_id (str): The identifier of the exchange (e.g., 'binance', 'kraken').
              - api_key (str): The API key for the exchange.
              - api_secret (str): The API secret for the exchange.
              - api_passphrase (str): The API passphrase for the exchange, if required.

      Returns:
          ccxt.Exchange: An instance of the exchange class from the ccxt library, initialized with the provided API key information.

      Raises:
          HTTPException: If there is an error during the connection to the exchange. The exception will have a status code of 400 and will include the error message.
      """
    try:
        exchange_class = getattr(ccxt, exchange_info.exchange_id)
        exchange = exchange_class({
            'apiKey': exchange_info.api_key,
            'secret': exchange_info.api_secret,
            'password': exchange_info.api_passphrase,
        })
        return exchange
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
