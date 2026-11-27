"""Nối model — chỗ DUY NHẤT trong bản chạy thử gọi model AI.
Hỗ trợ sẵn chế độ fake (CP2), Google Gemini, OpenAI và Anthropic (CP3).
"""
import json
import os
import time
import urllib.error
import urllib.request

from tracing import model_call

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOW_RAW = False


def load_env(path=os.path.join(ROOT, ".env")):
    """Đọc file .env (KEY=VALUE mỗi dòng) vào biến môi trường, không ghi đè biến đã có."""
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env()
MODEL_PROVIDER = (os.environ.get("MODEL_PROVIDER") or "fake").strip().lower()
MODEL_NAME = (os.environ.get("MODEL_NAME") or "").strip()
API_KEY = (os.environ.get("API_KEY") or "").strip()


def post_json(url, headers, body, timeout=60, max_retries=4):
    """Gửi POST JSON, trả về JSON phản hồi. Hỗ trợ retry tự động khi gặp 503, 429 hoặc timeout."""
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        method="POST",
        headers=dict({"Content-Type": "application/json"}, **headers),
    )
    delay = 2
    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                data = json.loads(r.read().decode("utf-8"))
            if SHOW_RAW:
                print(json.dumps(data, ensure_ascii=False, indent=2)[:3000])
            return data
        except urllib.error.HTTPError as e:
            code = e.code
            err_body = e.read().decode("utf-8", "replace")[:300]
            if code in (503, 429, 408, 504) and attempt < max_retries - 1:
                time.sleep(delay)
                delay *= 2
                continue
            raise RuntimeError("HTTP %d: %s" % (code, err_body))
        except (urllib.error.URLError, TimeoutError) as e:
            if attempt < max_retries - 1:
                time.sleep(delay)
                delay *= 2
                continue
            raise RuntimeError("Network Error / Timeout: %s" % str(e))


def call_gemini(system: str, user: str) -> dict:
    model = MODEL_NAME or "gemini-3.1-flash-lite"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={API_KEY}"
    body = {
        "contents": [{"role": "user", "parts": [{"text": user}]}],
        "generationConfig": {"temperature": 0.2},
    }
    if system:
        body["systemInstruction"] = {"parts": [{"text": system}]}
    data = post_json(url, {}, body)
    cands = data.get("candidates") or []
    parts = (cands[0].get("content") or {}).get("parts") or [] if cands else []
    text = "".join(p.get("text", "") for p in parts)
    u = data.get("usageMetadata") or {}
    tokens_in = int(u.get("promptTokenCount", 0))
    tokens_out = int(u.get("candidatesTokenCount", 0)) + int(u.get("thoughtsTokenCount", 0))
    return {"text": text, "model": model, "tokens_in": tokens_in, "tokens_out": tokens_out}


def call_openai(system: str, user: str) -> dict:
    model = MODEL_NAME or "gpt-4o-mini"
    url = "https://api.openai.com/v1/chat/completions"
    messages = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": user}]
    data = post_json(url, {"Authorization": "Bearer " + API_KEY}, {"model": model, "messages": messages, "temperature": 0.2})
    u = data["usage"]
    return {
        "text": data["choices"][0]["message"]["content"],
        "model": model,
        "tokens_in": int(u["prompt_tokens"]),
        "tokens_out": int(u["completion_tokens"]),
    }


def call_claude(system: str, user: str) -> dict:
    model = MODEL_NAME or "claude-haiku-5-5"
    url = "https://api.anthropic.com/v1/messages"
    data = post_json(
        url,
        {"x-api-key": API_KEY, "anthropic-version": "2023-06-01"},
        {"model": model, "max_tokens": 1024, "system": system or "", "messages": [{"role": "user", "content": user}]},
    )
    text = "".join(b.get("text", "") for b in data.get("content", []) if b.get("type") == "text")
    u = data["usage"]
    return {
        "text": text,
        "model": model,
        "tokens_in": int(u["input_tokens"]),
        "tokens_out": int(u["output_tokens"]),
    }


@model_call
def call_model(system: str, user: str) -> dict:
    if MODEL_PROVIDER == "fake":
        last = (user.strip().splitlines() or [""])[-1]
        return {"text": "[câu trả lời giả — chưa nối model] " + last[:60], "model": "fake", "tokens_in": 0, "tokens_out": 0}
    if MODEL_PROVIDER == "gemini":
        return call_gemini(system, user)
    if MODEL_PROVIDER == "openai":
        return call_openai(system, user)
    if MODEL_PROVIDER == "anthropic":
        return call_claude(system, user)
    raise NotImplementedError(
        f"Chưa hỗ trợ MODEL_PROVIDER={MODEL_PROVIDER}. Dùng gemini, openai, anthropic hoặc fake."
    )
