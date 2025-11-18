"""
Health Repository
系統健康檢查資料存取
"""
from sqlalchemy.orm import Session
from sqlalchemy import text


class HealthRepository:
    """健康檢查資料存取層"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def check_database_connection(self) -> bool:
        """
        檢查資料庫連接
        
        Returns:
            bool: True if connected, False otherwise
        """
        try:
            self.db.execute(text("SELECT 1"))
            return True
        except Exception:
            return False
