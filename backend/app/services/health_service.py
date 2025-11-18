"""
Health Service
系統健康檢查業務邏輯
"""
from datetime import datetime

from app.repositories.health_repository import HealthRepository


class HealthService:
    """健康檢查業務邏輯層"""
    
    def __init__(self, health_repo: HealthRepository):
        self.health_repo = health_repo
    
    def check_health(self) -> dict:
        """
        執行系統健康檢查
        檢查資料庫連接狀態
        """
        is_db_connected = self.health_repo.check_database_connection()
        
        if is_db_connected:
            db_status = "healthy"
            overall_status = "healthy"
        else:
            db_status = "unhealthy"
            overall_status = "unhealthy"
        
        return {
            "status": overall_status,
            "timestamp": datetime.utcnow().isoformat(),
            "database": db_status,
            "service": "CineMood API"
        }
