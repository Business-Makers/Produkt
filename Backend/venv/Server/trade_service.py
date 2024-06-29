import ccxt
from sqlalchemy.orm import Session
from models import Api, Trade, TakeProfit
from utils import verify_trade_token
from fastapi import HTTPException, FastAPI
from datetime import datetime
import logging

logging.basicConfig(filename='trade_debug.log', level=logging.WARNING, format='%(asctime)s %(levelname)s:%(message)s')
logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)
logging.getLogger('sqlalchemy.pool').setLevel(logging.ERROR)
logging.getLogger('sqlalchemy.dialects').setLevel(logging.ERROR)
logging.getLogger('sqlalchemy.orm').setLevel(logging.ERROR)
logging.getLogger('sqlalchemy.engine.Engine').setLevel(logging.ERROR)

logger = logging.getLogger(__name__)
class TradeService:
    """
        Service class to handle trade-related operations.

        Args:
            db (Session): Database session.
            authorization (str): Authorization token.
        """


    def __init__(self, db: Session, authorization: str):
        """
                Initialize TradeService with database session and authorization token.

                Args:
                    db (Session): Database session.
                    authorization (str): Authorization token.
                """
        self.db = db
        self.authorization = authorization
        self.account_id = self._get_account_id_from_token()
        self.api_key = self._get_api_key()
        self.api_id = None

    def _get_account_id_from_token(self):
        """
                Extract account ID from the authorization token.

                Raises:
                    HTTPException: If the authorization token is missing or invalid.

                Returns:
                    int: Account ID.
                """
        if self.authorization is None:
            raise HTTPException(status_code=401, detail="jalli halloAuthorization header missing or invalid.")
        token = self.authorization.split(" ")[1]
        payload = verify_trade_token(token)
        if payload is None:
            raise HTTPException(status_code=401, detail="Invalid or expired token",
                                headers={"WWW-Authenticate": "Bearer"})
        return payload.get("account_id")

    def get_api_id(self, order):
        """
                Get the API ID for a given order.

                Args:
                    order: The order object containing exchange name.

                Raises:
                    HTTPException: If the API is not found for the given exchange name.

                Returns:
                    int: API ID.
                """
        apiID = None
        api_name = order.exchangeName
        account_apis = self.db.query(Api).filter(Api.accountID == self.account_id).all()
        for a in account_apis:
            if a.exchange_name == api_name:
                apiID = a.api_id
                return apiID
        raise HTTPException(status_code=404, detail=f"API named '{api_name}' not found.")

    def _get_api_key(self):
        """
               Get the API key for the account.

               Raises:
                   HTTPException: If the API key is not found for the account.

               Returns:
                   Api: API key object.
               """
        api_key = self.db.query(Api).filter(Api.accountID == self.account_id).first()
        if not api_key:
            raise HTTPException(status_code=404, detail="API key not found for the account")
        return api_key

    def _get_exchange_instance(self):
        """
                Get the exchange instance using ccxt.

                Returns:
                    ccxt.Exchange: Exchange instance.
                """
        exchange_class = getattr(ccxt, self.api_key.exchange_name)
        exchange_args = {
            'apiKey': self.api_key.key,
            'secret': self.api_key.secret_Key
        }
        if self.api_key.passphrase:
            exchange_args['password'] = self.api_key.passphrase
        return exchange_class(exchange_args)

    def has_sufficient_usdt_balance(self, required_amount):
        """
                Check if the account has sufficient USDT balance.

                Args:
                    required_amount (float): The required amount of USDT.

                Raises:
                    HTTPException: If there's an error fetching the balance.

                Returns:
                    bool: True if sufficient balance, otherwise False.
                """
        try:
            exchange = self._get_exchange_instance()
            balance = exchange.fetch_balance()
            usdt_balance = balance['free'].get('USDT', 0)
            return usdt_balance >= required_amount
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching balance: {str(e)}")

    def create_order(self, order):
        """
                Create a new order.

                Args:
                    order: The order object containing order details.

                Raises:
                    HTTPException: If there's an error creating the order.

                Returns:
                    dict: The created order details.
                """
        try:
            logger.warning("Erstelle Bestellung: %s", order)
            if not self.has_sufficient_usdt_balance(order.amount * order.price):
                logger.warning("Unzureichender USDT-Bestand für Bestellung: %s", order)
                raise HTTPException(status_code=400, detail="Insufficient USDT balance")

            exchange = self._get_exchange_instance()
            order_params = {
                'order_type': order.order_type
            }
            created_order = None
            if order.order_type == 'market':
                additional_params = {
                    'symbol': order.symbol,
                    'side': order.side,
                    'amount': order.amount,
                    # 'take_profit_price': order.take_profit_prices,
                    # 'stop_loss_price': order.stop_loss_prices,
                    #'params': {'timeInForce': 'GTC'}
                }
                order_params.update(additional_params)
                logger.warning("vor exchange create market order")
                created_order = exchange.create_market_order(**additional_params)
                date_bought = datetime.now().date()
                logger.warning("Market-Bestellung erstellt: %s", created_order)

            elif order.order_type == 'limit':
                additional_params = {
                    'symbol': order.symbol,
                    'side': order.side,
                    'amount': order.amount,
                    #'price': order.price,
                    # 'stop_price': order.stop_price,
                    # 'take_profit_price': order.take_profit_prices,
                    # 'stop_loss_price': order.stop_loss_prices,
                    #'params': {'timeInForce': 'GTC'}
                }
                order_params.update(additional_params)
                logger.warning("vor exchange create limit order")
                created_order = exchange.create_limit_order(**additional_params)
                date_bought = None
                logger.warning("Limit-Bestellung erstellt: %s", created_order)
            else:
                logger.warning("Ungültiger Bestelltyp: %s", order.order_type)
                raise HTTPException(status_code=400, detail="Invalid order type")
            new_trade = None
            api_id = self.get_api_id(order)
            if order.order_type == 'market':
                new_trade = Trade(
                    trade_price=0,
                    trade_type=order.order_type,
                    currency_name=order.symbol,
                    currency_volume=order.amount,
                    trade_status=created_order['status'],
                    date_create=datetime.now().date(),
                    date_bought=date_bought,
                    api_id=api_id
                )
            if order.order_type == 'limit':
                new_trade = Trade(
                    trade_price=order.price,
                    trade_type=order.order_type,
                    currency_name=order.symbol,
                    currency_volume=order.amount,
                    trade_status=created_order['status'],
                    date_create=datetime.now().date(),
                    date_bought=None,
                    api_id=api_id
                )
            self.db.add(new_trade)
            self.db.commit()
            self.db.refresh(new_trade)
            logger.warning("Neuer Trade in der Datenbank gespeichert: %s", new_trade)

            # Optionally add Take-Profit and Stop-Loss orders
            if order.take_profit_prices:
                self.add_take_profits(new_trade.trade_id, order.take_profit_prices)
                logger.warning("Take-Profit-Aufträge hinzugefügt: %s", order.take_profit_prices)
            if order.stop_loss_price:
                self.add_stop_loss(new_trade.trade_id, order.stop_loss_price)
                logger.warning("Stop-Loss-Auftrag hinzugefügt: %s", order.stop_loss_price)

            return {"message": "Order created successfully", "order": created_order}
        except HTTPException as e:
            logger.warning("HTTP-Fehler bei der Bestellungserstellung: %s", e.detail)
            raise e
        except Exception as e:
            logger.warning("Interner Serverfehler bei der Bestellungserstellung")
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

    def add_take_profits(self, trade_id, take_profit_prices):
        """
                Add Take-Profit orders.

                Args:
                    trade_id (int): The trade ID.
                    take_profit_prices (list): List of Take-Profit prices.

                Raises:
                    HTTPException: If there's an error adding Take-Profit orders.

                Returns:
                    dict: Details of the added Take-Profit orders.
                """
        try:
            trade = self.db.query(Trade).filter(Trade.trade_id == trade_id).first()
            if not trade:
                raise HTTPException(status_code=404, detail="Trade not found")

            exchange = self._get_exchange_instance()

            response = []
            for price in take_profit_prices:
                take_profit_order = exchange.create_order(
                    symbol=trade.currency_name,
                    type='take_profit_market',
                    side='sell' if trade.trade_status == 'open' else 'buy',
                    amount=trade.currency_volume / len(take_profit_prices),  # Aufteilen des Volumens
                    params={'stopPrice': price, 'reduceOnly': True}
                )
                new_take_profit = TakeProfit(trade_id=trade_id, price=price)
                self.db.add(new_take_profit)
                response.append(take_profit_order)

            self.db.commit()
            return {"message": "Take-Profit orders added successfully", "take_profit_orders": response}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

    def add_stop_loss(self, trade_id, stop_loss_price):
        """
                Add Stop-Loss order.

                Args:
                    trade_id (int): The trade ID.
                    stop_loss_price (float): The Stop-Loss price.

                Raises:
                    HTTPException: If there's an error adding the Stop-Loss order.

                Returns:
                    dict: Details of the added Stop-Loss order.
                """
        try:
            trade = self.db.query(Trade).filter(Trade.trade_id == trade_id).first()
            if not trade:
                raise HTTPException(status_code=404, detail="Trade not found")

            exchange = self._get_exchange_instance()

            stop_loss_order = exchange.create_order(
                symbol=trade.currency_name,
                type='stop_market',
                side='sell' if trade.trade_status == 'open' else 'buy',
                amount=trade.currency_volume,
                params={'stopPrice': stop_loss_price, 'reduceOnly': True}
            )

            trade.stop_loss_price = stop_loss_price
            self.db.commit()

            return {"message": "Stop-Loss order added successfully", "stop_loss_order": stop_loss_order}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Server Error: {str(e)}")

    def add_take_profit_and_stop_loss(self, trade_id, take_profit_prices, stop_loss_price, comment):
        """
            Add Take-Profit and Stop-Loss orders and update trade with a comment.

            Args:
                trade_id (int): The trade ID.
                take_profit_prices (list): List of Take-Profit prices.
                stop_loss_price (float): The Stop-Loss price.
                comment (str): Comment to add to the trade.

            Raises:
                HTTPException: If there's an error adding the orders or updating the comment.

            Returns:
                dict: Success message.
            """
        try:

            if take_profit_prices:
                self.add_take_profits(trade_id, take_profit_prices)

            if stop_loss_price:
                self.add_stop_loss(trade_id, stop_loss_price)

            if comment:
                trade = self.db.query(Trade).filter(Trade.trade_id == trade_id).first()
                trade.comment = comment
                self.db.commit()
                self.db.refresh(trade)

            return {"message": "Take-profit, stop-loss orders and Comment added successfully"}
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

    def calculate_profit_loss_amount(self, trade_id: int) -> float:
        """
            Calculate the profit or loss amount for a trade.

            Args:
                trade_id (int): The trade ID.

            Raises:
                HTTPException: If the trade is not found or purchase rate is not set.

            Returns:
                float: Profit or loss amount.
            """
        trade = self.db.query(Trade).filter(Trade.trade_id == trade_id).first()
        if not trade:
            raise HTTPException(status_code=404, detail="Trade not found")

        if trade.purchase_rate is None:
            raise HTTPException(status_code=400, detail="Purchase rate not set for the trade")

        exchange = self._get_exchange_instance()
        ticker = exchange.fetch_ticker(trade.currency_name)
        current_price = ticker['last']

        profit_loss_amount = (current_price - trade.purchase_rate) * trade.currency_volume

        return profit_loss_amount

    def calculate_profit_loss_percentage(self, trade_id: int) -> float:
        """
            Calculate the profit or loss percentage for a trade.

            Args:
                trade_id (int): The trade ID.

            Raises:
                HTTPException: If the trade is not found or purchase rate is not set.
                ValueError: If the purchase rate is zero.

            Returns:
                float: Profit or loss percentage.
            """
        trade = self.db.query(Trade).filter(Trade.trade_id == trade_id).first()
        if not trade:
            raise HTTPException(status_code=404, detail="Trade not found")

        if trade.purchase_rate is None:
            raise HTTPException(status_code=400, detail="Purchase rate not set for the trade")

        exchange = self._get_exchange_instance()
        ticker = exchange.fetch_ticker(trade.currency_name)
        current_price = ticker['last']

        if trade.purchase_rate == 0:
            raise ValueError("Purchase rate cannot be zero")

        profit_loss_percentage = ((current_price - trade.purchase_rate) / trade.purchase_rate) * 100
        return profit_loss_percentage

    def complete_trade(self, trade_id: int):
        """
            Complete a trade by canceling open orders and calculating profit/loss.

            Args:
                trade_id (int): The trade ID.

            Raises:
                HTTPException: If the trade is not found or there's an error canceling orders or updating the trade.

            Returns:
                dict: Success message with profit/loss amount and percentage.
            """
        trade = self.db.query(Trade).filter(Trade.trade_id == trade_id).first()
        if not trade:
            raise HTTPException(status_code=404, detail="Trade not found")

        exchange = self._get_exchange_instance()

        # Cancel all open Take-Profit and Stop-Loss orders
        for take_profit in trade.take_profits:
            try:
                exchange.cancel_order(take_profit.order_id, trade.currency_name)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error cancelling Take-Profit order: {str(e)}")

        if trade.stop_loss_price:
            try:
                exchange.cancel_order(trade.stop_loss_order_id, trade.currency_name)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error cancelling Stop-Loss order: {str(e)}")

        # Calculate profit/loss
        profit_loss_amount = self.calculate_profit_loss_amount(trade_id)
        profit_loss_percentage = self.calculate_profit_loss_percentage(trade_id)

        trade.selling_rate = profit_loss_amount
        trade.date_sale = datetime.now()
        trade.purchase_rate = profit_loss_percentage
        self.db.commit()

        return {
            "message": "Trade completed successfully",
            "profit_loss_amount": profit_loss_amount,
            "profit_loss_percentage": profit_loss_percentage
        }


    def check_and_update_limit_orders(self):
        """
            Check and update limit orders by setting the date bought if closed.

            Returns:
                None
            """
        trades = self.db.query(Trade).filter(Trade.trade_type == 'limit', Trade.date_bought == None).all()
        exchange = self._get_exchange_instance()

        for trade in trades:
            try:
                order = exchange.fetch_order(trade.trade_id, trade.currency_name)
                if order['status'] == 'closed':
                    trade.date_bought = datetime.now()
                    self.db.commit()
            except Exception as e:
                print(f"Error checking order {trade.trade_id}: {str(e)}")

    def update_stop_loss_and_take_profits(self, trade_id: int, new_stop_loss_price: float,
                                          new_take_profit_prices: list):
        """
            Update Stop-Loss and Take-Profit orders for a trade.

            Args:
                trade_id (int): The trade ID.
                new_stop_loss_price (float): The new Stop-Loss price.
                new_take_profit_prices (list): List of new Take-Profit prices.

            Raises:
                HTTPException: If there's an error updating the orders.

            Returns:
                dict: Success message.
            """
        try:
            trade = self.db.query(Trade).filter(Trade.trade_id == trade_id).first()
            if not trade:
                raise HTTPException(status_code=404, detail="Trade not found")

            exchange = self._get_exchange_instance()

            # Update Stop-Loss order
            if new_stop_loss_price:
                # Cancel existing Stop-Loss order if it exists
                if trade.stop_loss_price:
                    try:
                        open_orders = exchange.fetch_open_orders(symbol=trade.currency_name)
                        for order in open_orders:
                            if order['type'] == 'stop_market' and order['price'] == trade.stop_loss_price:
                                exchange.cancel_order(order['id'], trade.currency_name)
                    except Exception as e:
                        raise HTTPException(status_code=500,
                                            detail=f"Error cancelling existing Stop-Loss order: {str(e)}")

                # Create new Stop-Loss order
                stop_loss_order = exchange.create_order(
                    symbol=trade.currency_name,
                    type='stop_market',
                    side='sell' if trade.trade_status == 'open' else 'buy',
                    amount=trade.currency_volume,
                    params={'stopPrice': new_stop_loss_price, 'reduceOnly': True}
                )
                trade.stop_loss_price = new_stop_loss_price

            # Update Take-Profit orders
            if new_take_profit_prices:
                # Cancel existing Take-Profit orders if they exist
                try:
                    open_orders = exchange.fetch_open_orders(symbol=trade.currency_name)
                    for order in open_orders:
                        if order['type'] == 'take_profit_market' and order['price'] in [tp.price for tp in
                                                                                        trade.take_profits]:
                            exchange.cancel_order(order['id'], trade.currency_name)
                    for take_profit in trade.take_profits:
                        self.db.delete(take_profit)
                except Exception as e:
                    raise HTTPException(status_code=500,
                                        detail=f"Error cancelling existing Take-Profit orders: {str(e)}")

                # Create new Take-Profit orders
                for price in new_take_profit_prices:
                    take_profit_order = exchange.create_order(
                        symbol=trade.currency_name,
                        type='take_profit_market',
                        side='sell' if trade.trade_status == 'open' else 'buy',
                        amount=trade.currency_volume / len(new_take_profit_prices),  # Aufteilen des Volumens
                        params={'stopPrice': price, 'reduceOnly': True}
                    )
                    new_take_profit = TakeProfit(trade_id=trade_id, price=price)
                    self.db.add(new_take_profit)

            self.db.commit()
            self.db.refresh(trade)

            return {"message": "Stop-Loss and Take-Profit orders updated successfully"}
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


    def update_trade_with_profit_loss(self, trade_id: int):
        """
            Update trade with profit/loss information if Take-Profit or Stop-Loss is reached.

            Args:
                trade_id (int): The trade ID.

            Raises:
                HTTPException: If the trade is not found or there's an error updating the trade.
                ValueError: If the purchase rate is zero.

            Returns:
                dict: Success message with profit/loss amount and percentage.
            """
        try:
            trade = self.db.query(Trade).filter(Trade.trade_id == trade_id).first()
            if not trade:
                raise HTTPException(status_code=404, detail="Trade not found")

            if trade.purchase_rate is None:
                raise HTTPException(status_code=400, detail="Purchase rate not set for the trade")

            exchange = self._get_exchange_instance()
            ticker = exchange.fetch_ticker(trade.currency_name)
            current_price = ticker['last']

            # Check if Take-Profit or Stop-Loss was reached
            take_profit_reached = any(tp.price <= current_price for tp in trade.take_profits)
            stop_loss_reached = trade.stop_loss_price and trade.stop_loss_price >= current_price

            if take_profit_reached or stop_loss_reached:
                # Calculate profit/loss amount
                profit_loss_amount = (current_price - trade.purchase_rate) * trade.currency_volume
                trade.selling_rate = profit_loss_amount

                # Calculate profit/loss percentage
                if trade.purchase_rate == 0:
                    raise ValueError("Purchase rate cannot be zero")
                profit_loss_percentage = ((current_price - trade.purchase_rate) / trade.purchase_rate) * 100
                trade.purchase_rate = profit_loss_percentage

                # Update trade status and date_sale
                trade.trade_status = 'closed'
                trade.date_sale = datetime.now()

                self.db.commit()
                self.db.refresh(trade)

                return {
                    "message": "Trade updated with profit/loss successfully",
                    "profit_loss_amount": profit_loss_amount,
                    "profit_loss_percentage": profit_loss_percentage
                }
            else:
                return {"message": "No Take-Profit or Stop-Loss reached"}
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

    def cancel_order(self, order_id: str, symbol: str):
        """
            Cancel an open order.

            Args:
                order_id (str): The order ID.
                symbol (str): The trading pair symbol.

            Raises:
                HTTPException: If there's an error canceling the order.

            Returns:
                dict: Success message with order details.
            """
        try:
            exchange = self._get_exchange_instance()
            canceled_order = exchange.cancel_order(order_id, symbol)
            return {"message": "Order canceled successfully", "order": canceled_order}
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
