# Psych Dialogue Backend (Microservices) — GitHub-ready

**Modelo por defecto:** `gpt-5`

This project contains three FastAPI microservices:
- `gateway` — API gateway for frontend.
- `dialogue_service` — sends prompts to OpenAI Responses API (gpt-5) to simulate a patient.
- `fine_tune_service` — uploads datasets and creates fine-tune jobs.

## Quick start (clone + push to GitHub)

1. Create a new **empty** repository on GitHub (no README/license).
2. Clone it locally:
   ```bash
   git clone git@github.com:YOUR_USERNAME/psych-dialogue-backend.git
   cd psych-dialogue-backend
   ```
3. Copy the project files into the cloned repo folder (or move this project there).
4. Configure `.env`:
   ```bash
   cp .env.example .env
   # Edit .env and set OPENAI_API_KEY
   ```
5. Commit & push:
   ```bash
   git add .
   git commit -m "Initial project — microservices FastAPI with gpt-5"
   git branch -M main
   git remote add origin git@github.com:YOUR_USERNAME/psych-dialogue-backend.git
   git push -u origin main
   ```

## Run locally (dev)
Install dependencies and run the services individually:

```bash
pip install -r requirements.txt
uvicorn gateway.main:app --reload --port 8000
uvicorn dialogue_service.main:app --reload --port 8001
uvicorn fine_tune_service.main:app --reload --port 8002
```

Or run with Docker Compose:
```bash
docker-compose up --build
```

## Notes & Safety
- Do **not** send real PHI or sensitive patient data to third-party APIs.
- Fine-tuning may incur costs and requires OpenAI account access.

## References
- OpenAI quickstart & Responses API examples. See official docs for client usage and fine-tuning details. 
