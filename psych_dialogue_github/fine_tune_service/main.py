from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os, json, tempfile
from openai import OpenAI

app = FastAPI(title="Fine-Tune Service")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Example(BaseModel):
    prompt: str
    completion: str

@app.post("/finetune")
async def create_finetune_job(examples: dict):
    """
    Expects JSON: {'examples':[{'prompt':..,'completion':..}, ...]}
    Writes a .jsonl, uploads it, and creates a fine-tune job using gpt-5 as base.
    """
    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY not configured")

    exs = examples.get("examples")
    if not exs or not isinstance(exs, list):
        raise HTTPException(status_code=400, detail="Invalid dataset format")

    tmp = tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".jsonl")
    try:
        for e in exs:
            tmp.write(json.dumps({"prompt": e["prompt"], "completion": e["completion"]}) + "\n")
        tmp.flush()
        tmp.close()

        # Upload file for fine-tuning
        with open(tmp.name, "rb") as fh:
            upload_resp = client.files.create(file=fh, purpose="fine-tune")
        file_id = upload_resp.id if hasattr(upload_resp, "id") else upload_resp["id"]

        # Create fine-tune job
        ft_resp = client.fine_tuning.jobs.create(training_file=file_id, model="gpt-5")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI error: {e}")

    return {"upload": str(upload_resp), "fine_tune": str(ft_resp)}
