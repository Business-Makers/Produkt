from fastapi import FastAPI, Depends, HTTPException
from schemas import ApiKeyCreation, AcoountPages_Info_Validate
from models import Api, AccountPages_Info
import ccxt

def getBalance_numberofCurrencies(exchange):
    balance = exchange.fetchBalance()
    if 'USDT' in balance['total']:
        usdt_balance = balance['total']['USDT']
        print(f"Ihr USDT-Kontoguthaben auf KuCoin: {usdt_balance}")
    non_zero_currencies = {currency: amount for currency, amount in total_balances.items() if amount > 0}
    number_of_currencies = len(non_zero_currencies)

    return usdt_balance, number_of_currencies

def connect_to_exchange(exchange_info: ApiKeyCreation, jwtcode: String):
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
        if exchange_info.passphrase:
            exchange_class = getattr(ccxt, exchange_info.exchange_id)
            exchange = exchange_class({
                'apiKey': exchange_info.api_key,
                'secret': exchange_info.api_secret,
                'password': exchange_info.api_passphrase,
            })
        else:
            exchange_class = getattr(ccxt, exchange_info.exchange_id)
            exchange = exchange_class({
                'apiKey': exchange_info.api_key,
                'secret': exchange_info.api_secret,
            })
        try:
            usdt_balance, number_of_currencies  = getBalance_numberofCurrencies(exchange)
            new_ApiKeyCreation = API(
                api_name= exchange_info.api_name,
                key= exchange_info.api_key,
                secret_Key=exchange_info.secret_key,
                passphrase=exchange_info.passphrase,
                accountID=jwtcode.accountID
            )
            session.add(new_ApiKeyCreation)
            session.commit()
            balanceof ,number_of_currencies = getBalance_numberofCurrencies(exchange)

            new_AccountPages_info = AccountPages_Info(
                balance= balanceof,
                currency_count=number_of_currencies,
                api_id= new_ApiKeyCreation.api_id,
            )
            session.add(new_AccountPages_info)
            session.commit()
            session.close()
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
