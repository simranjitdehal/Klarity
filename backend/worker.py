from db import SessionLocal
from models import incoming_log
import time, traceback
from log_processor import extract_exception, extract_file_info
from ai_service import generate_analysis as analyze_error

def worker():
    while True:
        db = SessionLocal()
        try:
            logs = db.query(incoming_log).filter_by(status="pending").first()

            if not logs:
                print("No pending logs. Worker is sleeping...")
                time.sleep(5)
                continue

            print(f"Processing log ID: {logs.id}")
            logs.status = "processing"
            db.commit()

            exception_type, exception_message = extract_exception(logs.raw_log)
            file, line, function = extract_file_info(logs.raw_log)

            logs.exception_type = exception_type
            logs.exception_message = exception_message
            logs.file = file
            logs.line = line
            logs.function = function

            ai_data = analyze_error(logs)

            logs.ai_summary = ai_data.get("ai_summary")
            logs.probable_cause = ai_data.get("probable_cause")
            logs.fix_summary = ai_data.get("fix_summary")
            logs.detailed_steps = ai_data.get("detailed_steps")
            logs.severity = ai_data.get("severity")

            logs.status = "Completed"
            print(f"Completed log ID: {logs.id}")

            db.commit()
        except Exception as e:
            print(f"Error:",e)
            traceback.print_exc()
            
        finally:
            db.close()
if __name__ == "__main__":
    worker()
