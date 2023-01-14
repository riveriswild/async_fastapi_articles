from fastapi import FastAPI, status

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