from fastapi import FastAPI, Request, Response
import time

def setup_middleware(app: FastAPI):
    @app.middleware("http")
    async def add_process_time(request: Request, call_next):
        start = time.time()
        resp = await call_next(request)
        resp.headers["X-Process-Time"] = str(time.time() - start)
        return resp
