#!/usr/bin/env python3
"""
List models available to the configured LiteLLM virtual key.

Run:
    python3 list_models.py

Before running, edit config.py and set API_KEY.
"""

from __future__ import annotations

import json
import sys
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from config import API_KEY, BASE_URL


BASE_URL = BASE_URL.rstrip("/")


def request_json(method: str, path: str) -> dict[str, Any]:
    if not API_KEY or API_KEY == "请替换成你的虚拟key":
        raise RuntimeError("请先打开 config.py，把 API_KEY 改成 LiteLLM 后台创建的虚拟 key。")

    request = Request(
        f"{BASE_URL}{path}",
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


def list_models() -> list[dict[str, Any]]:
    data = request_json("GET", "/models")
    models = data.get("data", [])
    if not isinstance(models, list):
        raise RuntimeError(f"/v1/models 返回格式异常：{data}")
    return models


def main() -> int:
    try:
        models = list_models()
    except Exception as exc:
        print(f"查询失败：{exc}", file=sys.stderr)
        return 1

    if not models:
        print("当前 key 没有查询到可用模型。")
        return 0

    print(f"当前 key 可使用 {len(models)} 个模型：")
    for index, model in enumerate(models, start=1):
        model_id = model.get("id", "<unknown>")
        owned_by = model.get("owned_by")
        if owned_by:
            print(f"{index}. {model_id}  owned_by={owned_by}")
        else:
            print(f"{index}. {model_id}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
