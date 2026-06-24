#!/usr/bin/env python3
"""
Call a LiteLLM AI Gateway using the OpenAI-compatible API.

Run:
    python3 call_litellm.py

Before running, edit config.py and set API_KEY / MODEL.
"""

from __future__ import annotations

import json
import sys
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from config import API_KEY, BASE_URL, MODEL, PROMPT

BASE_URL = BASE_URL.rstrip("/")


def request_json(method: str, path: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    if not API_KEY or API_KEY == "请替换成你的虚拟key":
        raise RuntimeError("请先打开 config.py，把 API_KEY 改成 LiteLLM 后台创建的虚拟 key。")

    body = None if payload is None else json.dumps(payload).encode("utf-8")
    request = Request(
        f"{BASE_URL}{path}",
        data=body,
        method=method,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
    )

    try:
        with urlopen(request, timeout=60) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {error_body}") from exc
    except URLError as exc:
        raise RuntimeError(f"请求网关失败：{exc.reason}") from exc


def list_models() -> list[str]:
    data = request_json("GET", "/models")
    return [item["id"] for item in data.get("data", []) if "id" in item]


def choose_model() -> str:
    if MODEL:
        return MODEL

    models = list_models()
    if not models:
        raise RuntimeError("没有从 /v1/models 获取到可用模型，请检查 LiteLLM 后台模型配置。")

    print("未设置 LITELLM_MODEL，自动使用第一个模型：", models[0])
    print("可用模型：")
    for model in models:
        print(" -", model)
    print()
    return models[0]


def chat_completion(model: str, prompt: str) -> str:
    data = request_json(
        "POST",
        "/chat/completions",
        {
            "model": model,
            "messages": [
                {"role": "system", "content": "你是一个简洁、可靠的中文助手。"},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.7,
        },
    )
    return data["choices"][0]["message"]["content"]


def main() -> int:
    try:
        model = choose_model()
        answer = chat_completion(model, PROMPT)
    except Exception as exc:
        print(f"调用失败：{exc}", file=sys.stderr)
        return 1

    print("模型：", model)
    print("回答：")
    print(answer)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
