"""
Entry point for `uvicorn main:app` from the repository root.

The application implementation lives in `backend.main`.
"""

from backend.main import app

__all__ = ["app"]
