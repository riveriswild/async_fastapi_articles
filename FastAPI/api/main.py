from fastapi import FastAPI 
from pydantic import BaseModel

class Article(BaseModel):
    id: int
    title: str
    description: str

app = FastAPI()

@app.get('/')
async def Index():
    return 'hello'

@app.get('/articles/{id}')
def get_artile(id:int):
    return{'article':{id}}

@app.post('/artcle/')
def add_article(article: Article):
    return article 