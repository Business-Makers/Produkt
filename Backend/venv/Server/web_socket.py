from typing import List
from database import get_db
from sqlalchemy.orm import Session
from fastapi import WebSocket, Depends, WebSocketDisconnect
import json
import ccxt
from utils import get_api_credentials
import logging

logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)
logging.getLogger('sqlalchemy.pool').setLevel(logging.ERROR)
logging.getLogger('sqlalchemy.dialects').setLevel(logging.ERROR)
logging.getLogger('sqlalchemy.orm').setLevel(logging.ERROR)

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)


manager = ConnectionManager()


async def fetch_infos(exchange_name: str, symbol: str, account_id: int, db: Session):
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
