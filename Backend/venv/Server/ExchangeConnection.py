import ccxt
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import Api, AccountPages_Info

class ExchangeConnection:
    def __init__(self, db: Session):
        self.db = db
        self.__exchange = None
        self.exchange_info = None

    def create_exchange_instance(self, exchange_info):
        self.exchange_info = exchange_info  # Store exchange_info when creating the instance
        exchange_config = {
            'apiKey': exchange_info.api_key,
            'secret': exchange_info.api_secret,
        }
        if exchange_info.passphrase:
            exchange_config['password'] = exchange_info.api_passphrase
        exchange_class = getattr(ccxt, exchange_info.exchange_id)
        self.__exchange = exchange_class(exchange_config)
        return self.__exchange

    def create_api_key(self, payload):
        try:
            new_ApiKey = Api(
                api_name=self.exchange_info.api_name,
                key=self.exchange_info.key,
                secret_key=self.exchange_info.secret_key,
                passphrase=self.exchange_info.passphrase,
                accountID=payload.get("account_id")
            )
            self.db.add(new_ApiKey)
            self.db.commit()
            self.db.refresh(new_ApiKey)
            return new_ApiKey
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    def fetch_and_store_account_info(self, new_ApiKey):
        balanceofaccount, number_of_currencies = self.get_balance_and_currency_count()
        try:
            new_accountpages_info = AccountPages_Info(
                balance=balanceofaccount,
                currency_count=number_of_currencies,
                api_id=new_ApiKey.api_id,
            )
            self.db.add(new_accountpages_info)
            self.db.commit()
            return new_accountpages_info
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    def get_balance_and_currency_count(self):
        try:
            balance = self.__exchange.fetchBalance()
            usdt_balance = balance['total'].get('USDT', -1)
            total_balances = balance['total']
            non_zero_currencies = {currency: amount for currency, amount in total_balances.items() if amount > 0}
            number_of_currencies = len(non_zero_currencies)
            return usdt_balance, number_of_currencies
        except Exception as e:
            print(f"Error fetching balance: {e}")
            return None, 0

    def get_exchange(self):
        return self.__exchange
