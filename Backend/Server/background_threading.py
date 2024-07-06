import threading
import time
from database import SessionLocal
from trade_service import TradeService
from fastapi import HTTPException
import logging

logging.basicConfig(filename='debugAll.log', level=logging.WARNING, format='%(asctime)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)


class background_threads:
    """
    A class to handle background tasks related to trade services.
        Attributes:
            authorization (str): Authorization token for accessing trade services.
            running (bool): A flag to indicate whether the background tasks are running.
    """

    def __init__(self):
        """
        Initializes the background_threads class with default values.
        """
        self.authorization = None
        self.running = False

    def set_authorization(self, authorization: str):
        """
        Sets the authorization token for the trade services.
            Args:
                authorization (str): The authorization token to be set.
        """
        self.authorization = authorization

    def start_background_tasks(self):
        """
        Starts the background task in a separate thread.
        """
        self.running = True
        threading.Thread(target=self.run_background_task).start()

    def run_background_task(self):
        """
        The main method that runs in the background to check and update limit orders.

        Raises:
        HTTPException: If the authorization token is not set.
        """
        if not self.authorization:
            raise HTTPException(status_code=403, detail='Authorization Token is not set.')
        db = SessionLocal()

        trade_service = TradeService(db, self.authorization)

        try:
            while self.running:
                trade_service.check_and_update_limit_orders()
                time.sleep(1000)

        finally:
            db.close()

    def stop_background_tasks(self):
        """
        Stops the background task.
        """
        self.running = False
