"""
CloudJobHunt - Main entry point
Import the app from app.main to avoid duplication
"""
from app.main import app

# This module serves as the entry point for uvicorn: uvicorn main:app
__all__ = ['app']

