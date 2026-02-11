from models import ParsedLog, LogLevel
from typing import List

def parse_log(txt: str) -> ParsedLog:
    txt = txt.strip()
    if not txt:
        return ParsedLog(level=LogLevel.INFO, message="")
    
    parts = txt.split(" ", 1)
    raw_level = parts[0].upper()
    message = parts[1] if len(parts) > 1 else ""
    level = LogLevel(raw_level) if raw_level in LogLevel.__members__ else LogLevel.INFO
    return ParsedLog(level=level, message=message)

def parse_logs(text: str) -> List[ParsedLog]:
    lines = text.splitlines()
    results = []

    for line in lines:
        line = line.strip()
        if not line:
            continue
        results.append(parse_log(line))

    return results
