#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""泛微 E10 OpenAPI CLI（首版：认证 + 流程查询）。

所有命令向 stdout 输出单个 JSON 对象。
文档：../fanwei-openapi/markdown/工作流程/所有流程列表.md 等。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests
import urllib3

urllib3.disable_warnings()
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent
STATE_DIR = ROOT / "state"
TOKEN_FILE = STATE_DIR / "token.json"
CONFIG_FILE = ROOT / "config.env"

# 官方路径（相对 OpenApiOrigin）
PATH_AUTHORIZE = "/oauth2/authorize"
PATH_ACCESS_TOKEN = "/oauth2/access_token"
PATH_REFRESH_TOKEN = "/oauth2/refresh_token"
PATH_LIST_ALL = "/api/workflow/list/paService/v1/getAllWorkflowRequestList"
PATH_COUNT_ALL = "/api/workflow/list/paService/v1/getAllWorkflowRequestCount"
PATH_LIST_MONITOR = "/api/workflow/list/paService/v1/getMonitorWorkflowRequestList"
PATH_COUNT_MONITOR = "/api/workflow/list/paService/v1/getMonitorWorkflowRequestCount"

FLOW_STATUS_LABEL = {
    0: "草稿", 1: "审批中", 2: "已退回", 3: "正常归档", 4: "强制归档",
    5: "已作废", 6: "待提交", 7: "暂停", 8: "撤销", -99: "已删除",
}


# ---------------------------------------------------------------- 输出 / 配置

def emit(payload: Dict[str, Any]) -> None:
    print(json.dumps(payload, ensure_ascii=False, default=str))


def fail(code: str, message: str, **extra: Any) -> None:
    out = {"ok": False, "status": "ERROR", "errorCode": code, "message": message}
    out.update(extra)
    emit(out)
    sys.exit(1)


def _load_dotenv(path: Path) -> Dict[str, str]:
    out: Dict[str, str] = {}
    if not path.exists():
        return out
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def load_config() -> Dict[str, str]:
    file_cfg = _load_dotenv(CONFIG_FILE)
    keys = [
        "E10_OPENAPI_ORIGIN", "E10_CORPID", "E10_APP_KEY", "E10_APP_SECRET",
        "E10_USERID", "E10_ACCESS_TOKEN", "E10_REFRESH_TOKEN",
    ]
    cfg: Dict[str, str] = {}
    for k in keys:
        cfg[k] = (os.environ.get(k) or file_cfg.get(k) or "").strip()
    origin = cfg["E10_OPENAPI_ORIGIN"].rstrip("/")
    if not origin:
        fail("NEEDS_CONFIG", f"缺少 E10_OPENAPI_ORIGIN。请复制 {CONFIG_FILE.name} 自 config.example.env 并填写。")
    cfg["E10_OPENAPI_ORIGIN"] = origin
    return cfg


def _read_token_cache() -> Dict[str, Any]:
    if not TOKEN_FILE.exists():
        return {}
    try:
        return json.loads(TOKEN_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _write_token_cache(data: Dict[str, Any]) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    TOKEN_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


# ---------------------------------------------------------------- HTTP

class OpenApiClient:
    def __init__(self, origin: str):
        self.origin = origin.rstrip("/")
        self.s = requests.Session()
        self.s.verify = False
        self.s.trust_env = False
        self.s.headers.update({
            "Accept": "application/json, text/plain, */*",
            "User-Agent": "e10-openapi-cli/0.1",
        })

    def post_json(self, path: str, body: Optional[dict] = None,
                  params: Optional[dict] = None) -> Any:
        url = self.origin + path
        r = self.s.post(url, json=body or {}, params=params or {}, timeout=60)
        return self._parse(r, url)

    def get(self, path: str, params: Optional[dict] = None) -> Any:
        url = self.origin + path
        r = self.s.get(url, params=params or {}, timeout=60)
        return self._parse(r, url)

    def post_form(self, path: str, data: Optional[dict] = None,
                  params: Optional[dict] = None) -> Any:
        url = self.origin + path
        r = self.s.post(url, data=data or {}, params=params or {}, timeout=60)
        return self._parse(r, url)

    @staticmethod
    def _parse(r: requests.Response, url: str) -> Any:
        try:
            data = r.json()
        except Exception:
            fail("HTTP_ERROR", f"非 JSON 响应 HTTP {r.status_code}",
                 url=url, bodyPreview=(r.text or "")[:500])
        if r.status_code >= 400:
            fail("HTTP_ERROR", f"HTTP {r.status_code}", url=url, response=data)
        return data


def resolve_access_token(cfg: Dict[str, str], allow_expired: bool = False) -> str:
    if cfg.get("E10_ACCESS_TOKEN"):
        return cfg["E10_ACCESS_TOKEN"]
    cache = _read_token_cache()
    token = str(cache.get("accessToken") or cache.get("access_token") or "").strip()
    if not token:
        fail("NEEDS_AUTH", "无 access_token。请先执行: auth code → auth token --code <code>，"
             "或在 config.env / 环境变量设置 E10_ACCESS_TOKEN。")
    expires_at = cache.get("expiresAt")
    if expires_at and not allow_expired and time.time() > float(expires_at) - 60:
        # 尝试 refresh
        refresh = str(cache.get("refreshToken") or cache.get("refresh_token")
                      or cfg.get("E10_REFRESH_TOKEN") or "").strip()
        if refresh:
            try:
                return _do_refresh(cfg, refresh)["accessToken"]
            except SystemExit:
                raise
            except Exception as e:
                fail("TOKEN_EXPIRED", f"access_token 已过期且 refresh 失败: {e}")
        fail("TOKEN_EXPIRED", "access_token 已过期，请重新 auth token。")
    return token


def require_userid(cfg: Dict[str, str]) -> str:
    uid = cfg.get("E10_USERID") or ""
    if not uid:
        fail("NEEDS_CONFIG", "缺少 E10_USERID（OpenAPI 用户 ID）。")
    return str(uid)


# ---------------------------------------------------------------- auth 命令

def cmd_auth_code(cfg: Dict[str, str], args: argparse.Namespace) -> None:
    corpid = cfg.get("E10_CORPID") or ""
    if not corpid:
        fail("NEEDS_CONFIG", "缺少 E10_CORPID。")
    client = OpenApiClient(cfg["E10_OPENAPI_ORIGIN"])
    params = {
        "corpid": corpid,
        "response_type": "code",
        "state": args.state or "e10cli",
    }
    # 文档支持 GET/POST
    data = client.get(PATH_AUTHORIZE, params=params) if args.method == "GET" \
        else client.post_json(PATH_AUTHORIZE, body=params, params=params)
    code = _dig(data, "code", "data.code")
    emit({
        "ok": True,
        "status": "CODE_READY" if code else "RAW",
        "code": code,
        "raw": data,
        "hint": "code 约 10 分钟有效且一次性。下一步: auth token --code <code>",
    })


def cmd_auth_token(cfg: Dict[str, str], args: argparse.Namespace) -> None:
    app_key = cfg.get("E10_APP_KEY") or ""
    app_secret = cfg.get("E10_APP_SECRET") or ""
    if not app_key or not app_secret:
        fail("NEEDS_CONFIG", "缺少 E10_APP_KEY / E10_APP_SECRET。")
    if not args.code:
        fail("NEEDS_INPUT", "请传 --code。")
    client = OpenApiClient(cfg["E10_OPENAPI_ORIGIN"])
    body = {
        "app_key": app_key,
        "app_secret": app_secret,
        "grant_type": "authorization_code",
        "code": args.code,
    }
    data = client.post_json(PATH_ACCESS_TOKEN, body=body)
    saved = _persist_token_response(data)
    emit({
        "ok": True,
        "status": "TOKEN_READY",
        "accessToken": saved.get("accessToken"),
        "expiresIn": saved.get("expiresIn"),
        "expiresAt": saved.get("expiresAt"),
        "tokenFile": str(TOKEN_FILE),
        "raw": data,
    })


def _do_refresh(cfg: Dict[str, str], refresh_token: str) -> Dict[str, Any]:
    client = OpenApiClient(cfg["E10_OPENAPI_ORIGIN"])
    body = {"grant_type": "refresh_token", "refresh_token": refresh_token}
    data = client.post_json(PATH_REFRESH_TOKEN, body=body)
    return _persist_token_response(data)


def cmd_auth_refresh(cfg: Dict[str, str], _args: argparse.Namespace) -> None:
    cache = _read_token_cache()
    refresh = str(cache.get("refreshToken") or cache.get("refresh_token")
                  or cfg.get("E10_REFRESH_TOKEN") or "").strip()
    if not refresh:
        fail("NEEDS_AUTH", "无 refresh_token 可刷新。")
    saved = _do_refresh(cfg, refresh)
    emit({
        "ok": True,
        "status": "TOKEN_READY",
        "accessToken": saved.get("accessToken"),
        "expiresIn": saved.get("expiresIn"),
        "expiresAt": saved.get("expiresAt"),
        "tokenFile": str(TOKEN_FILE),
    })


def cmd_auth_status(cfg: Dict[str, str], _args: argparse.Namespace) -> None:
    cache = _read_token_cache()
    token = cfg.get("E10_ACCESS_TOKEN") or cache.get("accessToken") or cache.get("access_token")
    expires_at = cache.get("expiresAt")
    remaining = None
    if expires_at:
        remaining = int(float(expires_at) - time.time())
    emit({
        "ok": True,
        "status": "READY" if token else "NEEDS_AUTH",
        "hasAccessToken": bool(token),
        "hasRefreshToken": bool(cache.get("refreshToken") or cfg.get("E10_REFRESH_TOKEN")),
        "expiresAt": expires_at,
        "remainingSeconds": remaining,
        "openapiOrigin": cfg["E10_OPENAPI_ORIGIN"],
        "userid": cfg.get("E10_USERID") or None,
        "tokenFile": str(TOKEN_FILE) if TOKEN_FILE.exists() else None,
        "configFile": str(CONFIG_FILE) if CONFIG_FILE.exists() else None,
    })


def _persist_token_response(data: Any) -> Dict[str, Any]:
    # 兼容多种返回形态
    access = _dig(data, "accessToken", "access_token", "data.accessToken", "data.access_token")
    refresh = _dig(data, "refreshToken", "refresh_token", "data.refreshToken", "data.refresh_token")
    expires_in = _dig(data, "expires_in", "expire_in", "expiresIn", "data.expires_in", "data.expire_in")
    err = _dig(data, "errcode", "errCode", "data.errcode")
    if err not in (None, "", 0, "0") and not access:
        fail("AUTH_FAILED", str(_dig(data, "errmsg", "errMsg", "message") or data), raw=data)
    if not access:
        fail("AUTH_FAILED", "响应中未找到 accessToken", raw=data)
    expires_in_i = int(expires_in or 7200)
    saved = {
        "accessToken": str(access),
        "refreshToken": str(refresh) if refresh else None,
        "expiresIn": expires_in_i,
        "expiresAt": time.time() + expires_in_i,
        "savedAt": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "raw": data,
    }
    _write_token_cache(saved)
    return saved


# ---------------------------------------------------------------- condition / workflow

def build_condition(args: argparse.Namespace) -> Dict[str, Any]:
    cond: Dict[str, Any] = {}
    if getattr(args, "title", None):
        cond["requestname"] = args.title
    if getattr(args, "request_mark", None):
        cond["requestmark"] = args.request_mark
    if getattr(args, "workflow_id", None):
        cond["workflowid"] = args.workflow_id
    if getattr(args, "workflow_type", None):
        cond["workflowtype"] = args.workflow_type
    if getattr(args, "creater", None):
        cond["createrList"] = args.creater
    if getattr(args, "status", None):
        statuses: List[int] = []
        for part in str(args.status).split(","):
            part = part.strip()
            if part == "":
                continue
            statuses.append(int(part))
        if statuses:
            cond["flowStatusList"] = statuses
    if getattr(args, "create_start", None) or getattr(args, "create_end", None):
        cond["createdate"] = "CUSTOM_DATE"
        if args.create_start:
            cond["createdateCustomStart"] = args.create_start
        if args.create_end:
            cond["createdateCustomEnd"] = args.create_end
    elif getattr(args, "create_date", None):
        cond["createdate"] = args.create_date
    if getattr(args, "condition_json", None):
        extra = _load_json_arg(args.condition_json)
        if not isinstance(extra, dict):
            fail("NEEDS_INPUT", "--condition-json 必须是 JSON 对象")
        cond.update(extra)
    return cond


def build_result_data_param(args: argparse.Namespace) -> Optional[Dict[str, Any]]:
    flags = {
        "needFormDetail": getattr(args, "need_form_detail", False),
        "needCurrentNode": getattr(args, "need_current_node", False),
        "needWfNames": getattr(args, "need_wf_names", False),
        "needLastOperatorInfo": getattr(args, "need_last_operator", False),
        "needUserDepartmentName": getattr(args, "need_dept_name", False),
        "needFormId": getattr(args, "need_form_id", False),
    }
    # 默认打开工作流名称，列表更可读
    if not any(flags.values()) and not getattr(args, "raw_fields", False):
        flags["needWfNames"] = True
    active = {k: True for k, v in flags.items() if v}
    return active or None


def _load_json_arg(value: str) -> Any:
    p = Path(value)
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return json.loads(value)


def _workflow_body(cfg: Dict[str, str], args: argparse.Namespace,
                   with_page: bool) -> Dict[str, Any]:
    token = resolve_access_token(cfg)
    userid = require_userid(cfg)
    body: Dict[str, Any] = {
        "access_token": token,
        "userid": userid,
    }
    if with_page:
        body["pageNo"] = int(args.page)
        body["pageSize"] = int(args.size)
    if getattr(args, "merge_show", False):
        body["mergeShow"] = True
    cond = build_condition(args)
    if cond:
        body["condition"] = cond
    rdp = build_result_data_param(args) if with_page else None
    if rdp:
        # 文档把 need* 写在 resultDataParam 下；同时有些环境也接受顶层。
        # 按文档放入 condition 同级的常见形态：部分实现直接摊在 body。
        # 这里按 raw 文档 resultDataParam 结构放 body。
        body["resultDataParam"] = rdp
        # 兼容：部分版本要求塞进 condition
        body.setdefault("condition", {})
        if isinstance(body["condition"], dict):
            body["condition"].setdefault("resultDataParam", rdp)
    return body


def _normalize_list_payload(data: Any) -> Dict[str, Any]:
    """尽量抽出列表与总数，保留 raw。"""
    items: List[Any] = []
    if isinstance(data, list):
        items = data
    elif isinstance(data, dict):
        for key in ("data", "list", "records", "rows", "result"):
            v = data.get(key)
            if isinstance(v, list):
                items = v
                break
            if isinstance(v, dict):
                for k2 in ("list", "records", "rows", "data"):
                    if isinstance(v.get(k2), list):
                        items = v[k2]
                        break
                if items:
                    break
        if not items and isinstance(data.get("data"), dict):
            # 有的返回 data 本身是 map of requestid
            pass
    enriched = []
    for it in items:
        if isinstance(it, dict):
            row = dict(it)
            fs = row.get("flowStatus")
            if fs is not None and "flowStatusLabel" not in row:
                try:
                    row["flowStatusLabel"] = FLOW_STATUS_LABEL.get(int(fs), str(fs))
                except Exception:
                    row["flowStatusLabel"] = str(fs)
            enriched.append(row)
        else:
            enriched.append(it)
    count = None
    if isinstance(data, dict):
        count = _dig(data, "count", "total", "data.count", "data.total")
    return {"items": enriched, "count": count, "itemCount": len(enriched)}


def cmd_workflow_list(cfg: Dict[str, str], args: argparse.Namespace, kind: str) -> None:
    path = PATH_LIST_ALL if kind == "all" else PATH_LIST_MONITOR
    client = OpenApiClient(cfg["E10_OPENAPI_ORIGIN"])

    if not args.all_pages:
        body = _workflow_body(cfg, args, with_page=True)
        # 文档备注：access_token 放 param
        params = {"access_token": body["access_token"]}
        data = client.post_json(path, body=body, params=params)
        norm = _normalize_list_payload(data)
        emit({
            "ok": True,
            "status": "OK",
            "api": path,
            "kind": kind,
            "pageNo": int(args.page),
            "pageSize": int(args.size),
            "condition": body.get("condition"),
            "itemCount": norm["itemCount"],
            "count": norm["count"],
            "items": norm["items"],
            "raw": data,
            "scopeNote": (
                "默认返回当前 userid 参与的流程" if kind == "all"
                else "返回该 userid 有监控权限可见的流程"
            ),
        })
        return

    # 翻页
    all_items: List[Any] = []
    start_page = int(args.page)
    page = start_page
    size = int(args.size)
    max_pages = int(args.max_pages)
    total_hint = None
    last_raw = None
    pages_fetched = 0
    while pages_fetched < max_pages:
        args.page = page
        body = _workflow_body(cfg, args, with_page=True)
        params = {"access_token": body["access_token"]}
        data = client.post_json(path, body=body, params=params)
        last_raw = data
        pages_fetched += 1
        norm = _normalize_list_payload(data)
        if norm["count"] is not None:
            total_hint = norm["count"]
        batch = norm["items"]
        all_items.extend(batch)
        if len(batch) < size:
            break
        if total_hint is not None:
            try:
                if len(all_items) >= int(total_hint):
                    break
            except Exception:
                pass
        page += 1
    emit({
        "ok": True,
        "status": "OK",
        "api": path,
        "kind": kind,
        "allPages": True,
        "startPage": start_page,
        "pagesFetched": pages_fetched,
        "pageSize": size,
        "itemCount": len(all_items),
        "count": total_hint,
        "items": all_items,
        "rawLastPage": last_raw,
        "scopeNote": (
            "默认返回当前 userid 参与的流程" if kind == "all"
            else "返回该 userid 有监控权限可见的流程"
        ),
    })


def cmd_workflow_list_all(cfg: Dict[str, str], args: argparse.Namespace) -> None:
    cmd_workflow_list(cfg, args, "all")


def cmd_workflow_list_monitor(cfg: Dict[str, str], args: argparse.Namespace) -> None:
    cmd_workflow_list(cfg, args, "monitor")


def cmd_workflow_count(cfg: Dict[str, str], args: argparse.Namespace, kind: str) -> None:
    path = PATH_COUNT_ALL if kind == "all" else PATH_COUNT_MONITOR
    client = OpenApiClient(cfg["E10_OPENAPI_ORIGIN"])
    body = _workflow_body(cfg, args, with_page=False)
    params = {"access_token": body["access_token"]}
    data = client.post_json(path, body=body, params=params)
    # 实测形态：{"message":{...},"data":{"count":"77"}}
    count = _dig(data, "data.count", "count", "data.total", "total")
    if count is None and isinstance(data, dict):
        inner = data.get("data")
        if isinstance(inner, (int, float, str)):
            count = inner
        elif isinstance(inner, dict) and "count" in inner:
            count = inner["count"]
    if isinstance(data, (int, float, str)) and str(data).isdigit():
        count = data
    emit({
        "ok": True,
        "status": "OK",
        "api": path,
        "kind": kind,
        "condition": body.get("condition"),
        "count": count,
        "raw": data,
        "scopeNote": (
            "默认统计当前 userid 参与的流程" if kind == "all"
            else "统计该 userid 有监控权限可见的流程"
        ),
    })


def cmd_workflow_count_all(cfg: Dict[str, str], args: argparse.Namespace) -> None:
    cmd_workflow_count(cfg, args, "all")


def cmd_workflow_count_monitor(cfg: Dict[str, str], args: argparse.Namespace) -> None:
    cmd_workflow_count(cfg, args, "monitor")


# ---------------------------------------------------------------- utils

def _dig(obj: Any, *paths: str) -> Any:
    for path in paths:
        cur = obj
        ok = True
        for part in path.split("."):
            if isinstance(cur, dict) and part in cur:
                cur = cur[part]
            else:
                ok = False
                break
        if ok and cur is not None:
            return cur
    return None


# ---------------------------------------------------------------- argparse

def add_filter_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--title", help="审批标题（condition.requestname）")
    p.add_argument("--request-mark", help="审批编号")
    p.add_argument("--workflow-id", help="工作流 id，多个逗号分隔")
    p.add_argument("--workflow-type", help="工作流类型 id，多个逗号分隔")
    p.add_argument("--creater", help="发起人 userid，多个逗号分隔 → createrList")
    p.add_argument("--status", help="流转状态，逗号分隔：0草稿 1审批中 2退回 3归档 ...")
    p.add_argument("--create-date",
                   help="发起日期枚举：TODAY/CURRENT_WEEK/CURRENT_MONTH/CURRENT_YEAR/...")
    p.add_argument("--create-start", help="自定义发起开始 yyyy-MM-dd HH:mm:ss")
    p.add_argument("--create-end", help="自定义发起结束 yyyy-MM-dd HH:mm:ss")
    p.add_argument("--condition-json", help="额外 condition JSON 字符串或文件路径")
    p.add_argument("--merge-show", action="store_true", help="mergeShow=true")


def add_list_args(p: argparse.ArgumentParser) -> None:
    add_filter_args(p)
    p.add_argument("--page", type=int, default=1)
    p.add_argument("--size", type=int, default=20)
    p.add_argument("--all-pages", action="store_true", help="自动翻页直至末页")
    p.add_argument("--max-pages", type=int, default=50, help="--all-pages 时最大页数")
    p.add_argument("--need-form-detail", action="store_true")
    p.add_argument("--need-current-node", action="store_true")
    p.add_argument("--need-wf-names", action="store_true")
    p.add_argument("--need-last-operator", action="store_true")
    p.add_argument("--need-dept-name", action="store_true")
    p.add_argument("--need-form-id", action="store_true")
    p.add_argument("--raw-fields", action="store_true",
                   help="不自动附加 needWfNames")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="e10_openapi",
        description="泛微 E10 OpenAPI CLI（认证 + 流程查询）",
    )
    sub = parser.add_subparsers(dest="group", required=True)

    # auth
    auth = sub.add_parser("auth", help="认证：code / token / refresh / status")
    auth_sub = auth.add_subparsers(dest="action", required=True)

    p_code = auth_sub.add_parser("code", help="获取授权 code")
    p_code.add_argument("--state", default="e10cli")
    p_code.add_argument("--method", choices=["GET", "POST"], default="GET")
    p_code.set_defaults(func=cmd_auth_code)

    p_token = auth_sub.add_parser("token", help="用 code 换 access_token")
    p_token.add_argument("--code", required=True)
    p_token.set_defaults(func=cmd_auth_token)

    p_refresh = auth_sub.add_parser("refresh", help="刷新 access_token")
    p_refresh.set_defaults(func=cmd_auth_refresh)

    p_status = auth_sub.add_parser("status", help="查看本地令牌状态")
    p_status.set_defaults(func=cmd_auth_status)

    # workflow
    wf = sub.add_parser("workflow", help="流程查询")
    wf_sub = wf.add_subparsers(dest="action", required=True)

    p_list = wf_sub.add_parser("list-all", help="所有流程列表（当前用户参与）")
    add_list_args(p_list)
    p_list.set_defaults(func=cmd_workflow_list_all)

    p_count = wf_sub.add_parser("count-all", help="所有流程数量（当前用户参与）")
    add_filter_args(p_count)
    p_count.set_defaults(func=cmd_workflow_count_all)

    p_lm = wf_sub.add_parser("list-monitor", help="监控列表（需监控权限）")
    add_list_args(p_lm)
    p_lm.set_defaults(func=cmd_workflow_list_monitor)

    p_cm = wf_sub.add_parser("count-monitor", help="监控列表数量")
    add_filter_args(p_cm)
    p_cm.set_defaults(func=cmd_workflow_count_monitor)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    cfg = load_config()
    # status / code 不强制 token；其余按命令自己检查
    try:
        args.func(cfg, args)
    except requests.RequestException as e:
        fail("NETWORK_ERROR", str(e))


if __name__ == "__main__":
    main()
