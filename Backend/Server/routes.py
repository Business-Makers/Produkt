"""
FastAPI Application File

This file contains the main FastAPI application setup, including endpoint definitions and event handlers.
"""
import asyncio
import json
from datetime import date, timedelta

from fastapi import FastAPI, Depends, HTTPException, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db, init_db
from fastapi.responses import JSONResponse
from models import Account, Member, Api, AccountPages_Info, Trade, TakeProfit, Subscription
from schemas import LoginCredentials, UserRegistration, PasswordResetRequest, ApiKeyCreation, OrderRequest, \
    AddTakeProfitStopLossRequest, UpdateTradeRequest, Subscription_Info, SellRequest
from utils import get_hashed_password, verify_password, create_access_token, generate_reset_token, \
    send_password_reset_email, verify_reset_token, verify_access_token, find_mail, mailTheme, verify_trade_token
from smtp import send_email
from trade_service import TradeService
import ccxt
from web_socket import websocket_endpoint
from background_threading import background_threads
from web_socket import manager
import logging
from paypal import Paypal

logging.basicConfig(filename='trade_debug.log', level=logging.WARNING, format='%(asctime)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()  # creates instance of FastAPI class

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ursprünge
    allow_credentials=True,
    allow_methods=["*"],  # HTTP-Methoden
    allow_headers=["*"],  # HTTP-Header
)

background = background_threads()


@app.on_event("startup")
async def on_startup():
    """
        Event handler function called on application startup.

        This function is automatically called when the FastAPI application starts up.
        It is decorated with `@app.on_event("startup")` to register it as an event handler for the application startup event.
        Inside this function, it calls the `init_db()` function to initialize the database by creating all tables.
        """
    init_db()

    # todo: Background async await


app.websocket("\ws\{user_id}")(websocket_endpoint)


@app.post("/login/")
def login(credentials: LoginCredentials, db: Session = Depends(get_db)):
    """
    Handles user login and password authentication.

    This endpoint authenticates user login credentials.
    It takes the login credentials provided by the user and checks them against the stored hashed password in the database.
    If the credentials are correct, it generates an access token and returns it to the client.

    Parameters:
        - credentials (LoginCredentials): The user's login credentials containing username and password.
        - db (Session, optional): The database session dependency obtained using `Depends(get_db)`.

    Returns:
        dict: A dictionary containing the access token and token type if authentication is successful.

    Raises:
        HTTPException: If the login credentials are incorrect or an internal error occurs.
    """
    try:
        db_user = db.query(Account).filter(Account.login_name == credentials.login_name).first()

        if db_user and verify_password(credentials.password, db_user.hashed_password):
            # Generate token
            account_id = db_user.account_id

            access_token = create_access_token(
                data={"sub": db_user.login_name, "account_id": account_id}
            )

            mailAdress = find_mail(db_user, db)
            if mailAdress:
                # send_email(mailAdress, mailTheme.login.name, db)
                pass
            background.set_authorization(access_token)

            background.start_background_tasks()

            return {"message": "Logged in successfully", "access_token": access_token, "token_type": "bearer"}
        else:
            raise HTTPException(status_code=401, detail="Incorrect username or password")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/register/")
def register(user: UserRegistration, db: Session = Depends(get_db)):
    """
    Handles new user registration.

    This endpoint registers new users.
    It takes the user registration details provided by the client, creates a new member and account in the database,
    and associates them together. It also hashes the user's password before storing it in the database.

    Parameters:
        - user (UserRegistration): The user's registration details containing personal information and login credentials.
        - db (Session, optional): The database session dependency obtained using `Depends(get_db)`.

    Returns:
        dict: A dictionary containing the success message if registration is successful.

    Raises:
        HTTPException: If the phone number, email, or login name is already registered or if an internal error occurs.
    """
    if user.phone_number:
        existing_phone_number = db.query(Member).filter(Member.phone_number == user.phone_number).first()
        if existing_phone_number:
            raise HTTPException(status_code=400, detail="Phone number already registered")

    existing_email = db.query(Member).filter(Member.email == user.eMail).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    existing_user = db.query(Account).filter(Account.login_name == user.login_name).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Login name already registered")

    try:

        new_member = Member(
            firstname=user.firstname,
            lastname=user.lastname,
            birthday=user.birthday,
            email=user.eMail,
            phone_number=user.phone_number,
            address=user.address,
            country=user.country
        )

        db.add(new_member)
        db.commit()
        db.refresh(new_member)

        hashed_password = get_hashed_password(user.password)
        new_account = Account(
            login_name=user.login_name,
            hashed_password=hashed_password,
            memberID=new_member.member_id
        )
        db.add(new_account)
        db.commit()

        send_email(user.eMail, mailTheme.registration.name, db)
        return {"message": "Registration successful! We're excited to have you with us."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def get_balance_and_currency_count(exchange):
    """
        Retrieve the balance and the number of non-zero currency balances from the exchange.

        Parameters:
            - exchange: The exchange instance to fetch the balance from.

        Returns:
            tuple: A tuple containing the USDT balance and the number of non-zero currency balances.

        Prints:
            An error message if there is an issue fetching the balance.
        """
    try:
        balance = exchange.fetchBalance()
        usdt_balance = balance['total'].get('USDT', -1)
        total_balances = balance['total']
        non_zero_currencies = {currency: amount for currency, amount in total_balances.items() if amount > 0}
        number_of_currencies = len(non_zero_currencies)
        return usdt_balance, number_of_currencies
    except Exception as e:
        print(f"Error fetching balance: {e}")
        return None, 0


@app.post("/connect-exchange/")
def connect_exchange(exchange_info: ApiKeyCreation, db: Session = Depends(get_db), authorization: str = Header(None)):
    """
        Connects a user's account to a cryptocurrency exchange using provided API keys.

        This endpoint allows users to connect their account to a cryptocurrency exchange.
        It verifies the provided API keys and retrieves the balance and currency count from the exchange.

        Parameters:
            - exchange_info (ApiKeyCreation): The API key information for the exchange.
            - db (Session, optional): The database session dependency obtained using `Depends(get_db)`.
            - authorization (str): The authorization header containing the Bearer token.

        Returns:
            dict: A dictionary containing a success message and the account information.

        Raises:
            HTTPException: If the authorization header is missing or invalid, the exchange ID is not valid, or an internal error occurs.
        """
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header missing or invalid.")

    token = authorization.split(" ")[1]
    payload = verify_trade_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token", headers={"WWW-Authenticate": "Bearer"})
    account_id = payload.get("account_id")
    existing_user = db.query(Api).filter(Api.secret_Key == exchange_info.secret_key).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Exchange Connection already registered")
    try:
        exchange_class = getattr(ccxt, exchange_info.exchange_name)
        exchange_args = {
            'apiKey': exchange_info.key,
            'secret': exchange_info.secret_key
        }
        if exchange_info.passphrase:
            exchange_args['password'] = exchange_info.passphrase
        exchange = exchange_class(exchange_args)

        new_ApiKey = Api(
            exchange_name=exchange_info.exchange_name,
            key=exchange_info.key,
            secret_Key=exchange_info.secret_key,
            passphrase=exchange_info.passphrase,
            accountID=account_id
        )
        db.add(new_ApiKey)
        db.commit()
        db.refresh(new_ApiKey)

        balance_of_account, number_of_currencies = get_balance_and_currency_count(exchange)

        new_accountpages_info = AccountPages_Info(
            balance=balance_of_account,
            account_holder=exchange_info.account_holder,
            currency_count=number_of_currencies,
            exchange_name=exchange_info.exchange_name,
            api_id=new_ApiKey.api_id
        )
        db.add(new_accountpages_info)
        db.commit()
        db.close()
        return {"message": "Exchange connected successfully"}
    except AttributeError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Exchange ID {exchange_info.exchange_name} is not valid.")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@app.get("/dashboard/")
def get_dashboard(db: Session = Depends(get_db), authorization: str = Header(None)):
    """
        Retrieves the dashboard data for the authenticated user.

        This endpoint fetches the connected exchanges and their balance information for the authenticated user.

        Parameters:
            - db (Session, optional): The database session dependency obtained using `Depends(get_db)`.
            - authorization (str): The authorization header containing the Bearer token.

        Returns:
            dict: A dictionary containing the dashboard data.

        Raises:
            HTTPException: If the authorization header is missing or invalid, or an internal error occurs.
        """
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header missing or invalid.")

    token = authorization.split(" ")[1]
    payload = verify_trade_token(token)
    if payload is None:
        raise HTTPException(status_code=402, detail="Invalid or expired token", headers={"WWW-Authenticate": "Bearer"})
    account_id = payload.get("account_id")

    try:
        api_keys = db.query(Api).filter(Api.accountID == account_id).all()
        dashboard_data = []
        for api_key in api_keys:
            if api_key and api_key.account_pages_info:
                account_holder = api_key.account_pages_info.account_holder
            else:
                raise HTTPException(status_code=403, detail="No account pages info available.")
            exchange_class = getattr(ccxt, api_key.exchange_name)
            exchange_args = {
                'apiKey': api_key.key,
                'secret': api_key.secret_Key
            }
            if api_key.passphrase:
                exchange_args['password'] = api_key.passphrase
            exchange = exchange_class(exchange_args)

            balance_of_account, number_of_currencies = get_balance_and_currency_count(exchange)
            dashboard_data.append({
                "exchange_name": api_key.exchange_name,
                "account_holder": account_holder,
                "balance": balance_of_account,
                "currency_count": number_of_currencies
            })

        return {"dashboard": dashboard_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@app.get("/trades/")
def get_trade(db: Session = Depends(get_db), authorization: str = Header(None)):
    """
    Retrieves all trades for the authenticated user.

    Parameters:
        - db (Session, optional): The database session dependency obtained using `Depends(get_db)`.
        - authorization (str): The authorization header containing the Bearer token.

    Returns:
        dict: A dictionary containing all trades for the authenticated user.

    Raises:
        HTTPException: If the authorization header is missing or invalid, or an internal error occurs.
    """
    try:
        if authorization is None or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Authorization header missing or invalid.")

        token = authorization.split(" ")[1]
        payload = verify_trade_token(token)
        if payload is None:
            raise HTTPException(status_code=402, detail="Invalid or expired token",
                                headers={"WWW-Authenticate": "Bearer"})
        account_id = payload.get("account_id")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Authorization Error: {str(e)}")

    try:
        api_keys = db.query(Api).filter(Api.accountID == account_id).all()
        if not api_keys:
            raise HTTPException(status_code=404, detail="API keys not found for the account")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database Query Error (api_keys): {str(e)}")

    trades_data = []
    try:
        for api_key in api_keys:
            try:
                trades = db.query(Trade).filter(Trade.api_id == api_key.api_id).all()
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Database Query Error (trades): {str(e)}")

            if api_key and api_key.account_pages_info:
                account_holder = api_key.account_pages_info.account_holder
            else:
                raise HTTPException(status_code=403, detail="No account pages info available for API key")

            for trade in trades:
                try:
                    trades_data.append({
                        "account_holder": account_holder,
                        # "exchange_name": api_key.exchange_name,
                        "trade_id": trade.trade_id,
                        "trade_type": trade.trade_type,
                        "trade_price": trade.trade_price,
                        "currency_name": trade.currency_name,
                        "currency_volume": trade.currency_volume,
                        "trade_status": trade.trade_status,
                        "date_create": trade.date_create,
                        "date_bought": trade.date_bought,
                        "date_sale": trade.date_sale,
                        "purchase_rate": trade.purchase_rate,
                        "selling_rate": trade.selling_rate,
                        "comment": trade.comment,
                        "stop_loss_price": trade.stop_loss_price
                        # "take_profits": [{"price": tp.price} for tp in trade.take_profits]
                    })
                except Exception as e:
                    raise HTTPException(status_code=500, detail=f"Error processing trade data: {str(e)}")
            # asyncio.create_task(send_real_time_updates(account_id, db, authorization))
        return {"trades": trades_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


async def send_real_time_updates(account_id: int, db: Session, authorization: str):
    """
        Sends real-time updates of trade prices and selling rates to clients.

        Args:
            account_id (int): The ID of the account.
            db (Session): The database session.
            authorization (str): The authorization token.

        Returns:
            None
        """
    trade_service = TradeService(db, authorization)
    api_keys = db.query(Api).filter(Api.accountID == account_id).all()

    while True:
        for api_key in api_keys:
            trades = db.query(Trade).filter(Trade.api_id == api_key.api_id).all()
            exchange = trade_service._get_exchange_instance()
            for trade in trades:
                ticker = exchange.fetch_ticker(trade.currency_name)
                current_price = ticker['last']
                purchase_rate = trade.purchase_rate
                selling_rate = (current_price - purchase_rate) * trade.currency_volume

                message = {
                    "trade_id": trade.trade_id,
                    "current_price": current_price,
                    "purchase_rate": purchase_rate,
                    "selling_rate": selling_rate
                }

                await manager.broadcast(json.dumps(message), account_id)
        await asyncio.sleep(10)  # Update every 10 seconds


@app.post("/trades/create-order/")
def create_order(order: OrderRequest, db: Session = Depends(get_db), authorization: str = Header(None)):
    """
    Creates a market or limit order, optionally with take-profit and/or stop-loss.

    Parameters:
        - order (OrderRequest): The order details.
        - db (Session, optional): The database session dependency obtained using `Depends(get_db)`.
        - authorization (str): The authorization header containing the Bearer token.

    Returns:
        dict: A dictionary containing the order details if creation is successful.

    Raises:
        HTTPException: If the authorization header is missing or invalid, or an internal error occurs.
    """

    trade_service = TradeService(db, authorization)

    return trade_service.create_order(order)


@app.post("/trades/add-take-profit-stop-loss/")
def add_take_profit_stop_loss(request: AddTakeProfitStopLossRequest, db: Session = Depends(get_db),
                              authorization: str = Header(None)):
    """
    Adds take-profit and/or stop-loss orders to an existing trade.

    Parameters:
        - request (AddTakeProfitStopLossRequest): The request details containing trade ID, take-profit prices, and stop-loss price.
        - db (Session, optional): The database session dependency obtained using `Depends(get_db)`.
        - authorization (str): The authorization header containing the Bearer token.

    Returns:
        dict: A dictionary containing the details of the added orders if successful.

    Raises:
        HTTPException: If the authorization header is missing or invalid, or an internal error occurs.
    """
    trade_service = TradeService(db, authorization)
    return trade_service.add_take_profit_and_stop_loss(request.trade_id, request.take_profit_prices,
                                                       request.stop_loss_price, request.comment)


@app.post("/complete_trade/")
def complete_trade(request: SellRequest, db: Session = Depends(get_db), authorization: str = Header(None)):
    """
        Completes a trade based on the provided trade ID.

        Args:
            trade_id (int): The ID of the trade to be completed.
            db (Session): The database session dependency.
            authorization (str, optional): The authorization token passed in the header.

        Returns:
            dict: A dictionary containing the result of completing the trade.
                  Example:
                  {
                      "success": True,
                      "message": "Trade completed successfully."
                  }
                  or
                  {
                      "success": False,
                      "error": "Error message"
                  }
        """
    logger.warning("pre alles")
    trade_service = TradeService(db, authorization)
    logger.warning(f"tarden {trade_service}")
    result = trade_service.complete_trade(request.trade_id)
    logger.warning(f"result {result}")
    return result


@app.put("/trades/update/")
def update_trade(request: UpdateTradeRequest, db: Session = Depends(get_db), authorization: str = Header(None)):
    """
    Updates the stop-loss and take-profit prices for an existing trade.

    Parameters:
        - request (UpdateTradeRequest): The request details containing trade ID, new stop-loss price, and new take-profit prices.
        - db (Session, optional): The database session dependency obtained using `Depends(get_db)`.
        - authorization (str): The authorization header containing the Bearer token.

    Returns:
        dict: A dictionary containing the details of the updated orders if successful.

    Raises:
        HTTPException: If the authorization header is missing or invalid, or an internal error occurs.
    """
    trade_service = TradeService(db, authorization)
    return trade_service.update_stop_loss_and_take_profits(request.trade_id, request.new_stop_loss_price,
                                                           request.new_take_profit_prices)


@app.delete("/cancel_order/{order_id}")
def cancel_order(order_id: str, symbol: str, db: Session = Depends(get_db), authorization: str = Header(None)):
    """
        Cancels an order and removes it from the database.

        Parameters:
            - order_id (str): The ID of the order to cancel.
            - symbol (str): The symbol of the order to cancel.
            - db (Session, optional): The database session dependency obtained using `Depends(get_db)`.
            - authorization (str): The authorization header containing the Bearer token.

        Returns:
            dict: A dictionary containing the cancellation details if successful.

        Raises:
            HTTPException: If the authorization header is missing or invalid, the order is not found, or an internal error occurs.
    """
    trade_service = TradeService(db, authorization)
    # Storniere die Order auf der Börse
    response = trade_service.cancel_order(order_id, symbol)

    # Entferne die Order aus der Datenbank
    trade = db.query(Trade).filter(Trade.trade_id == order_id).first()
    if not trade:
        raise HTTPException(status_code=404, detail="Order not found")

    db.delete(trade)
    db.commit()

    return {"message": "Order canceled and removed from database successfully", "order": response}


@app.post("/request-password-reset/")
def forgot_password(email: str, db: Session = Depends(get_db)):
    """
        Handles the request to reset a password.

        This endpoint sends a password reset email to the provided email address.
        It retrieves the user associated with the given email, generates a reset token,
        and sends an email with the token to the user's email address.

        Parameters:
            - email (str): The email address of the user requesting the password reset.
            - db (Session, optional): The database session dependency obtained using `Depends(get_db)`.

        Returns:
            dict: A dictionary containing a success message if the email was sent successfully.
        """
    user = db.query(Account).filter(Account.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    reset_token = generate_reset_token(user.login_name)
    send_password_reset_email(user.email, reset_token)
    return {"message": "Passwort-Reset was send to your email address."}


@app.post("/reset-password/")
def reset_password(reset_request: PasswordResetRequest, db: Session = Depends(get_db)):
    """
        Handles resetting a user's password.

        This endpoint allows users to reset their password using a valid reset token.
        It verifies the provided token, updates the user's password with the new one,
        and commits the changes to the database.

        Parameters:
            - reset_request (PasswordResetRequest): The request containing the reset token and new password.
            - db (Session, optional): The database session dependency obtained using `Depends(get_db)`.

        Returns:
            dict: A dictionary containing a success message if the password was reset successfully.
        """
    user = verify_reset_token(reset_request.token)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid token.")
    hashed_password = get_hashed_password(reset_request.new_password)
    user.hashed_password = hashed_password
    db.commit()

    return {"message": "Password reset successfully."}


@app.get('/payment/execute')
def execute_payment(request: Request, db: Session = Depends(get_db), authorization: str = Header(None)):
    """
        Executes a PayPal payment and updates the subscription status in the database.

        Args:
            request (Request): The FastAPI request object.
            db (Session): The database session dependency.
            authorization (str, optional): The authorization token passed in the header.

        Raises:
            HTTPException: If the authorization header is missing or invalid,
                           or if the payment execution fails.

        Returns:
            JSONResponse: A JSON response indicating the result of the payment execution.
                          Example:
                          {
                              "message": "Payment executed successfully"
                          }
        """
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header missing or invalid.")

    token = authorization.split(" ")[1]
    payload = verify_trade_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token", headers={"WWW-Authenticate": "Bearer"})

    paypal = Paypal()
    payment_id = request.query_params.get('paymentId')
    payer_id = request.query_params.get('PayerID')
    if not payment_id or not payer_id:
        raise HTTPException(status_code=400, detail="Missing paymentId or PayerID")

    result = paypal.execute_payment(payment_id, payer_id)
    if result == "Payment executed successfully":
        try:
            db.query(Subscription).filter(Subscription.payment_id == payment_id).update({"abo_status": "active"})
            db.commit()
            return JSONResponse(content={"message": "Payment executed successfully"})
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(status_code=400, detail="Payment execution failed")


@app.post('/payment')
def create_payment(subscription: Subscription_Info, db: Session = Depends(get_db), authorization: str = Header(None)):
    logging.debug(f"Received subscription data: {subscription}")

    """
    Creates a PayPal payment for a subscription and stores the subscription details in the database.

    Args:
        subscription (Subscription_Info): The subscription information including currency, amount, product name, product days, and subscription status.
        db (Session): Database session used for transaction.
        authorization (str): Authorization header containing the Bearer token for authentication.

    Raises:
        HTTPException: If the authorization header is missing, invalid, or token verification fails (401).
        HTTPException: If payment creation fails (400).
        HTTPException: If there's an internal server error during database operations (500).

    Returns:
        JSONResponse: Contains a success message and approval URL if payment is created successfully, or an error message otherwise.
    """

    logging.info("Begin create Payment")

    paypal = Paypal()
    if authorization is None or not authorization.startswith("Bearer "):
        logging.error("Missing or invalid Authorization-Header")
        raise HTTPException(status_code=401, detail="Authorization header missing or invalid.")

    token = authorization.split(" ")[1]
    payload = verify_trade_token(token)
    if payload is None:
        logging.error("Invalid or missing Token")
        raise HTTPException(status_code=401, detail="Invalid or expired token", headers={"WWW-Authenticate": "Bearer"})

    account_id = payload.get("account_id")
    logging.info(f"account_id: {account_id}")

    subscription_amount = 0
    if subscription.product_name == "Basic" and subscription.product_days == 365:
        subscription_amount = 99
    if subscription.product_name == "Basic" and subscription.product_days == 30:
        subscription_amount = 8
    if subscription.product_name == "Silver" and subscription.product_days == 365:
        subscription_amount = 199
    if subscription.product_name == "Silver" and subscription.product_days == 30:
        subscription_amount = 15
    if subscription.product_name == "Gold" and subscription.product_days == 365:
        subscription_amount = 299
    if subscription.product_name == "Gold" and subscription.product_days == 30:
        subscription_amount = 20

    logging.info(
        f"Abo create: {subscription_amount} for {subscription.product_name} ({subscription.product_days} Days)")

    result = paypal.create_payment(subscription.currency, subscription_amount, subscription.product_name)
    if "approval_url" in result:
        try:
            new_subscription = Subscription(
                amount=subscription_amount,
                date_start=date.today(),
                date_end=date.today() + timedelta(days=subscription.product_days),
                product_name=subscription.product_name,
                abo_status="Active",
                currency=subscription.currency,
                account_id=account_id,
                payment_id=result['payment_id']
            )
            db.add(new_subscription)
            db.commit()
            db.refresh(new_subscription)
            logging.info("Abo saved in DB")
            return JSONResponse(
                content={"message": "Payment creation successfully", "approval_url": result["approval_url"]}
            )
        except Exception as e:
            db.rollback()
            logging.error(f"Database error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    else:
        logging.error("create payment failed")
        raise HTTPException(status_code=400, detail="Payment creation failed")
