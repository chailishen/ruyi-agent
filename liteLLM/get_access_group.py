#!/usr/bin/env python3
"""
Query a LiteLLM access group by ID.

API: GET /v1/access_group/{access_group_id}

Run:
    python3 get_access_group.py
    python3 get_access_group.py <access_group_id>
    python3 get_access_group.py --list

Before running, edit config.py and set ADMIN_API_KEY / ACCESS_GROUP_ID.
Note: this route requires a Master Key or admin key, not a regular virtual key.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from config import ACCESS_GROUP_ID, ADMIN_API_KEY, BASE_URL

BASE_URL = BASE_URL.rstrip("/")


def request_json(method: str, path: str) -> dict[str, Any]:
    if not ADMIN_API_KEY or ADMIN_API_KEY == "请替换成你的MasterKey":
        raise RuntimeError(
            "请先在 config.py 中设置 ADMIN_API_KEY（LiteLLM Master Key 或管理员 key）。"
            "普通虚拟 key 无法调用 /v1/access_group 接口。"
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


def list_access_groups() -> list[dict[str, Any]]:
    data = request_json("GET", "/access_group")
    groups = data if isinstance(data, list) else data.get("access_groups", data.get("data", []))
    if not isinstance(groups, list):
        raise RuntimeError(f"/v1/access_group 返回格式异常：{data}")
    return groups


def get_access_group(access_group_id: str) -> dict[str, Any]:
    data = request_json("GET", f"/access_group/{access_group_id}")
    if not isinstance(data, dict):
        raise RuntimeError(f"/v1/access_group/{access_group_id} 返回格式异常：{data}")
    return data


def print_access_group(group: dict[str, Any]) -> None:
    print("访问组 ID：", group.get("access_group_id", "<unknown>"))
    print("访问组名称：", group.get("access_group_name", "<unknown>"))

    description = group.get("description")
    if description:
        print("描述：", description)

    model_names = group.get("access_model_names") or []
    print(f"\n可用模型（{len(model_names)} 个）：")
    if model_names:
        for index, model_name in enumerate(model_names, start=1):
            print(f"  {index}. {model_name}")
    else:
        print("  （无）")

    for label, field in [
        ("MCP 服务", "access_mcp_server_ids"),
        ("Agent", "access_agent_ids"),
        ("关联团队", "assigned_team_ids"),
        ("关联 Key", "assigned_key_ids"),
    ]:
        values = group.get(field) or []
        if values:
            print(f"\n{label}：")
            for value in values:
                print(f"  - {value}")

    created_at = group.get("created_at")
    updated_at = group.get("updated_at")
    if created_at or updated_at:
        print("\n时间：")
        if created_at:
            print("  创建：", created_at)
        if updated_at:
            print("  更新：", updated_at)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="查询 LiteLLM 访问组信息")
    parser.add_argument(
        "access_group_id",
        nargs="?",
        default=ACCESS_GROUP_ID,
        help="访问组 ID；也可在 config.py 中设置 ACCESS_GROUP_ID",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="列出所有访问组（GET /v1/access_group）",
    )
    parser.add_argument(
        "--raw",
        action="store_true",
        help="输出完整 JSON 响应",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()

    try:
        if args.list:
            groups = list_access_groups()
            if args.raw:
                print(json.dumps(groups, ensure_ascii=False, indent=2))
                return 0

            if not groups:
                print("没有查询到访问组。")
                return 0

            print(f"共 {len(groups)} 个访问组：")
            for index, group in enumerate(groups, start=1):
                group_id = group.get("access_group_id", group.get("id", "<unknown>"))
                group_name = group.get("access_group_name", group.get("access_group", "<unknown>"))
                model_count = len(group.get("access_model_names") or group.get("model_names") or [])
                print(f"{index}. {group_name}  id={group_id}  models={model_count}")
            return 0

        access_group_id = (args.access_group_id or "").strip()
        if not access_group_id:
            raise RuntimeError("请传入 access_group_id，或在 config.py 中设置 ACCESS_GROUP_ID。")

        group = get_access_group(access_group_id)
        if args.raw:
            print(json.dumps(group, ensure_ascii=False, indent=2))
            return 0

        print_access_group(group)
    except Exception as exc:
        print(f"查询失败：{exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
