from typing import List
from fastapi import Depends, FastAPI, status, HTTPException
from .database import engine, sessionLocal
from . import models
from .schemas import ArticleSchema, MyArticleSchema
from sqlalchemy.orm import Session
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/articles/', response_model = List[MyArticleSchema])
def get_article(db:Session = Depends(get_db)):
    all_articles = db.query(models.Article).all()
    return all_articles 

@app.get('/articles/{id}', status_code=status.HTTP_200_OK, response_model = MyArticleSchema)
def article_details(id:int, db:Session = Depends(get_db)):
    # article_details = db.query(models.Article).filter(models.Article.id == id).first()
    article_details = db.query(models.Article).get(id)
    if article_details:
        return article_details
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The article with id {id} does not exist')
    

@app.post('/articles/', status_code=status.HTTP_201_CREATED )
def add_article(article:ArticleSchema, db:Session = Depends(get_db)):
    new_article = models.Article(title=article.title, description=article.description)
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article

@app.put('/articles/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_article(id:int, article:ArticleSchema, db:Session = Depends(get_db)):
    db.query(models.Article).filter(models.Article.id == id).update({'title':article.title, 'description':article.description})
    return {'message': "The article has been updated"}

@app.delete('/articles/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_article(id:int, db:Session = Depends(get_db)):
    db.query(models.Article).filter(models.Article.id == id).delete(synchronize_session=False)
    db.commit()
    