import httpx
from fastapi import APIRouter, Depends

router = APIRouter()

# healthcheck api
@router.get('/healthcheck')
def healthcheck():
    return {'status': 'ok'}