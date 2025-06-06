from pydantic import BaseModel
from typing import Optional

class ArticleCreate(BaseModel):
    url: str

class ArticleOut(BaseModel):
    id: int
    url: str
    status: str
    title: Optional[str] = None
    summary: Optional[str] = None
    outline: Optional[str] = None
    draft: Optional[str] = None

    class Config:
        orm_mode = True
