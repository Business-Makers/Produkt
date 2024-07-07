from typing import List
from database import get_db
from sqlalchemy.orm import Session
from fastapi import WebSocket, Depends, WebSocketDisconnect
import json
import ccxt
from utils import get_api_credentials
import logging

logging.basicConfig(filename='debugAll.log', level=logging.WARNING, format='%(asctime)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)


class ConnectionManager:
    """
        Manages WebSocket connections.

        Attributes:
            active_connections (List[WebSocket]): List to store active WebSocket connections.
        """

    def __init__(self):
        """
                Initializes a ConnectionManager object.
                """
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """
               Accepts a WebSocket connection and adds it to the active connections list.

               Args:
                   websocket (WebSocket): WebSocket connection object to accept.
               """
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        """
                Disconnects a WebSocket connection and removes it from the active connections list.

                Args:
                    websocket (WebSocket): WebSocket connection object to disconnect.
                """
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        """
                Sends a personal message to a specific WebSocket connection.

                Args:
                    message (str): Message to send.
                    websocket (WebSocket): WebSocket connection object to send the message to.
                """
        await websocket.send_text(message)


manager = ConnectionManager()


async def fetch_infos(exchange_name: str, symbol: str, account_id: int, db: Session):
    """
        Fetches ticker information from a cryptocurrency exchange.

        Args:
            exchange_name (str): Name of the cryptocurrency exchange (e.g., 'binance', 'kraken').
            symbol (str): Symbol of the cryptocurrency pair (e.g., 'BTC/USDT').
            account_id (int): ID of the user account for which API credentials are retrieved.
            db (Session): SQLAlchemy database session.

        Returns:
            dict: Dictionary containing ticker information retrieved from the exchange.

        Raises:
            Exception: If there's an error fetching ticker information from the exchange.
        """
    creds = get_api_credentials(account_id, exchange_name, db)
    exchange_class = getattr(ccxt, exchange_name)
    exchange = exchange_class({
        'apiKey': creds['api_Key'],
        'secret': creds['secret'],
        'passphrase': creds['passphrase']
    })

    ticker = exchange.fetch_ticker(symbol)
    return ticker


async def websocket_endpoint(websocket: WebSocket, user_id: int, db: Session = Depends(get_db)):
    """
        WebSocket endpoint for handling real-time data requests.

        Args:
            websocket (WebSocket): WebSocket connection object.
            user_id (int): ID of the user making the WebSocket connection.
            db (Session, optional): SQLAlchemy database session. Defaults to Depends(get_db).
        """

    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            info_request = json.loads(data)
            exchange_name = info_request['exchange_name']
            symbol = info_request['symbol']

            try:
                ticker = await fetch_infos(exchange_name, symbol, user_id, db)
                response = {
                    "status": "ok",
                    "ticker": ticker
                }
            except Exception as e:
                response = {"status": "error",
                            "message": str(e)}

            await manager.send_personal_message(json.dumps(response), websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        await manager.send_personal_message(json.dumps({"status": "error", "message": str(e)}), websocket)
