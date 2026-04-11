from fastapi import FastAPI, Request, HTTPException

from schemas import IngestPayload, AnalyzeResponse
from ai_service import generate_analysis
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import json
from auth import get_user_from_api_key
from ingest import router as ingest_router


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://klarityai.up.railway.app", "http://127.0.0.1:8000", "http://localhost:3000", "http://localhost:5500"],  # restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingest_router)


# BASE_DIR = Path(__file__).resolve().parent
# FRONTEND_STATIC = BASE_DIR.parent / "frontend" / "static"

# app.mount("/static", StaticFiles(directory=FRONTEND_STATIC), name="static")
# templates = Jinja2Templates(directory="frontend/templates")

# latest_analysis = None

# STORAGE_FILE = "latest_analysis.json"

# @app.post("/ingest", response_model=AnalyzeResponse)
# def ingest(payload: IngestPayload, request: Request):
#     api_key = request.headers.get("x-api-key")
#     user = get_user_from_api_key(api_key)
#     if not api_key:
#         raise HTTPException(status_code=401, detail="API key missing")
#     if not user:
#         raise HTTPException(status_code=403, detail="Invalid API key")

#     latest_analysis = generate_analysis(payload)

#     with open("latest_analysis.json", "w") as f:
#         json.dump(latest_analysis, f)

#     return {"analysis": latest_analysis}


# @app.get("/")
# def home(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})

# @app.get("/latest")
# def latest():
#     try:
#         with open(STORAGE_FILE, "r") as f:
#             latest_analysis = json.load(f)

#         return {"analysis": latest_analysis}

#     except FileNotFoundError:
#         return {"analysis": None}

#     except Exception as e:
#         return {"analysis": None, "error": str(e)}

