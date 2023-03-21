from fastapi import FastAPI
from app.api.routes.gpt import router as gpt_router

app = FastAPI()

app.include_router(gpt_router, prefix='/api')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('app.main:app', host='0.0.0.0', port=8000, log_level='info', reload=True)
