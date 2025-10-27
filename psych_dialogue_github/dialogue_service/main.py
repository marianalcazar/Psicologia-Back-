from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from openai import OpenAI

app = FastAPI(title="Dialogue Service")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class DialogueRequest(BaseModel):
    session_id: str
    user_input: str

@app.post("/dialogue")
async def get_patient_reply(req: DialogueRequest):
    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY not configured")

    system_prompt = (
        "Eres un paciente en una cita psicológica. Responde con honestidad, "
        "emociones controladas y sin dar consejos clínicos. Mantén respuestas entre 1 y 4 oraciones."
    )

    # Use the Responses API (recommended for gpt-5)
    try:
        resp = client.responses.create(
            model="gpt-5",
            input=[
                {"role":"system","content": system_prompt},
                {"role":"user","content": req.user_input}
            ],
            max_tokens=300,
            temperature=0.7,
        )
        # Extract text (compatibility note: response shapes may vary; check docs)
        text = ""
        if hasattr(resp, "output_text"):
            text = resp.output_text
        else:
            # fallback: try to extract from resp.output[0].content
            outputs = getattr(resp, "output", None)
            if outputs and len(outputs) and isinstance(outputs[0], dict):
                parts = outputs[0].get("content") or outputs[0].get("text")
                if isinstance(parts, list):
                    text = "\n".join(p.get("text","") for p in parts if isinstance(p, dict))
                elif isinstance(parts, str):
                    text = parts
        text = text.strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI error: {e}")

    return {"session_id": req.session_id, "reply": text}
