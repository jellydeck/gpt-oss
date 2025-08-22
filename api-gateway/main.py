import os, json, hashlib
from fastapi import FastAPI, HTTPException, Depends, Request, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import httpx
import redis
from cache import CacheManager
from middleware import setup_middleware

app = FastAPI()
setup_middleware(app)

VLLM_URL = os.getenv("VLLM_URL")
REDIS_URL = os.getenv("REDIS_URL")
API_KEY = os.getenv("API_KEY", "")
security = HTTPBearer(auto_error=False) if API_KEY else None
cache = CacheManager(REDIS_URL, ttl=int(os.getenv("CACHE_TTL", "3600")))

@app.on_event("startup")
async def start():
    await cache.connect()

def verify_key(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if API_KEY and (not credentials or credentials.credentials != API_KEY):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return True

def cache_key(data: dict):
    s = json.dumps(data, sort_keys=True)
    return hashlib.md5(s.encode()).hexdigest()

async def forward(path, payload):
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{VLLM_URL}{path}", json=payload)
        resp.raise_for_status()
        return resp.json()

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/v1/chat/completions")
async def chat(req: Request, auth=Depends(verify_key)):
    payload = await req.json()
    key = cache_key(payload)
    cached = await cache.get(key)
    if cached: return cached
    result = await forward("/chat/completions", payload)
    await cache.set(key, result)
    return result

@app.post("/v1/completions")
async def comp(req: Request, auth=Depends(verify_key)):
    payload = await req.json()
    key = cache_key(payload)
    cached = await cache.get(key)
    if cached: return cached
    result = await forward("/completions", payload)
    await cache.set(key, result)
    return result
