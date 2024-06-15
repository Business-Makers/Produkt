import time
from sqlalchemy.orm import Session

from trade_service import TradeService


class background_threads:
    def __init__(self, db: Session, authorization: str):
        self.db = db
        self.authorization = authorization
        self.trade_service = TradeService(db, authorization)

    def background_check_limit_orders(self):
        while True:
            self.trade_service.check_and_update_limit_orders()
            time.sleep(1)
