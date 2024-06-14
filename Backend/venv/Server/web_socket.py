from typing import List
from database import get_db
from sqlalchemy.orm import Session
from fastapi import WebSocket, Depends, WebSocketDisconnect
import json
import ccxt
from utils import get_api_credentials


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

async def execute_trade(exchange_name: str, symbol: str, amount: float, price: float, user_id: int, db: Session):
    creds = get_api_credentials(user_id, exchange_name, db)
    exchange_class = getattr(ccxt, exchange_name)
    exchange = exchange_class({
        'apiKey': creds['api_key'],
        'secret': creds['secret'],
        'password': creds.get('password')
    })
    order = exchange.create_limit_buy_order(symbol, amount, price)
    return order

async def websocket_endpoint(websocket: WebSocket, user_id: int, db: Session = Depends(get_db)):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Erwarte eine Nachricht im JSON-Format mit Trade-Informationen
            trade_data = json.loads(data)
            exchange_name = trade_data['exchange']
            symbol = trade_data['symbol']
            amount = trade_data['amount']
            price = trade_data['price']

           
            try:
                order = await execute_trade(exchange_name, symbol, amount, price, user_id, db)
                response = {
                    "status": "success",
                    "order": order
                }
            except Exception as e:
                response = {
                    "status": "error",
                    "message": str(e)
                }
            await manager.send_personal_message(json.dumps(response), websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        await manager.send_personal_message(json.dumps({"status": "error", "message": str(e)}), websocket)
