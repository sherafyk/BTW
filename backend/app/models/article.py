from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from ..database import Base

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, nullable=False)
    status = Column(String, default="submitted", nullable=False)
    title = Column(String)
    author = Column(String)
    publish_date = Column(String)
    content = Column(Text)
    summary = Column(Text)
    outline = Column(Text)
    draft = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
