"""
Main Application Entry Point

This script serves as the entry point for running the FastAPI application.
It imports the FastAPI instance 'app' from the 'routes' module and uses the Uvicorn server to run the application.

Usage:
    Run this script to start the FastAPI application.
"""

import uvicorn
from routes import app

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
