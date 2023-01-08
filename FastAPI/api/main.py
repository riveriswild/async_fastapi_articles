from fastapi import FastAPI 

app = FastAPI()

@app.get('/')
async def Index():
    return 'hello'

@app.get('/articles/{id}')
def get_artile(id:int):
    return{'article':{id}}