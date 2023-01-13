from fastapi import Depends, FastAPI, status
from .database import engine, sessionLocal
from . import models
from .schemas import ArticleSchema
from sqlalchemy.orm import Session
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
        

@app.post('/articles/', status_code=status.HTTP_201_CREATED )
def add_article(article:ArticleSchema, db:Session = Depends(get_db)):
    new_article = models.Article(title=article.title, description=article.description)
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article