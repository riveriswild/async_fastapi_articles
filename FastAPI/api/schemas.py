from pydantic import BaseModel



class ArticleSchema(BaseModel):
    # id:int
    title:str
    description:str


class IdArticleSchema(ArticleSchema):
    id:int

class MyArticleSchema(ArticleSchema):
    title: str
    description: str
    
    class Config:
        orm_mode = True