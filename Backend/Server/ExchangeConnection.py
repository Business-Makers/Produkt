import ccxt
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import Api, AccountPages_Info
import logging

logging.basicConfig(filename='debugAll.log', level=logging.WARNING, format='%(asctime)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)


class ExchangeConnection:
    """
        A class to manage connections and operations with cryptocurrency exchanges using ccxt.
        """

    def __init__(self, db: Session):
        """
                Initialize the ExchangeConnection with a database session.

                Args:
                    db (Session): SQLAlchemy session for database operations.
                """
        self.db = db
        self.__exchange = None
        self.exchange_info = None

    def create_exchange_instance(self, exchange_info):
        """
                Create an instance of the exchange using provided exchange information.

                Args:
                    exchange_info: An object containing exchange configuration details such as API key, secret, and passphrase.

                Returns:
                    An instance of the exchange class.
                """

        self.exchange_info = exchange_info  # Store exchange_info when creating the instance
        exchange_config = {
            'apiKey': exchange_info.api_key,
            'secret': exchange_info.api_secret,
        }
        if exchange_info.passphrase:
            exchange_config['password'] = exchange_info.api_passphrase
        exchange_class = getattr(ccxt, exchange_info.exchange_name)
        self.__exchange = exchange_class(exchange_config)
        return self.__exchange

    def create_api_key(self, payload):
        """
                Create a new API key entry in the database.

                Args:
                    payload (dict): A dictionary containing the account ID.

                Returns:
                    The newly created Api object.

                Raises:
                    HTTPException: If there is an error during the database transaction.
                """
        try:
            new_ApiKey = Api(
                api_name=self.exchange_info.exchange_name,
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
        """
                Fetch account balance information from the exchange and store it in the database.

                Args:
                    new_ApiKey: The Api object containing API key information.

                Returns:
                    The newly created AccountPages_Info object.

                Raises:
                    HTTPException: If there is an error during the database transaction.
                """
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
        """
                Retrieve the balance and the number of non-zero currency balances from the exchange.

                Returns:
                    tuple: A tuple containing the USDT balance and the number of non-zero currency balances.

                Prints:
                    An error message if there is an issue fetching the balance.
                """
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
        """
                Get the current exchange instance.

                Returns:
                    The exchange instance.
                """
        return self.__exchange
