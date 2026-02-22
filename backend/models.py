# from pydantic import BaseModel
# from enum import Enum as enum
# from typing import List

# class IngestPayload(BaseModel):
#     project_id: str
#     error_type: str
#     error_message: str
#     traceback: str


# class LogLevel(str,enum):
#     INFO = "INFO"
#     WARNING = "WARNING"
#     ERROR = "ERROR"
#     DEBUG = "DEBUG"
#     UNKNOWN = "UNKNOWN"

# class LogInput(BaseModel):
#     logs: str

# class ParsedLog(BaseModel):
#     level: LogLevel
#     message: str

# class AnalyzeResponse(BaseModel):
#     parsed: List[ParsedLog]
#     analysis: dict

from pydantic import BaseModel
from typing import Dict, Optional


class LastFrame(BaseModel):
    file: Optional[str] = None
    line: Optional[int] = None
    function: Optional[str] = None
    code: Optional[str] = None


class IngestPayload(BaseModel):
    project_id: str
    exception_type: str
    exception_message: str
    last_frame: LastFrame
    context_snippet: str
    original_line_count: int
    refined_line_count: int


class AnalyzeResponse(BaseModel):
    analysis: dict
