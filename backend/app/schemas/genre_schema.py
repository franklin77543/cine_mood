"""
Genre Schemas
電影類型的 Pydantic 模型
"""
from pydantic import BaseModel, ConfigDict


class GenreBase(BaseModel):
    """Genre 基礎模型"""
    id: int
    tmdb_id: int
    name: str
    
    model_config = ConfigDict(from_attributes=True)


class GenreSchema(GenreBase):
    """Genre 完整模型"""
    pass
