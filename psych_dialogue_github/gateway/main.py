from fastapi import FastAPI, HTTPException
import httpx
import os
from pydantic import BaseModel

app = FastAPI(title="Gateway")

DIALOGUE_URL = os.getenv("DIALOGUE_URL", "http://localhost:8001")
FINETUNE_URL = os.getenv("FINETUNE_URL", "http://localhost:8002")

class DialogueRequest(BaseModel):
    session_id: str
    user_input: str

@app.post("/api/dialogue")
async def proxy_dialogue(payload: DialogueRequest):
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(f"{DIALOGUE_URL}/dialogue", json=payload.dict())
    if resp.status_code != 200:
        raise HTTPException(status_code=502, detail="Dialogue service error")
    return resp.json()

class FineTuneRequest(BaseModel):
    dataset: dict

@app.post("/api/finetune")
async def create_finetune(payload: FineTuneRequest):
    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(f"{FINETUNE_URL}/finetune", json=payload.dataset)
    if resp.status_code != 200:
        raise HTTPException(status_code=502, detail="Fine-tune service error")
    return resp.json()
