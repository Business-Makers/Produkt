import ccxt
from sqlalchemy.orm import Session
from models import Api, Trade, TakeProfit
from utils import verify_trade_token
from fastapi import HTTPException
from datetime import datetime


class TradeService:
    def __init__(self, db: Session, authorization: str):
        self.db = db
        self.authorization = authorization
        self.account_id = self._get_account_id_from_token()
        self.api_key = self._get_api_key()

    def _get_account_id_from_token(self):
        if self.authorization is None:
            raise HTTPException(status_code=401, detail="jalli halloAuthorization header missing or invalid.")
        token = self.authorization.split(" ")[1]
        payload = verify_trade_token(token)
        if payload is None:
            raise HTTPException(status_code=401, detail="Invalid or expired token",
                                headers={"WWW-Authenticate": "Bearer"})
        return payload.get("account_id")

    def _get_api_key(self):
        api_key = self.db.query(Api).filter(Api.accountID == self.account_id).first()
        if not api_key:
            raise HTTPException(status_code=404, detail="API key not found for the account")
        return api_key

    def _get_exchange_instance(self):
        exchange_class = getattr(ccxt, self.api_key.exchange_name)
        exchange_args = {
            'apiKey': self.api_key.key,
            'secret': self.api_key.secret_Key
        }
        if self.api_key.passphrase:
            exchange_args['password'] = self.api_key.passphrase
        return exchange_class(exchange_args)

    def has_sufficient_usdt_balance(self, required_amount):
        try:
            exchange = self._get_exchange_instance()
            balance = exchange.fetch_balance()
            usdt_balance = balance['free'].get('USDT', 0)
            return usdt_balance >= required_amount
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching balance: {str(e)}")

    def create_order(self, order):
        try:
            if not self.has_sufficient_usdt_balance(order.amount * order.price):
                raise HTTPException(status_code=400, detail="Insufficient USDT balance")

            exchange = self._get_exchange_instance()
            order_params = {
                'order_type': order.order_type
            }

            if order.order_type == 'market':
                additional_params = {
                    'symbol': order.symbol,
                    'side': order.side,
                    'amount': order.amount,
                    #'take_profit_price': order.take_profit_prices,
                    #'stop_loss_price': order.stop_loss_prices,
                    'params': {'timeInForce': 'GTC'}
                }
                order_params.update(additional_params)
                created_order = exchange.create_market_order(**additional_params)
                date_bought = datetime.now()

            elif order.order_type == 'limit':
                additional_params = {
                    'symbol': order.symbol,
                    'side': order.side,
                    'amount': order.amount,
                    'price': order.price,
                    #'stop_price': order.stop_price,
                    #'take_profit_price': order.take_profit_prices,
                    #'stop_loss_price': order.stop_loss_prices,
                    'params': {'timeInForce': 'GTC'}
                }
                order_params.update(additional_params)
                created_order = exchange.create_limit_order(**additional_params)
                date_bought = None
            else:
                raise HTTPException(status_code=400, detail="Invalid order type")

            if order.order_type == 'market':
                new_trade = Trade(
                    trade_type=order.order_type,
                    currency_name=order.symbol,
                    currency_volume=order.amount,
                    trade_status=created_order['status'],
                    date_create=created_order['timestamp'],
                    date_bought=date_bought,
                    api_id=order.
                )
            self.db.add(new_trade)
            self.db.commit()
            self.db.refresh(new_trade)

            # Optionally add Take-Profit and Stop-Loss orders
            if order.take_profit_prices:
                self.add_take_profits(new_trade.trade_id, order.take_profit_prices)
            if order.stop_loss_price:
                self.add_stop_loss(new_trade.trade_id, order.stop_loss_price)

            return {"message": "Order created successfully", "order": created_order}
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

    def add_take_profits(self, trade_id, take_profit_prices):
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

    # todo: AnnaSabr =>laufen lassen
    def check_and_update_limit_orders(self):
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

    # todo: AnnaSabr =>laufen lassen
    def update_trade_with_profit_loss(self, trade_id: int):
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
        try:
            exchange = self._get_exchange_instance()
            canceled_order = exchange.cancel_order(order_id, symbol)
            return {"message": "Order canceled successfully", "order": canceled_order}
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
