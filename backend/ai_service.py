from typing import List
from models import ParsedLog, LogLevel
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.environ.get('DEEPSEEK_API_KEY'), base_url="https://api.deepseek.com")


def generate_analysis(logs: List[ParsedLog]) -> dict:
    # deterministic logic
    error_count = sum(1 for log in logs if log.level == LogLevel.ERROR)

    # prepare text for AI
    formatted_logs = "\n".join(
        f"{log.level}: {log.message}" for log in logs
    )

    # call DeepSeek
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": "You are a senior engineer analyzing application logs."
            },
            {
                "role": "user",
                "content": f"Analyze these logs and explain issues briefly:\n\n{formatted_logs}"
            }
        ]
    )

    #extract AI text
    ai_summary = response.choices[0].message.content

    #return final result
    return {
        "summary": ai_summary,
        "errors_found": error_count,
        "status": "AI_CONNECTED"
    }
