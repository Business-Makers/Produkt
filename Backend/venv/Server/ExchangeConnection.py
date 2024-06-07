from fastapi import FastAPI, Depends, HTTPException
from schemas import ApiKeyCreation, AcoountPages_Info_Validate
from models import Api, AccountPages_Info
import ccxt

def getBalance_numberofCurrencies(exchange):
    balance = exchange.fetchBalance()
    if 'USDT' in balance['total']:
        usdt_balance = balance['total']['USDT']
        print(f"Ihr USDT-Kontoguthaben auf KuCoin: {usdt_balance}")
    total_balances = balance['total']
    non_zero_currencies = {currency: amount for currency, amount in total_balances.items() if amount > 0}
    number_of_currencies = len(non_zero_currencies)

    return usdt_balance, number_of_currencies
