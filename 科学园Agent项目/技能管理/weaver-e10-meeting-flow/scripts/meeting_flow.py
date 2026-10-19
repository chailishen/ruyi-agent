#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""泛微 E10「会议申请」工作流发起 CLI（会议模块接口链，非普通 workflow 表单链）。

阶段式命令（前 6 个只读/准备，只有 create 会写入；写入结果不确定时绝不重试）：
  session   检查登录态
  workflows 确认当前用户可发起「会议申请」
  form      读会议表单能力表（字段/必填/选项/布局），生成 context
  rooms     列出/匹配会议室
  people    人员姓名 -> HRM id
  depts     部门名称 -> 部门 id
  conflict  会议室/参会人冲突预检
  prepare   校验并归一化用户数据，解析名称、运行冲突预检，产出待确认预览
  create    --confirm 执行写入链（草稿 / --submit 提交）
  detail    按 requestId 回读会议字段

所有命令输出单个 JSON 对象到 stdout。写操作前必须由调用方（Agent）向用户展示预览并取得明确确认。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import urllib3
import requests

urllib3.disable_warnings()
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# ---------------------------------------------------------------- 部署期常量
# 雄安科学园 E10（2026-10-16 实测）。workflowId 是本 skill 的目标流程；
# formId/layoutId/layoutMultiId 在 form 阶段全部动态获取，不在此硬编码。
DEFAULT_BASE_URL = "https://zhxz.xasp.com.cn"
DEFAULT_WORKFLOW_ID = "1302788388361633792"
DEFAULT_WORKFLOW_NAME = "会议申请"

# 会议自定义表单上的文本域字段（会议物资 hywz）。该字段不出现在 PC 布局与
# getMeetingDetailField ADD 响应中，只能随 saveFormData 的 dataDetails 提交；
# fieldId 为部署期实测值（与 workflowId 同级的环境事实）。
CUSTOM_TEXT_FIELDS = {"materials": "1302788014707867664"}

SKILL_ROOT = Path(__file__).resolve().parent.parent
STATE_DIR = SKILL_ROOT / "state"
CONTEXT_DIR = STATE_DIR / "create_contexts"
DT_RE = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$")

# 会议业务字段中文显示名（仅展示用；字段能力/必填/选项均以系统实时返回为准）
KEY_LABELS = {
    "name": "会议名称", "mtType": "会议类型", "caller": "发起人", "contacter": "联系人",
    "mtDesc": "会议内容", "mtAccessorys": "相关附件", "frequent": "重复规则",
    "beginDatetime": "开始时间", "endDatetime": "结束时间", "address": "会议地点",
    "customizeAddress": "自定义会议地点", "remindType": "提醒方式",
    "remindImmediately": "立即提醒", "remindBeforeStart": "开始前提醒",
    "remindBeforeEnd": "结束前提醒", "remindToCreater": "提醒给创建人",
    "hrmMembers": "参会人员", "orgMembers": "参会部门", "totalMember": "应到人数",
    "otherMembers": "其他人员", "crmMembers": "参会客户",
}
# 提交 operate 时需要的非业务默认字段（周期/标签等，非周期会议也必须原样带）
OPERATE_DEFAULTS: Dict[str, Any] = {
    "hasVideo": 0, "meetingStatus": 0, "tenantKey": "", "crmTotalMember": 0,
    "roomUsageLink": "会议室使用情况", "frequent": "0", "customizeAddress": "",
    "monthLabel": "月", "weekLabel": "周", "byDateType": "0", "byDay": "",
    "remindToCreater": "0", "repeatDesc": "", "remindBeforeStart": "0",
    "mtDesc": "", "eachLabel": "每", "remindImmediately": 0,
    "remindHoursBeforeStart": 0, "crmMembers": "", "remindTimesBeforeStart": 0,
    "timesLabel": "次后", "repeatRuleEx": "", "yearLabel": "年", "byMonth": "",
    "count": 0, "occurLabel": "发生", "byDayCount": "", "sort": "0",
    "dayLabel": "天", "remindBeforeEnd": "0", "remindHoursBeforeEnd": 0,
    "contacter": "", "remindTimesBeforeEnd": 0, "mtAccessorys": "",
    "interval": 1, "finishAt": "2", "NoLabel": "第", "byMonthDay": "",
    "remindStartList": [], "remindEndList": [], "serviceItems": "",
    "isFromWorkflow": True, "operateType": "ADD", "fromWorkflow": True,
    "id": "", "isReadOnly": False, "isMobile": False,
}
FLOW_CREATE_DEFAULTS: Dict[str, Any] = {
    "isCreate": True, "apiModule": "workflow", "identityType": 0,
    "isAgent": False, "beAgentId": "0", "isTest": False, "requestLevel": "0",
    "secLevel": "0", "secValidity": "", "needWfBack": True, "sameOperateId": None,
    "customBtnId": None, "confirmSecondSubmit": False, "selectFlowParam": None,
    "freeChoiceNodeIds": None, "nodeAddOperators": None, "voteSubmit": False,
    "sealId": None, "unNeedVerifyPrivacyAgreement": 1, "remark": "",
    "attachments": [], "fileData": [], "locationData": {},
    "comment": {"relevanceList": [], "imAtContent": "", "atLinkList": [],
                "content": "", "originContent": ""},
    "quoteData": [], "fullTextAnnotationData": [],
    "signatureData": {"signatureImgId": ""},
    "userSignatureData": {"signatureImgId": ""},
    "secondVerifySet": {
        "applyEnableViewAuth": False, "applyViewVerfiyType": 0,
        "applyEnableHandleAuth": False, "applyHandleVerifyType": 0,
        "applyVerifyOperation": "0,1,11,4,5", "applyHandleQysServer": "-1",
        "applyEnableDataProtect": False, "applyDataProtectMode": 0,
        "applyDataInteractMode": -1, "applyQysServer": "-1",
        "applyDataVerifyOperation": "0,1,11,4,5", "nodeEnableViewAuth": False,
        "nodeEnableDoubleAuth": False, "nodeAuthVerifier": "-1",
        "nodeEnableHandleAuth": False, "nodeEnableDataProtect": False,
        "nodeFieldDataProtect": [], "enableHandDoubleAuth": False,
        "handAuthVerifier": "-1", "nodeEnableSignatures": False,
    },
    "clientType": 0,
}


class CliError(Exception):
    def __init__(self, code: str, message: str, extra: Optional[dict] = None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.extra = extra or {}


# ---------------------------------------------------------------- 输出
def emit(payload: Dict[str, Any]) -> None:
    print(json.dumps(payload, ensure_ascii=False, default=str))


def fail(code: str, message: str, **extra: Any) -> None:
    out = {"ok": False, "status": "ERROR", "errorCode": code, "message": message}
    out.update(extra)
    emit(out)
    sys.exit(1)


# ---------------------------------------------------------------- 认证
def _parse_kv(text: str) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            k, v = line.split("=", 1)
        elif ":" in line:
            k, v = line.split(":", 1)
        else:
            continue
        out[k.strip()] = v.strip()
    return out


def _runtime_from_e10_login() -> Optional[Dict[str, str]]:
    """生产路径：weaver-e10-login skill 的 e10-login CLI。"""
    exe = shutil.which("e10-login") or shutil.which("e10-login.cmd") or shutil.which("e10-login.exe")
    if not exe:
        return None
    try:
        p = subprocess.run([exe, "status"], capture_output=True, text=True, timeout=20)
        if p.returncode != 0:
            return None
        st = _parse_kv(p.stdout)
        base = (st.get("baseUrl") or "").strip()
        et = (st.get("ETEAMSID") or st.get("eteamsid") or "").strip()
        if not base or not et:
            return None
        cookie = f"ETEAMSID={et}"
        ua = ""
        w = subprocess.run([exe, "whoami"], capture_output=True, text=True, timeout=20)
        if w.returncode == 0:
            wi = _parse_kv(w.stdout)
            if wi.get("cookies"):
                cookie = wi["cookies"].strip()
            ua = (wi.get("User-Agent") or wi.get("userAgent") or "").strip()
        return {"baseUrl": base.rstrip("/"), "eteamsId": et, "cookieHeader": cookie,
                "userAgent": ua, "source": "e10-login"}
    except Exception:
        return None


def _runtime_from_env() -> Optional[Dict[str, str]]:
    base = os.environ.get("E10_BASE_URL", "").strip()
    cookie = os.environ.get("E10_COOKIE", "").strip()
    et = os.environ.get("ETEAMSID", "").strip()
    if base and (cookie or et):
        if not cookie:
            cookie = f"ETEAMSID={et}; langType=zh_CN"
        return {"baseUrl": base.rstrip("/"), "eteamsId": et, "cookieHeader": cookie,
                "userAgent": "", "source": "env"}
    return None


def _runtime_from_workbuddy() -> Optional[Dict[str, str]]:
    """开发/探针回退：WorkBuddy 抓取的 sysadmin 会话文件（非生产路径）。"""
    sess_dir = os.environ.get(
        "E10_SESSION_DIR",
        r"C:\Users\zhang\.workbuddy\binaries\node\workspace",
    )
    d = Path(sess_dir)
    cj = d / "sysadmin_cookies.json"
    ef = d / "sysadmin_eteamsid.txt"
    if not cj.exists() or not ef.exists():
        return None
    try:
        raw = json.loads(cj.read_text(encoding="utf-8"))
        cookie = "; ".join(f"{c['name']}={c['value']}" for c in raw)
        et = ef.read_text(encoding="utf-8").strip()
        return {"baseUrl": DEFAULT_BASE_URL, "eteamsId": et, "cookieHeader": cookie,
                "userAgent": "", "source": "workbuddy-dev-session"}
    except Exception:
        return None


def resolve_runtime() -> Dict[str, str]:
    for provider in (_runtime_from_env, _runtime_from_e10_login, _runtime_from_workbuddy):
        rt = provider()
        if rt:
            return rt
    raise CliError(
        "NEEDS_LOGIN",
        "未找到 E10 登录态。生产环境请先使用 weaver-e10-login skill 登录（e10-login CLI）；"
        "或设置环境变量 E10_BASE_URL + E10_COOKIE（或 ETEAMSID）。",
    )


# ---------------------------------------------------------------- HTTP 客户端
class Client:
    def __init__(self, rt: Dict[str, str]):
        self.base = rt["baseUrl"].rstrip("/")
        self.s = requests.Session()
        self.s.verify = False
        self.s.trust_env = False
        headers = {
            "Cookie": rt["cookieHeader"],
            "eteamsid": rt.get("eteamsId", ""),
            "User-Agent": rt.get("userAgent") or "AgentType=pc,IsAgent=true",
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json, text/plain, */*",
        }
        self.s.headers.update({k: v for k, v in headers.items() if v})
        self.auth_source = rt["source"]

    def post(self, path: str, body: Any = None, params: Optional[dict] = None,
             timeout: int = 40) -> Dict[str, Any]:
        r = self.s.post(self.base + path, json=body if body is not None else {},
                        params=params, timeout=timeout)
        return self._parse(r, path)

    def get(self, path: str, params: Optional[dict] = None, timeout: int = 40) -> Dict[str, Any]:
        r = self.s.get(self.base + path, params=params, timeout=timeout)
        return self._parse(r, path)

    @staticmethod
    def _parse(r: requests.Response, path: str) -> Dict[str, Any]:
        if r.status_code in (401, 403) or "login" in r.url.lower().split("?")[0].rsplit("/", 1)[-1]:
            raise CliError("SESSION_EXPIRED", f"登录态已失效（{path}），请重新登录后再试。")
        try:
            j = r.json()
        except Exception:
            raise CliError("REMOTE_NON_JSON",
                           f"{path} 返回非 JSON（HTTP {r.status_code}）：{r.text[:200]}")
        if isinstance(j, dict) and j.get("status") is False:
            msg = str(j.get("msg") or j.get("message") or "接口返回失败")
            if "登录" in msg or "login" in msg.lower():
                raise CliError("SESSION_EXPIRED", f"登录态已失效：{msg}")
            raise CliError("REMOTE_REJECTED", f"{path} 被服务端拒绝：{msg}",
                           {"path": path, "code": j.get("code"), "raw": j})
        return j

    def data(self, j: Dict[str, Any], what: str) -> Any:
        if not isinstance(j, dict) or j.get("status") is not True:
            raise CliError("REMOTE_FORMAT_ERROR", f"{what}：接口响应缺少 status=true")
        return j.get("data")


# ---------------------------------------------------------------- context
def ctx_path(ctx_id: str) -> Path:
    if not re.fullmatch(r"[A-Za-z0-9_-]{6,64}", ctx_id):
        raise CliError("BAD_CONTEXT", f"非法 context id：{ctx_id}")
    p = CONTEXT_DIR / f"{ctx_id}.json"
    if not p.exists():
        raise CliError("CONTEXT_NOT_FOUND",
                       f"context 不存在：{ctx_id}。请先运行 form 命令生成。")
    return p


def load_ctx(ctx_id: str) -> Dict[str, Any]:
    return json.loads(ctx_path(ctx_id).read_text(encoding="utf-8"))


def save_ctx(ctx: Dict[str, Any]) -> None:
    CONTEXT_DIR.mkdir(parents=True, exist_ok=True)
    (CONTEXT_DIR / f"{ctx['ctx']}.json").write_text(
        json.dumps(ctx, ensure_ascii=False, indent=1, default=str), encoding="utf-8")


# ---------------------------------------------------------------- 会议接口封装
def load_base_create(cli: Client, wf_id: str) -> Dict[str, Any]:
    j = cli.post("/api/workflow/core/flowPage/loadBaseParam",
                 {"workflowId": wf_id, "isCreate": 1, "isMobile": 0},
                 params={"workflowId": wf_id, "isCreate": 1})
    d = cli.data(j, "loadBaseParam")
    cp = d.get("commonParam") or {}
    if not cp.get("authStr") or not cp.get("requestId"):
        raise CliError("REMOTE_FORMAT_ERROR", "loadBaseParam 未返回 authStr/requestId")
    return cp


def load_base_view(cli: Client, wf_id: str, req_id: str) -> Dict[str, Any]:
    body = {"workflowId": wf_id, "requestId": req_id, "isCreate": 0, "isMobile": 0}
    j = cli.post("/api/workflow/core/flowPage/loadBaseParam", body,
                 params={"workflowId": wf_id, "requestId": req_id})
    d = cli.data(j, "loadBaseParam(view)")
    cp = d.get("commonParam") or {}
    if not cp.get("authStr"):
        raise CliError("REMOTE_FORMAT_ERROR", "loadBaseParam(view) 未返回 authStr")
    return cp


def get_detail_add(cli: Client, wf_id: str, node: str, cp: Dict[str, Any]) -> Dict[str, Any]:
    rid, auth, sig = cp["requestId"], cp["authStr"], cp["authSignatureStr"]
    custom = {"requestId": rid, "nodeId": node, "workflowId": wf_id}
    params = {"operateType": "ADD", "meetingId": "", "meetingDate": "", "beginDate": "",
              "endDate": "", "beginTime": "", "endTime": "", "address": "", "name": "",
              "secAuthCode": "", "fromWorkflow": "true", "repeat": "false",
              "requestId": rid, "nodeId": node, "workflowId": wf_id,
              "customParams": json.dumps(custom, ensure_ascii=False),
              "authStr": auth, "authSignatureStr": sig, "isReadOnly": "false"}
    j = cli.get("/api/meeting/detail/getMeetingDetailField", params=params)
    return cli.data(j, "getMeetingDetailField")


def get_detail_edit(cli: Client, wf_id: str, req_id: str, meeting_id: str,
                    cp: Dict[str, Any]) -> Dict[str, Any]:
    """view 态回读：operateType=UPDATE + view 态 authStr。"""
    node = cp.get("userCurrentNodeId") or cp.get("fixedNodeId") or ""
    custom = {"requestId": req_id, "nodeId": node, "workflowId": wf_id}
    params = {"operateType": "UPDATE", "meetingId": meeting_id, "meetingDate": "",
              "beginDate": "", "endDate": "", "beginTime": "", "endTime": "",
              "address": "", "name": "", "secAuthCode": "", "fromWorkflow": "true",
              "repeat": "false", "requestId": req_id, "nodeId": node, "workflowId": wf_id,
              "customParams": json.dumps(custom, ensure_ascii=False),
              "authStr": cp["authStr"], "authSignatureStr": cp["authSignatureStr"],
              "isReadOnly": "false"}
    j = cli.get("/api/meeting/detail/getMeetingDetailField", params=params)
    return cli.data(j, "getMeetingDetailField(UPDATE)")


# ---------------------------------------------------------------- 命令实现
def cmd_session(args: argparse.Namespace) -> None:
    rt = resolve_runtime()
    cli = Client(rt)
    j = cli.get("/api/meeting/detail/getCreateBaseData", params={"isMobile": "false"})
    cli.data(j, "getCreateBaseData")
    emit({"ok": True, "status": "READY", "baseUrl": rt["baseUrl"],
          "authSource": rt["source"]})


def cmd_workflows(args: argparse.Namespace) -> None:
    rt = resolve_runtime()
    cli = Client(rt)
    j = cli.post("/api/workflow/list/newflow/getNewFlowListData",
                 {"wfpBelongTypeCode": "1", "loadOfsFlow": "0", "clientCtrl": 1},
                 params={"sf_request_type": "ajax"})
    data = cli.data(j, "可发起工作流列表")
    if not isinstance(data, dict):
        raise CliError("REMOTE_FORMAT_ERROR", "工作流列表 data 格式错误")
    groups = data.get("listDataGroup") if isinstance(data.get("listDataGroup"), list) else []
    type_names = {str(g.get("id")): str(g.get("typename", "")) for g in groups if isinstance(g, dict)}
    items = data.get("listData") if isinstance(data.get("listData"), list) else []
    want_id = (args.workflow_id or DEFAULT_WORKFLOW_ID).strip()
    want_name = (args.name or DEFAULT_WORKFLOW_NAME).strip()
    matches = []
    seen = set()
    for it in items:
        if not isinstance(it, dict):
            continue
        wid = str(it.get("workflowid") or it.get("id") or "").strip()
        nm = str(it.get("workflowname") or it.get("workflowName") or "").strip()
        if not wid or not nm or wid in seen:
            continue
        if wid == want_id or (not args.workflow_id and want_name and want_name in nm):
            seen.add(wid)
            matches.append({"id": wid, "workflowname": nm,
                            "workflowdesc": str(it.get("workflowdesc") or ""),
                            "typename": type_names.get(str(it.get("type") or ""), "")})
    if not matches:
        emit({"ok": True, "status": "NOT_FOUND", "workflowId": want_id,
              "message": "当前用户可发起列表中没有「会议申请」，可能已停用或无发起权限。"})
        return
    emit({"ok": True, "status": "SELECTED", "workflows": matches,
          "message": f"可发起：{matches[0]['workflowname']}（{matches[0]['id']}）"})


def _summarize_field(key: str, node: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    if not isinstance(node, dict) or "itemType" not in node:
        return None
    if not node.get("visible", False):
        return None
    options = None
    if isinstance(node.get("options"), list) and node["options"]:
        options = [{"id": str(o.get("id", "")), "content": o.get("content", "")}
                   for o in node["options"] if isinstance(o, dict)]
    return {
        "key": key, "label": KEY_LABELS.get(key, key),
        "itemType": node.get("itemType"), "required": bool(node.get("required")),
        "readOnly": bool(node.get("readOnly") or node.get("disable")),
        "multiple": bool(node.get("multiple")), "options": options,
    }


def cmd_form(args: argparse.Namespace) -> None:
    rt = resolve_runtime()
    cli = Client(rt)
    wf_id = (args.workflow_id or DEFAULT_WORKFLOW_ID).strip()

    # 1. 创建态 loadBaseParam（等同浏览器打开发起页，会拿到一个临时 requestId，不保存即不落库）
    cp = load_base_create(cli, wf_id)
    node = str(cp.get("userCurrentNodeId") or cp.get("fixedNodeId") or "")
    # 2. 布局多页 ID + 会议业务字段
    lm = cli.post("/api/meeting/workflowNodeLayout/getMeetingFormLayoutMultiple",
                  {"mtNodeId": node, "workflowId": wf_id, "terminalType": "PC"})
    layout_multi = str(cli.data(lm, "getMeetingFormLayoutMultiple") or "").strip()
    detail = get_detail_add(cli, wf_id, node, cp)

    # 会议自定义表单：从布局组件里取每个 BaseField 的 fieldId↔dataKey↔标题↔必填↔可见
    form_id = str((detail.get("createBaseData") or {}).get("EBFormId") or "").strip()
    layout_id = str(((detail.get("meetingFields") or {}).get("data") or {}).get("layoutId")
                    or "").strip()
    custom_fields: List[Dict[str, Any]] = []
    try:
        fl = cli.post("/api/meeting/form/core/getFormLayout",
                      {"formId": form_id, "layoutId": layout_id,
                       "module": "meeting", "client": "pc"},
                      params={"formId": form_id})
        fl_data = cli.data(fl, "getFormLayout") or {}
        seen = set()
        for page in ((fl_data.get("formLayout") or {}).get("pageLayouts") or []):
            for comp in page.get("comps") or []:
                if comp.get("type") != "BaseField":
                    continue
                c = comp.get("config") or {}
                fid = str(c.get("fieldId") or "").strip()
                if not fid or fid in seen:
                    continue
                seen.add(fid)
                custom_fields.append({
                    "fieldId": fid,
                    "dataKey": str(c.get("dataKey") or c.get("columnName") or ""),
                    "label": str(c.get("title") or ""),
                    "columnType": str(c.get("columnType") or c.get("valueType") or ""),
                    "required": bool(c.get("required")),
                    "readOnly": bool(c.get("readOnly")),
                    "visible": bool(c.get("display", True)),
                })
    except CliError:
        pass  # 自定义表单布局是增强信息，拿不到不影响写入链
    for key, fid in CUSTOM_TEXT_FIELDS.items():
        if not any(f["fieldId"] == fid for f in custom_fields):
            custom_fields.append({"fieldId": fid, "dataKey": key,
                                  "label": "会议物资", "columnType": "TEXTAREA",
                                  "required": False, "readOnly": False, "visible": True})
    mf = detail.get("meetingFields") or {}
    items = mf.get("items") or {}

    all_fields = [f for k, n in items.items()
                  if (f := _summarize_field(k, n)) is not None]
    # 对外只暴露可填写业务字段（剔除 DESCRIPTION/标签等内部项与只读项）；
    # frequent 虽实时必填，但脚本固定发"永不"自动满足，从用户必填列表中剔除。
    fields = [f for f in all_fields
              if f["itemType"] != "DESCRIPTION" and not f["readOnly"]]
    user_required = [f["key"] for f in fields
                     if f["required"] and f["key"] not in ("frequent",)]

    cu = cp.get("currentUser") if isinstance(cp.get("currentUser"), dict) else {}
    hrm_id = str(cp.get("identityId") or cu.get("id") or cu.get("hrmId") or "").strip()
    user_name = str(cu.get("name") or cu.get("userName") or cu.get("lastname") or "").strip()
    raw_title = str(cp.get("flowPageTitleText") or cp.get("flowPageTitle") or "")
    plain_title = re.sub(r"<[^>]+>", "", raw_title).strip()
    wf_name = (re.split(r"\s*-\s*", plain_title)[0] if plain_title else "") \
        or DEFAULT_WORKFLOW_NAME

    ctx = {
        "ctx": "mf_" + uuid.uuid4().hex[:10],
        "createdAt": datetime.now().isoformat(timespec="seconds"),
        "baseUrl": rt["baseUrl"], "authSource": rt["source"],
        "workflow": {"id": wf_id, "name": wf_name},
        "nodeId": node,
        "currentUser": {"hrmId": hrm_id, "name": user_name},
        "form": {"id": form_id, "layoutId": layout_id,
                 "layoutMultiId": layout_multi,
                 "customTextFields": dict(CUSTOM_TEXT_FIELDS)},
        "fields": fields, "requiredKeys": user_required,
        "customFields": custom_fields,
        "tempRequestId": cp.get("requestId"),
        "prepared": None, "result": None,
    }
    save_ctx(ctx)
    emit({"ok": True, "status": "FORM_READY", "ctx": ctx["ctx"],
          "workflow": ctx["workflow"], "currentUser": ctx["currentUser"],
          "form": {"id": form_id, "layoutId": layout_id, "layoutMultiId": layout_multi},
          "requiredKeys": user_required,
          "fields": fields,
          "customFields": custom_fields, "customFieldCount": len(custom_fields),
          "nextStep": "调用 rooms/people/depts 解析名称后，用 prepare 生成预览。",
          "contextFile": str(ctx_path(ctx["ctx"]))})


def _all_rooms(cli: Client, date_str: str) -> List[Dict[str, str]]:
    j = cli.post("/api/meeting/roomUsage/getAllRoomUrl",
                 {"currentdate": date_str, "bywhat": 4, "type": "day", "mode": "my,other"})
    data = cli.data(j, "会议室列表")
    if not isinstance(data, list):
        return []
    return [{"id": str(r.get("id", "")), "name": str(r.get("name", ""))}
            for r in data if isinstance(r, dict) and r.get("id")]


def cmd_rooms(args: argparse.Namespace) -> None:
    rt = resolve_runtime()
    cli = Client(rt)
    date_str = (args.begin or datetime.now().strftime("%Y-%m-%d"))[:10]
    rooms = _all_rooms(cli, date_str)
    if args.name:
        kw = args.name.strip()
        exact = [r for r in rooms if r["name"] == kw]
        if exact:
            matched, ambiguous = exact, []
        else:
            fuzzy = [r for r in rooms if kw in r["name"] or r["name"] in kw]
            matched, ambiguous = ([fuzzy[0]], fuzzy[1:]) if len(fuzzy) == 1 else ([], fuzzy)
        if not matched:
            emit({"ok": True, "status": "NOT_FOUND", "query": kw,
                  "candidates": ambiguous or rooms,
                  "message": "系统里没有唯一匹配该名称的会议室，候选见 candidates。"})
            return
        out = {"ok": True, "status": "MATCHED", "room": matched[0]}
        if ambiguous:
            out["otherCandidates"] = ambiguous
        emit(out)
        return
    emit({"ok": True, "status": "READY", "date": date_str, "rooms": rooms})


def _complete(cli: Client, kind: str, keyword: str,
              begin: str = "", end: str = "") -> List[Dict[str, Any]]:
    body: Dict[str, Any] = {"browserMultiple": False, "newly": 0, "searchValue": keyword}
    if kind == "mt_room":
        body.update({"typeId": "-1", "beginDate": begin, "endDate": end, "totalMember": "0"})
    elif kind == "resource":
        body.update({"showPartTime": True})
    j = cli.post(f"/api/meeting/common/browser/complete/{kind}", body)
    data = cli.data(j, f"联想查询 {kind}")
    if isinstance(data, dict):
        rows = data.get("data") if isinstance(data.get("data"), list) else []
    elif isinstance(data, list):
        rows = data
    else:
        rows = []
    return rows if isinstance(rows, list) else []


def cmd_people(args: argparse.Namespace) -> None:
    rt = resolve_runtime()
    cli = Client(rt)
    out_people = []
    missing = []
    for raw in [x.strip() for x in args.names.split(",") if x.strip()]:
        if re.fullmatch(r"\d{15,}", raw):
            out_people.append({"query": raw, "id": raw, "name": "", "resolved": True})
            continue
        rows = _complete(cli, "resource", raw)
        exact = [r for r in rows if str(r.get("name") or r.get("content") or "") == raw]
        pool = exact or rows
        uniq: Dict[str, Dict[str, Any]] = {}
        for r in pool:
            rid = str(r.get("id") or r.get("mainId") or "").strip()
            if rid and rid not in uniq:
                uniq[rid] = {"id": rid, "name": str(r.get("name") or r.get("content") or ""),
                             "department": str(r.get("department") or "")}
        if len(uniq) == 1:
            p = next(iter(uniq.values()))
            out_people.append({"query": raw, "resolved": True, **p})
        else:
            missing.append({"query": raw,
                            "candidates": list(uniq.values()) if uniq else []})
    emit({"ok": True, "status": "READY" if not missing else "NEEDS_INPUT",
          "people": out_people, "missing": missing})


def cmd_depts(args: argparse.Namespace) -> None:
    rt = resolve_runtime()
    cli = Client(rt)
    out_depts, missing = [], []
    for raw in [x.strip() for x in args.names.split(",") if x.strip()]:
        if re.fullmatch(r"\d{15,}", raw):
            out_depts.append({"query": raw, "id": raw, "name": "", "resolved": True})
            continue
        rows = _complete(cli, "department", raw)
        exact = [r for r in rows if str(r.get("name") or r.get("content") or "") == raw]
        pool = exact or rows
        uniq: Dict[str, Dict[str, str]] = {}
        for r in pool:
            rid = str(r.get("id") or "").strip()
            if rid and rid not in uniq:
                uniq[rid] = {"id": rid, "name": str(r.get("name") or r.get("content") or "")}
        if len(uniq) == 1:
            d = next(iter(uniq.values()))
            out_depts.append({"query": raw, "resolved": True, **d})
        else:
            missing.append({"query": raw,
                            "candidates": list(uniq.values()) if uniq else []})
    emit({"ok": True, "status": "READY" if not missing else "NEEDS_INPUT",
          "departments": out_depts, "missing": missing})


# ---------------------------------------------------------------- 冲突预检
def _chk_body(d: Dict[str, Any]) -> Dict[str, Any]:
    return {"hrmids": d.get("hrmIds", ""), "crmids": "",
            "beginDatetime": d["beginDatetime"], "endDatetime": d["endDatetime"],
            "mtId": "", "contacter": "", "caller": d["caller"],
            "address": d["roomId"], "serviceItems": "",
            "totalmember": str(d.get("totalMember", 0)), "name": d["name"],
            "frequent": "0", "module": "", "isMobile": False}


def run_conflict_checks(cli: Client, d: Dict[str, Any]) -> Dict[str, Any]:
    """返回 {blocked, blocks:[...], warnings:[...], raw:{kind:data}}。接口异常一律视为阻断。"""
    blocks, warnings, raw = [], [], {}
    for kind, blocking in [("meetingChkRoom", True), ("meetingChkMember", False),
                           ("meetingChkRoomAttribute", True), ("meetingChkService", True)]:
        try:
            j = cli.post(f"/api/meeting/detail/{kind}", _chk_body(d))
            data = cli.data(j, kind) or {}
        except CliError as e:
            blocks.append({"kind": kind, "reason": e.message})
            continue
        raw[kind] = data
        if data.get("cansub") is False:
            msg = data.get("conflictMsg") or data.get("conflictMsgInfos") \
                or data.get("msg") or data
            item = {"kind": kind, "conflictMsg": msg}
            (blocks if blocking else warnings).append(item)
    return {"blocked": bool(blocks), "blocks": blocks, "warnings": warnings, "raw": raw}


def cmd_conflict(args: argparse.Namespace) -> None:
    ctx = load_ctx(args.context)
    data = json.loads(args.data) if args.data.startswith("{") else \
        json.loads(Path(args.data).read_text(encoding="utf-8"))
    data.setdefault("name", "冲突预检")
    data.setdefault("caller", ctx["currentUser"]["hrmId"])
    _validate_times(data)
    if not data.get("roomId"):
        raise CliError("BAD_INPUT", "conflict 需要 roomId（先用 rooms 命令解析）。")
    cli = Client(resolve_runtime())
    res = run_conflict_checks(cli, data)
    emit({"ok": True, "status": "BLOCKED" if res["blocked"] else "OK", **{
        k: v for k, v in res.items() if k != "raw"}, "details": res["raw"]})


def _validate_times(data: Dict[str, Any]) -> None:
    for k in ("beginDatetime", "endDatetime"):
        v = str(data.get(k) or "").strip()
        if not DT_RE.match(v):
            raise CliError("BAD_INPUT", f"{k} 必须是 yyyy-MM-dd HH:mm 格式，收到：{v!r}")
        try:
            datetime.strptime(v, "%Y-%m-%d %H:%M")
        except ValueError:
            raise CliError("BAD_INPUT", f"{k} 不是合法时间：{v!r}")
    if data["endDatetime"] <= data["beginDatetime"]:
        raise CliError("BAD_INPUT",
                       f"结束时间（{data['endDatetime']}）必须晚于开始时间（{data['beginDatetime']}）。")


# ---------------------------------------------------------------- prepare
def _resolve_room(cli: Client, ctx: Dict[str, Any], data: Dict[str, Any],
                  errors: List[str]) -> str:
    room = str(data.get("roomId") or data.get("room") or data.get("address") or "").strip()
    if not room:
        return ""
    if re.fullmatch(r"\d{15,}", room):
        return room
    rooms = _all_rooms(cli, str(data.get("beginDatetime") or
                                 datetime.now().strftime("%Y-%m-%d"))[:10])
    exact = [r for r in rooms if r["name"] == room]
    fuzzy = [r for r in rooms if room in r["name"]]
    if len(exact) == 1:
        return exact[0]["id"]
    if len(fuzzy) == 1:
        return fuzzy[0]["id"]
    errors.append(f"会议室 {room!r} 无法唯一匹配，候选："
                  + "、".join(r["name"] for r in (fuzzy or rooms)))
    return ""


def _resolve_people(cli: Client, key: str, kind: str, data: Dict[str, Any],
                    errors: List[str]) -> Tuple[List[str], List[Dict[str, str]]]:
    vals = data.get(key) or []
    if isinstance(vals, str):
        vals = [v.strip() for v in vals.split(",") if v.strip()]
    ids, resolved = [], []
    for v in vals:
        v = str(v).strip()
        if re.fullmatch(r"\d{15,}", v):
            ids.append(v)
            resolved.append({"id": v, "name": ""})
            continue
        rows = _complete(cli, kind, v)
        exact = [r for r in rows if str(r.get("name") or r.get("content") or "") == v]
        uniq: Dict[str, Dict[str, str]] = {}
        for r in (exact or rows):
            rid = str(r.get("id") or r.get("mainId") or "").strip()
            if rid and rid not in uniq:
                uniq[rid] = {"id": rid, "name": str(r.get("name") or r.get("content") or "")}
        if len(uniq) == 1:
            p = next(iter(uniq.values()))
            ids.append(p["id"])
            resolved.append(p)
        else:
            errors.append(f"参会{'人员' if kind == 'resource' else '部门'} {v!r} 无法唯一匹配"
                          + ("，候选：" + "、".join(p["name"] for p in uniq.values()) if uniq
                             else "（系统中未找到）"))
    return ids, resolved


def _remind_value(data: Dict[str, Any], ctx: Dict[str, Any]) -> str:
    r = data.get("remind")
    if not r:
        return ""
    opts = next((f.get("options") for f in ctx["fields"] if f["key"] == "remindType"), None) or []
    if isinstance(r, list) and r:
        picked = []
        for x in r:
            x = str(x)
            if re.fullmatch(r"\d+", x):
                picked.append(x)
            else:
                hit = next((o["id"] for o in opts if x in (o["content"], o["id"])), "")
                if hit:
                    picked.append(hit)
        return ",".join(picked)
    return opts[0]["id"] if opts else "6"


def cmd_prepare(args: argparse.Namespace) -> None:
    ctx = load_ctx(args.context)
    raw = args.data
    data = json.loads(raw) if raw.startswith("{") else json.loads(Path(raw).read_text(encoding="utf-8"))
    intent = args.intent or "draft"
    if intent not in ("draft", "submit"):
        raise CliError("BAD_INPUT", "intent 只能是 draft 或 submit")
    errors: List[str] = []          # 硬性错误：格式非法、名称无法解析
    missing: List[str] = []         # 缺必填：draft 允许（AC-8），submit 不允许
    warnings: List[str] = []

    # 名称（草稿允许空，空草稿服务端实测可存）
    name = str(data.get("name") or "").strip()
    if not name:
        missing.append("会议名称 name")

    # 时间：给了就必须成对且合法；完全不给草稿允许、提交拒绝；只给一个一律错误
    begin = str(data.get("beginDatetime") or "").strip()
    end = str(data.get("endDatetime") or "").strip()
    if begin or end:
        for label, v in (("开始时间 beginDatetime", begin), ("结束时间 endDatetime", end)):
            if v and not DT_RE.match(v):
                errors.append(f"{label} 必须是 yyyy-MM-dd HH:mm 格式（含小时分钟），收到：{v!r}")
            elif v:
                try:
                    datetime.strptime(v, "%Y-%m-%d %H:%M")
                except ValueError:
                    errors.append(f"{label} 不是合法时间：{v!r}")
        if not begin or not end:
            errors.append("开始/结束时间必须成对提供，不能只给一个。")
        elif DT_RE.match(begin) and DT_RE.match(end) and end <= begin:
            errors.append(f"结束时间（{end}）必须晚于开始时间（{begin}）。")
    else:
        missing.append("开始时间 beginDatetime")
        missing.append("结束时间 endDatetime")

    cli = Client(resolve_runtime())
    # 会议室：给了就解析（解析不了是硬错误）；没给草稿允许、提交拒绝
    room_raw = str(data.get("roomId") or data.get("room") or data.get("address") or "").strip()
    room_id = _resolve_room(cli, ctx, data, errors) if room_raw else ""
    if not room_id and not any("会议室" in e for e in errors):
        missing.append("会议地点 room（名称或会议室 id）")

    member_ids, member_objs = _resolve_people(cli, "members", "resource", data, errors)
    dept_ids, dept_objs = _resolve_people(cli, "departments", "department", data, errors)

    caller = str(data.get("caller") or ctx["currentUser"]["hrmId"]).strip()
    total = data.get("totalMember")
    if total in (None, ""):
        total = 1 + len(member_ids) + len(dept_ids)
    try:
        total = int(total)
    except (TypeError, ValueError):
        errors.append(f"应到人数 totalMember 必须是整数，收到：{total!r}")
        total = 0

    remind = _remind_value(data, ctx)
    mt_desc = str(data.get("mtDesc") or data.get("subject") or "").strip()
    other = str(data.get("otherMembers") or "").strip()
    materials = str(data.get("materials") or "").strip()

    if intent == "submit" and missing:
        errors.extend(f"缺少必填：{m}（提交前必须补全）" for m in missing)
        missing = []
    if errors:
        emit({"ok": True, "status": "NEEDS_INPUT", "ctx": ctx["ctx"], "intent": intent,
              "errors": errors,
              "missing": missing,
              "message": "请补齐/修正后重新 prepare（所有问题已一次列全）。"})
        return

    # 冲突预检仅在时段+会议室齐全时运行；缺时段的草稿跳过（create 时同样跳过）
    blocks, chk_warnings, conflict_checked = [], [], False
    if begin and end and room_id:
        chk = run_conflict_checks(cli, {
            "name": name or "（未命名会议）", "caller": caller,
            "beginDatetime": begin, "endDatetime": end,
            "roomId": room_id, "hrmIds": ",".join(member_ids),
            "totalMember": total})
        blocks, chk_warnings = chk["blocks"], chk["warnings"]
        conflict_checked = True
        if blocks:
            emit({"ok": True, "status": "BLOCKED", "ctx": ctx["ctx"],
                  "blocks": blocks,
                  "message": "冲突预检未通过，已终止；本 skill 不提供绕过选项。"
                             "请更换会议室或时间段后重新 prepare。"})
            return
    warnings.extend(f"参会人时间冲突：{json.dumps(w.get('conflictMsg'), ensure_ascii=False)}"
                    for w in chk_warnings)
    if missing:
        warnings.append("草稿缺少必填项，保存后需在 OA 中补全才能提交：" + "、".join(missing))

    prepared = {
        "intent": intent,
        "name": name, "beginDatetime": begin, "endDatetime": end,
        "caller": caller, "roomId": room_id,
        "members": member_ids, "memberLabels": member_objs,
        "departments": dept_ids, "departmentLabels": dept_objs,
        "otherMembers": other, "mtDesc": mt_desc, "materials": materials,
        "totalMember": total, "remindType": remind,
        "missingRequirements": missing, "conflictChecked": conflict_checked,
        "conflict": {"blocks": blocks, "warnings": chk_warnings},
        "preparedAt": datetime.now().isoformat(timespec="seconds"),
    }
    ctx["prepared"] = prepared
    ctx["result"] = None
    save_ctx(ctx)

    room_name = ""
    if room_id:
        rooms = _all_rooms(cli, begin[:10] or datetime.now().strftime("%Y-%m-%d"))
        room_name = next((r["name"] for r in rooms if r["id"] == room_id), room_id)
    preview = [
        f"会议名称：{name or '（草稿暂不填）'}",
        f"时间：{(begin + ' ~ ' + end) if begin else '（草稿暂不填）'}",
        f"会议室：{room_name or '（草稿暂不填）'}" + (f"（{room_id}）" if room_id and room_name != room_id else ""),
        f"发起人：{ctx['currentUser']['name'] or caller}",
        f"参会人员：{'、'.join(p['name'] or p['id'] for p in member_objs) or '（无）'}",
        f"参会部门：{'、'.join(p['name'] or p['id'] for p in dept_objs) or '（无）'}",
        f"其他人员：{other or '（无）'}",
        f"会议内容：{mt_desc or '（无）'}",
        f"会议物资：{materials or '（无）'}",
        f"应到人数：{total}",
        f"提醒方式：{('系统消息提醒（' + remind + '）') if remind else '（不提醒）'}",
    ]
    if missing:
        preview.append("待补必填：" + "、".join(missing) + "（草稿可先存，提交前必须补全）")
    preview.append(f"动作：{'保存草稿（不进入审批）' if intent == 'draft' else '提交（进入审批流）'}")
    emit({"ok": True, "status": "READY", "ctx": ctx["ctx"], "intent": intent,
          "missing": missing, "preview": preview, "warnings": warnings,
          "nextStep": "向用户展示 preview，取得明确确认后执行 create --confirm"
                      + (" --submit" if intent == "submit" else "")})


# ---------------------------------------------------------------- create
def _build_operate_payload(ctx: Dict[str, Any], p: Dict[str, Any], cp: Dict[str, Any],
                           form_data_id: str) -> Dict[str, Any]:
    wf_id, node = ctx["workflow"]["id"], ctx["nodeId"]
    rid, auth, sig = cp["requestId"], cp["authStr"], cp["authSignatureStr"]
    custom = {"requestId": rid, "nodeId": node, "workflowId": wf_id}
    body = dict(OPERATE_DEFAULTS)
    body.update({
        "name": p["name"], "caller": p["caller"],
        "beginDatetime": p["beginDatetime"], "endDatetime": p["endDatetime"],
        "address": p["roomId"], "mtType": "",
        "hrmMembers": ",".join(p["members"]), "orgMembers": ",".join(p["departments"]),
        "otherMembers": p["otherMembers"], "mtDesc": p["mtDesc"],
        "totalMember": p["totalMember"],
        "remindType": p["remindType"],
        "until": (p["beginDatetime"] or datetime.now().strftime("%Y-%m-%d %H:%M"))[:10],
        "formDataId": form_data_id,
        "layoutId": ctx["form"]["layoutId"], "layoutMultiId": ctx["form"]["layoutMultiId"],
        "requestId": rid, "nodeId": node, "workflowId": wf_id,
        "authStr": auth, "authSignatureStr": sig,
        "customParams": custom,  # 必须是对象，不能是 JSON 字符串
        "fromWorkflowParams": {**custom, "customParams": dict(custom),
                               "authStr": auth, "authSignatureStr": sig, "isReadOnly": False},
    })
    return body


def _build_flow_create(ctx: Dict[str, Any], cp: Dict[str, Any], meeting_id: str,
                       src: str) -> Dict[str, Any]:
    node = ctx["nodeId"]
    body = dict(FLOW_CREATE_DEFAULTS)
    body.update({
        "workflowId": ctx["workflow"]["id"], "identityId": cp.get("identityId") or p_caller(ctx),
        "requestId": cp["requestId"], "userCurrentNodeId": node, "fixedNodeId": node,
        "dataId": meeting_id, "authStr": cp["authStr"],
        "authSignatureStr": cp["authSignatureStr"],
        "pageKey": f"create_{ctx['workflow']['id']}_{int(time.time() * 1000)}",
        "src": src,
    })
    return body


def p_caller(ctx: Dict[str, Any]) -> str:
    return str(ctx["currentUser"]["hrmId"])


def cmd_create(args: argparse.Namespace) -> None:
    ctx = load_ctx(args.context)
    p = ctx.get("prepared")
    if not p:
        raise CliError("NOT_PREPARED", "尚未 prepare，或 context 已被重置。")
    submit = bool(args.submit)
    if submit and p.get("intent") != "submit":
        raise CliError("INTENT_MISMATCH",
                       "prepare 时意图为 draft；要提交审批请重新 prepare --intent submit。")
    if not args.confirm:
        raise CliError("CONFIRM_REQUIRED",
                       "create 必须带 --confirm；请先向用户展示 prepare 的 preview 并取得明确确认。")

    cli = Client(resolve_runtime())
    wf_id = ctx["workflow"]["id"]

    # 写入开始后任何异常都不得重试：返回 UNCERTAIN 让调用方走 detail/列表回查。
    try:
        # 1. 全新 loadBaseParam（每次创建态调用都会拿到新的临时 requestId，与 form 阶段的无关）
        cp = load_base_create(cli, wf_id)
        node = str(cp.get("userCurrentNodeId") or ctx["nodeId"])
        # 2. 落任何数据前先做冲突预检（仅时段+会议室齐全；缺必填草稿无此步。chk 不依赖 formDataId）
        if p.get("conflictChecked") and p["beginDatetime"] and p["endDatetime"] and p["roomId"]:
            chk = run_conflict_checks(cli, {
                "name": p["name"] or "（未命名会议）", "caller": p["caller"],
                "beginDatetime": p["beginDatetime"], "endDatetime": p["endDatetime"],
                "roomId": p["roomId"], "hrmIds": ",".join(p["members"]),
                "totalMember": p["totalMember"]})
            if chk["blocked"]:
                emit({"ok": True, "status": "BLOCKED", "blocks": chk["blocks"],
                      "message": "创建前冲突预检未通过，未写入任何数据。"})
                return

        # 3. saveFormData（会议自定义表单：仅会议物资等文本域走 dataDetails）
        details = []
        if p.get("materials"):
            fid = ctx["form"]["customTextFields"].get("materials")
            if fid:
                details.append({"formField": {"id": fid},
                                "dataText": {"content": p["materials"]}})
        sf = cli.post("/api/meeting/form/core/saveFormData", {
            "module": "meeting",
            "customParam": {"viewType": "ADD", "refResourceId": "", "workflowId": wf_id,
                            "requestId": cp["requestId"], "nodeId": node},
            "formData": {"module": "meeting", "dataDetails": details, "client": "pc",
                         "dataStatus": "submit", "form": {"id": ctx["form"]["id"]},
                         "formLayout": {"id": ctx["form"]["layoutId"]}},
        }, params={"formId": ctx["form"]["id"]})
        form_data_id = str(cli.data(sf, "saveFormData").get("id") or "").strip()
        if not form_data_id:
            raise CliError("REMOTE_FORMAT_ERROR", "saveFormData 未返回 id")

        # 4. operateMeetingByType（会议业务字段载体；customParams 必须是对象）
        op = cli.post("/api/meeting/detail/operateMeetingByType",
                      _build_operate_payload(ctx, p, cp, form_data_id))
        meeting_id = str(cli.data(op, "operateMeetingByType").get("id") or "").strip()
        if not meeting_id:
            raise CliError("REMOTE_FORMAT_ERROR", "operateMeetingByType 未返回会议 id")

        # 5. createByList
        cli.post("/api/bcw/common/relevance/createByList.common",
                 {"module": "meeting", "relevances": []})
        # 6. flow/create（响应业务字段在顶层，不在 data 下）
        fc = cli.post("/api/workflow/core/flow/create",
                      _build_flow_create(ctx, cp, meeting_id, "submit" if submit else "save"))
    except CliError:
        raise
    except Exception as e:
        emit({"ok": False, "status": "UNCERTAIN", "ctx": ctx["ctx"],
              "errorCode": "WRITE_UNCERTAIN",
              "message": f"写入过程中出现异常：{type(e).__name__}: {e}。禁止自动重试，"
                         "请用 detail/流程列表回查该时段单据后再决定。",
              "tempRequestId": locals().get("cp", {}).get("requestId")})
        return

    if not fc.get("flowIsCreateSuccess"):
        emit({"ok": False, "status": "UNCERTAIN", "ctx": ctx["ctx"], "raw": fc,
              "errorCode": "WRITE_NOT_CONFIRMED",
              "message": "flow/create 未返回 flowIsCreateSuccess=true，禁止重试，请回查。"})
        return

    req_id = str(fc.get("requestId") or cp["requestId"])
    result = {"requestId": req_id, "requestName": fc.get("requestName"),
              "isDraft": bool(fc.get("isDraft")), "meetingId": meeting_id,
              "formDataId": form_data_id, "submitted": submit,
              "viewUrl": ctx["baseUrl"] + "/sp/workflow/flowpage/view/" + req_id,
              "createUrl": ctx["baseUrl"] + "/sp/workflow/flowpage/create/" + wf_id,
              "rawResult": {"resultType": fc.get("resultType")}}
    ctx["result"] = result
    save_ctx(ctx)

    # 服务端回读关键字段（失败不影响创建结果）
    readback: Any = None
    if not (p.get("beginDatetime") and p.get("endDatetime") and p.get("roomId")):
        readback = {"skipped": "缺时间/会议室的草稿会议详情接口会报内部错误，已跳过字段回读；"
                               "可用 detail 或 OA 页面在补全后查看。"}
    else:
        try:
            vcp = load_base_view(cli, wf_id, req_id)
            vd = get_detail_edit(cli, wf_id, req_id, meeting_id, vcp)
            vals = (vd.get("meetingFields") or {}).get("items") or {}
            readback = {}
            for k in ("name", "beginDatetime", "endDatetime", "address", "hrmMembers",
                      "orgMembers", "otherMembers", "totalMember", "remindType", "mtDesc"):
                node2 = vals.get(k)
                if isinstance(node2, dict):
                    readback[k] = node2.get("value")
        except Exception as e:
            readback = {"readbackError": f"{type(e).__name__}: {e}"}

    emit({"ok": True, "status": "SUBMITTED" if submit else "DRAFT_CREATED",
          **result, "readback": readback})


# ---------------------------------------------------------------- detail
def _find_key(obj: Any, key: str) -> Any:
    if isinstance(obj, dict):
        if key in obj and obj[key] not in (None, "", 0):
            return obj[key]
        for v in obj.values():
            found = _find_key(v, key)
            if found not in (None, ""):
                return found
    elif isinstance(obj, list):
        for v in obj:
            found = _find_key(v, key)
            if found not in (None, ""):
                return found
    return None


def cmd_detail(args: argparse.Namespace) -> None:
    rt = resolve_runtime()
    cli = Client(rt)
    wf_id = (args.workflow_id or DEFAULT_WORKFLOW_ID).strip()
    rid = args.request_id.strip()
    # view 态三件套：loadBaseParam 取 view auth → loadFrameParam 取 dataId(会议id)
    # → getMeetingDetailField(UPDATE) 取字段值。
    vcp = load_base_view(cli, wf_id, rid)
    body = {"workflowId": wf_id, "requestId": rid, "isCreate": 0, "isMobile": 0}
    lf = cli.post("/api/workflow/core/flowPage/loadFrameParam", body,
                  params={"workflowId": wf_id, "requestId": rid, "isCreate": 0})
    lf_data = cli.data(lf, "loadFrameParam")
    meeting_id = str(_find_key(lf_data, "dataId") or "").strip()
    values: Dict[str, Any] = {}
    if meeting_id:
        vd = get_detail_edit(cli, wf_id, rid, meeting_id, vcp)
        for k, node in ((vd.get("meetingFields") or {}).get("items") or {}).items():
            if isinstance(node, dict) and "value" in node:
                values[k] = node.get("value")
    emit({"ok": True, "status": "FOUND" if meeting_id else "NOT_FOUND",
          "requestId": rid, "meetingId": meeting_id, "values": values,
          "viewUrl": rt["baseUrl"] + "/sp/workflow/flowpage/view/" + rid})


# ---------------------------------------------------------------- 入口
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="泛微 E10 会议申请工作流发起工具")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("session")

    w = sub.add_parser("workflows")
    w.add_argument("--workflow-id", default="")
    w.add_argument("--name", default="")

    f = sub.add_parser("form")
    f.add_argument("--workflow-id", default="")

    r = sub.add_parser("rooms")
    r.add_argument("--name", default="")
    r.add_argument("--begin", default="", help="yyyy-MM-dd（默认今天）")

    pp = sub.add_parser("people")
    pp.add_argument("--names", required=True, help="逗号分隔的姓名或 HRM id")

    dp = sub.add_parser("depts")
    dp.add_argument("--names", required=True, help="逗号分隔的部门名或部门 id")

    cf = sub.add_parser("conflict")
    cf.add_argument("context")
    cf.add_argument("--data", required=True, help="JSON 字符串或 @文件路径（文件直接给路径）")

    pr = sub.add_parser("prepare")
    pr.add_argument("context")
    pr.add_argument("--data", required=True, help="JSON 字符串或 JSON 文件路径")
    pr.add_argument("--intent", choices=["draft", "submit"], default="draft")

    cr = sub.add_parser("create")
    cr.add_argument("context")
    cr.add_argument("--confirm", action="store_true")
    cr.add_argument("--submit", action="store_true")

    dt = sub.add_parser("detail")
    dt.add_argument("--request-id", required=True)
    dt.add_argument("--workflow-id", default="")
    return p


def main() -> None:
    args = build_parser().parse_args()
    handlers = {
        "session": cmd_session, "workflows": cmd_workflows, "form": cmd_form,
        "rooms": cmd_rooms, "people": cmd_people, "depts": cmd_depts,
        "conflict": cmd_conflict, "prepare": cmd_prepare,
        "create": cmd_create, "detail": cmd_detail,
    }
    try:
        handlers[args.cmd](args)
    except CliError as e:
        fail(e.code, e.message, **e.extra)
    except (requests.RequestException, OSError) as e:
        fail("NETWORK_ERROR", f"网络错误：{type(e).__name__}: {e}")


if __name__ == "__main__":
    main()
