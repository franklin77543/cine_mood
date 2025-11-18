"""
Person Repository
負責演職人員相關的資料庫操作
"""
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from app.models.person_model import Person
from app.models.movie_credit_model import MovieCredit


class PersonRepository:
    """演職人員資料存取層"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_person_by_id(self, person_id: str) -> Optional[Person]:
        """根據 ID 獲取演職人員資訊"""
        return (
            self.db.query(Person)
            .options(joinedload(Person.credits))
            .filter(Person.id == person_id)
            .first()
        )
    
    def get_person_by_tmdb_id(self, tmdb_id: int) -> Optional[Person]:
        """根據 TMDB ID 獲取演職人員"""
        return self.db.query(Person).filter(Person.tmdb_id == tmdb_id).first()
    
    def get_popular_actors(self, limit: int = 10) -> List[tuple]:
        """
        獲取熱門演員
        返回 (Person, 電影數量) 的列表
        """
        return (
            self.db.query(Person, func.count(MovieCredit.id).label('movie_count'))
            .join(MovieCredit)
            .filter(MovieCredit.role == 'actor')
            .group_by(Person.id)
            .order_by(func.count(MovieCredit.id).desc())
            .limit(limit)
            .all()
        )
