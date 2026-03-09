from fastapi import FastAPI

app = FastAPI(title='Biostream IA backend ')

@app.get('/')
async def root():
    return {'message': 'backend running'}
