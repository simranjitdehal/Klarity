from fastapi import FastAPI, Request
# from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates
# from fastapi.staticfiles import StaticFiles
from models import IngestPayload, AnalyzeResponse
from ai_service import generate_analysis
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://klarityai.up.railway.app", "http://127.0.0.1:8000", "http://localhost:3000"],  # restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# BASE_DIR = Path(__file__).resolve().parent
# FRONTEND_STATIC = BASE_DIR.parent / "frontend" / "static"

# app.mount("/static", StaticFiles(directory=FRONTEND_STATIC), name="static")
# templates = Jinja2Templates(directory="frontend/templates")

latest_analysis = None


@app.post("/ingest", response_model=AnalyzeResponse)
def ingest(payload: IngestPayload):
    global latest_analysis
    latest_analysis = generate_analysis(payload)
    return {"analysis": latest_analysis}


# @app.get("/")
# def home(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})


@app.get("/latest")
def get_latest():
    return {"analysis": latest_analysis}
