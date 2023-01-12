from pydantic import BaseModel



class ArticleSchema(BaseModel):
    id:int
    title:str
    description:str
    text:str
    