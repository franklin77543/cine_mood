"""
Person Schemas
演職人員的 Pydantic 模型
"""
from pydantic import BaseModel, ConfigDict
from typing import Optional


class PersonBase(BaseModel):
    """Person 基礎模型"""
    id: str
    tmdb_id: int
    name: str
    profile_path: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)


class PersonSchema(PersonBase):
    """Person 完整模型"""
    pass


class CreditSchema(BaseModel):
    """演職人員參與電影的資訊"""
    person: PersonSchema
    role: str  # 'actor' 或 'director'
    character: Optional[str] = None
    order_num: Optional[int] = None
    
    model_config = ConfigDict(from_attributes=True)
