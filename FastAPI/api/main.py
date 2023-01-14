from fastapi import FastAPI, HTTPException, status

from .schemas import ArticleSchema, IdArticleSchema
from .db import metadata, database, engine, Article
from typing import List


metadata.create_all(engine)
app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()
    
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    
@app.post('/articles/', status_code=status.HTTP_201_CREATED, response_model=IdArticleSchema)
async def insert_article(article:ArticleSchema):
    query = Article.insert().values(title=article.title, description=article.description)
    last_record_id = await database.execute(query)
    return {**article.dict(), "id": last_record_id}

@app.get('/articles/', response_model=List[IdArticleSchema])
async def get_articles():
    query = Article.select()
    return await database.fetch_all(query=query)

@app.get('/articles/{id}', response_model=ArticleSchema)
async def get_details(id:int):
    query = Article.select().where(id==Article.c.id)
    article_det = await database.fetch_one(query=query)
    
    if not article_det:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    return {**article_det}

@app.put('/articles/{id}', response_model=IdArticleSchema)
async def update_article(id:int, article:ArticleSchema):
    query = Article.update().where(id==Article.c.id).values(title=article.title, description=article.description)
    await database.execute(query)
    return {**article.dict(), "id": id}