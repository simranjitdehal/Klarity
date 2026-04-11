# # from typing import List
# # from models import ParsedLog, LogLevel
# # from openai import OpenAI
# # import os
# # from dotenv import load_dotenv

# # load_dotenv()

# # client = OpenAI(api_key=os.environ.get('DEEPSEEK_API_KEY'), base_url="https://api.deepseek.com")


# # def generate_analysis(logs: List[ParsedLog]) -> dict:
# #     # deterministic logic
# #     error_count = sum(1 for log in logs if log.level == LogLevel.ERROR)

# #     # prepare text for AI
# #     formatted_logs = "\n".join(
# #         f"{log.level}: {log.message}" for log in logs
# #     )

# #     # call DeepSeek
# #     response = client.chat.completions.create(
# #         model="deepseek-chat",
# #         messages=[
# #             {
# #                 "role": "system",
# #                 "content": "You are a senior engineer analyzing application logs."
# #             },
# #             {
# #                 "role": "user",
# #                 "content": f"Analyze these logs and explain issues briefly:\n\n{formatted_logs}"
# #             }
# #         ]
# #     )

# #     #extract AI text
# #     ai_summary = response.choices[0].message.content

# #     #return final result
# #     return {
# #         "summary": ai_summary,
# #         "errors_found": error_count,
# #         "status": "AI_CONNECTED"
# #     }

# from schemas import IngestPayload
# from openai import OpenAI
# import os
# from dotenv import load_dotenv

# load_dotenv()

# client = OpenAI(
#     api_key=os.environ.get("DEEPSEEK_API_KEY"),
#     base_url="https://api.deepseek.com"
# )


# def generate_analysis(payload: IngestPayload) -> dict:

#     prompt = f"""
# You are a senior Python debugging assistant.

# Return output STRICTLY in this JSON format:

# {{
#   "root_cause": "...",
#   "why": "...",
#   "fix_summary": "...",
#   "corrected_code": "..."
# }}

# Keep explanations concise.
# Do NOT include markdown.
# Do NOT include extra commentary.
# Do NOT include shell commands.
# Do NOT include headers.
# Only valid JSON.

# ERROR DETAILS:

# Exception Type: {payload.exception_type}
# Exception Message: {payload.exception_message}

# Last Frame:
# File: {payload.last_frame.file}
# Line: {payload.last_frame.line}
# Function: {payload.last_frame.function}
# Code: {payload.last_frame.code}

# Context:
# {payload.context_snippet}
# """

#     response = client.chat.completions.create(
#         model="deepseek-chat",
#         messages=[
#             {
#                 "role": "system",
#                 "content": "You are precise, technical, and solution-oriented."
#             },
#             {
#                 "role": "user",
#                 "content": prompt
#             }
#         ]
#     )

#     ai_summary = response.choices[0].message.content

#     return {
#         "summary": ai_summary,
#         "status": "AI_CONNECTED"
#     }

from openai import OpenAI
import os
import json
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)


def generate_analysis(logs) -> dict:
    """
    Takes a processed log object and returns structured AI analysis
    """

    prompt = f"""
You are a senior backend engineer.

Analyze the error and return STRICT JSON:

{{
  "ai_summary": "...",
  "probable_cause": "...",
  "fix_summary": "...",
  "detailed_steps": "...",
  "severity": "low | medium | high"
}}

Rules:
- Be precise and practical
- Focus on root cause not the symptoms
- Fix steps MUST be numbered (1, 2, 3...)
- Keep answers concise
- No markdown
- No extra text
- Only valid JSON

ERROR DETAILS:

Type: {logs.exception_type}
Message: {logs.exception_message}
File: {logs.file}
Line: {logs.line}
Function: {logs.function}
"""

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are precise, technical, and solution-oriented."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            response_format={"type": "json_object"}
        )
    
        content = response.choices[0].message.content.strip()

        parsed = json.loads(content)

        return {
            "ai_summary": parsed.get("ai_summary"),
            "probable_cause": parsed.get("probable_cause"),
            "fix_summary": parsed.get("fix_summary"),
            "detailed_steps": parsed.get("detailed_steps"),
            "severity": parsed.get("severity")
        }

    except Exception as e:
        print("AI ERROR:", e)

        # 🔥 fallback (never break worker)
        return {
            "ai_summary": "AI analysis failed",
            "probable_cause": None,
            "fix_summary": None,
            "detailed_steps": None,
            "severity": "low"
        }