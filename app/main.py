from fastapi import FastAPI
from app.api.routes.healthcheck import router as healthcheck_router
from app.api.routes.gpt4 import router as gpt_router
from app.api.routes.chat_to_lily import router as lily_router

app = FastAPI()

app.include_router(healthcheck_router, prefix='/api')
app.include_router(gpt_router, prefix='/api')
app.include_router(lily_router, prefix='/api')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('app.main:app', host='0.0.0.0', port=8000, log_level='info', reload=True)
