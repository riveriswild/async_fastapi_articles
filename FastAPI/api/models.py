from .database import Base
from sqlalchemy import Column, Integer, String

class Article(Base):
    __table_name__ = 'articles'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    description = Column(String(400))
    
    