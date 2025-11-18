"""
Dependencies
FastAPI 依賴注入
"""
from typing import Generator
from app.db.session import SessionLocal


def get_db() -> Generator:
    """
    獲取資料庫 Session
    使用 FastAPI 依賴注入
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
