import os
from fastapi import FastAPI, HTTPException
from vllm import AsyncLLMEngine, AsyncEngineArgs
from vllm.server.openai_serving_chat import OpenAIServingChat
from vllm.server.openai_serving_completion import OpenAIServingCompletion

app = FastAPI()
MODEL = os.getenv("MODEL_NAME")
LOAD_4BIT = os.getenv("LOAD_IN_4BIT") == "true"
QCONF = os.getenv("QUANTIZATION_CONFIG")

engine = AsyncLLMEngine.from_engine_args(
    AsyncEngineArgs(
        model=MODEL,
        load_in_4bit=LOAD_4BIT,
        quantization_config=QCONF,
        max_model_len=int(os.getenv("MAX_MODEL_LEN", "32768")),
        max_num_seqs=int(os.getenv("MAX_BATCH_SIZE", "8")),
    )
)

@app.get("/health")
async def health():
    return {"status": "healthy", "model": MODEL}

@app.get("/v1/models")
async def list_models():
    return {"object":"list","data":[{"id":MODEL}]}

@app.post("/v1/chat/completions")
async def chat(req: dict):
    serv = OpenAIServingChat(engine, served_model_names=[MODEL], response_role="assistant")
    return await serv.create_chat_completion(req, request_id="1")

@app.post("/v1/completions")
async def comp(req: dict):
    serv = OpenAIServingCompletion(engine, served_model_names=[MODEL])
    return await serv.create_completion(req, request_id="1")
