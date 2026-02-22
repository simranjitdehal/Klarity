from fastapi import FastAPI
from models import AnalyzeResponse, IngestPayload
# from parser import parse_log, parse_logs
from typing import List
from ai_service import generate_analysis


app = FastAPI()

@app.post("/ingest")
def ingest(payload: IngestPayload):
    # parsed = parse_traceback(payload.traceback)
    ai_result = generate_analysis(payload)

    return {
        # "parsed": parsed,
        "analysis": ai_result
    }


# @app.post("/analyze",response_model=AnalyzeResponse)
# def analyze_logs(payload: LogInput):
#     parsed = parse_logs(payload.logs)
#     ai_result = generate_analysis(parsed)
#     return {
#         "parsed": parsed,
#         "analysis": ai_result
#     }


@app.get("/")
def health_check():
    return {"status": "AI agent is live"}