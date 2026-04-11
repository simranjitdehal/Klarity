from db import SessionLocal, get_db
from fastapi import FastAPI, Request, HTTPException, APIRouter, Depends
from schemas import PayloadIngest
from auth import get_user_from_api_key
from db import SessionLocal
from models import incoming_log
from sqlalchemy.orm import Session

#ingest api
router = APIRouter()
@router.post("/ingest")
def ingest(payload: PayloadIngest, request: Request):
    db = SessionLocal()
    try:
        api_key = request.headers.get("x-api-key")
        if not api_key:
            raise HTTPException(status_code=401, detail="API key missing")
        # Validate API key and get user
        user = get_user_from_api_key(api_key)
        if not user:
            raise HTTPException(status_code=403, detail="Invalid API key")
        # Here we would typically save the payload to the database
        log_data = incoming_log(
            user_id=user,
            raw_log=payload.error.raw_trace,
            environment=payload.metadata.environment,
            timestamp=payload.metadata.timestamp,
            status="pending"
        )
        db.add(log_data)
        db.commit()

        return {"message": "Log ingested successfully"}
    
    finally:
        db.close()
    
#this will return completeed logs to the js frontend
@router.get("/logs/completed")
def get_completed_logs(request: Request, db: Session = Depends(get_db)):
    api_key = request.headers.get("x-api-key")
    print("HEADER KEY:", request.headers.get("x-api-key"))
    if not api_key:
        raise HTTPException(status_code=401, detail="API key missing")

    user = get_user_from_api_key(api_key)
    if not user:
        raise HTTPException(status_code=403, detail="Invalid API key")

    logs = (
        db.query(incoming_log)
        .filter(
            incoming_log.user_id == user,
            incoming_log.status == "Completed"
        )
        .order_by(incoming_log.id.desc())
        .limit(1)
        .first()
    )

    if not logs:
        return {"message": "No logs yet"}

    return {
        "ai_summary": logs.ai_summary,
        "probable_cause": logs.probable_cause,
        "fix_summary": logs.fix_summary,
        "detailed_steps": logs.detailed_steps,
        "severity": logs.severity,
    }
