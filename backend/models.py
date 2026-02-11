from pydantic import BaseModel
from enum import Enum as enum
from typing import List

class LogLevel(str,enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    DEBUG = "DEBUG"
    UNKNOWN = "UNKNOWN"

class LogInput(BaseModel):
    logs: str

class ParsedLog(BaseModel):
    level: LogLevel
    message: str

class AnalyzeResponse(BaseModel):
    parsed: List[ParsedLog]
    analysis: dict
