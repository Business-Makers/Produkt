from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from schemas import ApiKeyCreation
import ccxt
import time


def connect_to_exchange(exchange_info: ApiKeyCreation):
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
