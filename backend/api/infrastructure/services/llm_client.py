import os
import json
import requests
from typing import List, Dict

LLM_BASE_URL = os.environ.get("LLM_BASE_URL")
LLM_API_KEY = os.environ.get("LLM_API_KEY")
LLM_MODEL = os.environ.get("LLM_MODEL")

HEADERS = {
    "Authorization": f"Bearer {LLM_API_KEY}",
    "Content-Type": "application/json",
}


def call_llm_text_only(system_prompt: str, user_prompt: str) -> Dict:
    body = {
        "model": LLM_MODEL,
        "temperature": 0.1,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }
    r = requests.post(
        f"{LLM_BASE_URL}/v1/chat/completions",
        headers=HEADERS,
        data=json.dumps(body),
        timeout=60,
    )
    r.raise_for_status()
    content = r.json()["choices"][0]["message"]["content"]
    return json.loads(content)


def call_llm_with_images(
    system_prompt: str, user_prompt: str, image_urls: List[str]
) -> Dict:
    content = [{"type": "text", "text": user_prompt}] + [
        {"type": "image_url", "image_url": {"url": url}} for url in image_urls
    ]
    body = {
        "model": LLM_MODEL,
        "temperature": 0.1,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": content},
        ],
    }
    r = requests.post(
        f"{LLM_BASE_URL}/v1/chat/completions",
        headers=HEADERS,
        data=json.dumps(body),
        timeout=60,
    )
    r.raise_for_status()
    content = r.json()["choices"][0]["message"]["content"]
    return json.loads(content)
