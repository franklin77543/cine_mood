"""
Health Check API
系統健康檢查
"""
from fastapi import APIRouter, Depends

from app.dependencies import get_health_service
from app.services.health_service import HealthService


router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
def health_check(service: HealthService = Depends(get_health_service)):
    """
    健康檢查端點
    
    檢查 API 和資料庫連接狀態
    """
    return service.check_health()
