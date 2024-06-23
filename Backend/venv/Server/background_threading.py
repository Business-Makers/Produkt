import threading
import time
from database import SessionLocal
from trade_service import TradeService
from fastapi import HTTPException


class background_threads:
    def __init__(self):
        self.authorization = None
        self.running = False

    def set_authorization(self, authorization: str):
        self.authorization = authorization

    def start_background_tasks(self):
        self.running = True
        threading.Thread(target=self.run_background_task).start()

    def run_background_task(self):
        if not self.authorization:
            raise HTTPException(status_code=403, detail='Authorization Token is not set.')
        db = SessionLocal()
        trade_service = TradeService(db, self.authorization)
        try:
            while self.running:
                trade_service.check_and_update_limit_orders()
                time.sleep(5)
                print("Hallo")
        finally:
            db.close()

    def stop_background_tasks(self):
        self.running = False
