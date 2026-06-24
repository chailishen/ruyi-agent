#!/usr/bin/env python3
"""
Query a LiteLLM user by user_id and print everything the API returns.

API: GET /user/info?user_id={user_id}

Run:
    python3 get_user_info.py <user_id>
    python3 get_user_info.py            # 使用 config.py 中的 USER_ID

Before running, edit config.py and set ADMIN_API_KEY（以及可选的 USER_ID）。
Note: this route requires a Master Key or admin key, not a regular virtual key.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from config import ADMIN_API_KEY, BASE_URL

# /user/info 是根路径下的管理接口，不在 /v1 下，这里去掉可能的 /v1 后缀
BASE_URL = BASE_URL.rstrip("/")
if BASE_URL.endswith("/v1"):
    BASE_URL = BASE_URL[: -len("/v1")]

try:
    from config import USER_ID  # type: ignore
except ImportError:
    USER_ID = ""


def request_json(method: str, path: str) -> Any:
    if not ADMIN_API_KEY or ADMIN_API_KEY == "请替换成你的MasterKey":
        raise RuntimeError(
            "请先在 config.py 中设置 ADMIN_API_KEY（LiteLLM Master Key 或管理员 key）。"
            "普通虚拟 key 无法调用 /user/info 接口。"
        )

    request = Request(
        f"{BASE_URL}{path}",
        method=method,
        headers={
            "Authorization": f"Bearer {ADMIN_API_KEY}",
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


def get_user_info(user_id: str) -> Any:
    return request_json("GET", f"/user/info?user_id={quote(user_id, safe='')}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="查询 LiteLLM 用户信息（GET /user/info）")
    parser.add_argument(
        "user_id",
        nargs="?",
        default=USER_ID,
        help="用户 ID；也可在 config.py 中设置 USER_ID",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()

    user_id = (args.user_id or "").strip()
    if not user_id:
        print("请传入 user_id，或在 config.py 中设置 USER_ID。", file=sys.stderr)
        return 1

    try:
        data = get_user_info(user_id)
    except Exception as exc:
        print(f"查询失败：{exc}", file=sys.stderr)
        return 1

    print(json.dumps(data, ensure_ascii=False, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
