---
name: weaver-e10-meeting-flow
display_name: 泛微E10会议申请发起助手
description: 泛微 E10/OA「会议申请」工作流专用发起 Skill。通过会议模块接口链（而非普通 workflow 表单接口）解析会议申请单的字段能力、会议室/人员/部门名称与ID、冲突预检，并在用户明确确认后保存草稿或提交审批，支持结果回读与单据链接输出。当用户要在雄安科学园 E10 上发起/创建/提交「会议申请」、预约会议走审批、查询已发起会议申请单时使用。
version: 1.0.0
---

# 泛微 E10「会议申请」发起助手

## 这个 Skill 解决什么

雄安科学园 E10（`https://zhxz.xasp.com.cn`）的「会议申请」流程（workflowId
`1302788388361633792`）挂的是**会议应用组件**（`@weapp/meeting/MeetingDetailCom`），
不是普通 workflow layout 表单。通用 `weaver-e10-workflow` 的
`workflow-create`（form→saveFormData 普通表单链）在本流程**必然失败**
（报 `缺少必要字段：formConfig.layoutMultiId`）。本 skill 走会议模块自己的接口链，
纯 HTTP 完成发起，不依赖浏览器。

流程后续审批操作（同意/退回/转办等）与列表查询**仍复用 `weaver-e10-workflow`**，本 skill 不重复实现。

## 命令执行原则（任何命令执行前必读）

1. **只执行本文件写明的命令与参数**，不得臆造 flag/接口；不确定就停止并说明能力边界。
2. **写操作只有 `create --confirm` 一条**。执行前必须把 `prepare` 返回的 `preview`
   原样展示给用户并取得**明确确认**；`--submit`（进入审批流）必须用户明确说"提交"。
3. **冲突阻断不可绕过**：`prepare`/`create` 返回 `BLOCKED` 时停止，不提供"强制提交"选项，
   让用户换会议室/时间段后重新 prepare。
4. **写后结果不确定（超时/异常/`UNCERTAIN`）禁止重试**：用 `detail` 或流程列表回查，
   如实告知用户，不得换参数再写一次（会产生重复会议/重复单据）。
5. HTTP 失败、登录失效、业务报错：立即停止并原样转述 `message`；登录失效（`SESSION_EXPIRED`）
   时引导用户用 weaver-e10-login 重新登录后再继续。
6. 所有 ID 按字符串处理（超过 JS 安全整数），禁止转 number。

## 环境与登录态

- Python 3 + `requests`（`pip install -r scripts/requirements.txt`，目录：
  `.trae/skills/weaver-e10-meeting-flow/`）。
- 调用统一入口：`python scripts/meeting_flow.py <命令>`，每个命令输出**单个 JSON 对象**。
- 认证解析顺序（代码内实现，无任何硬编码凭证）：
  1. 环境变量 `E10_BASE_URL` + `E10_COOKIE`（完整 Cookie 头）或 `ETEAMSID`；
  2. `e10-login` CLI（生产路径，weaver-e10-login skill 提供，读 `status`/`whoami`）；
  3. WorkBuddy 开发会话目录（`E10_SESSION_DIR`，默认
     `C:\Users\zhang\.workbuddy\binaries\node\workspace`，读 `sysadmin_cookies.json`
     + `sysadmin_eteamsid.txt`；仅探针/开发用，输出里 `authSource` 会标明）。
- 会话过期迹象：接口 401/403、返回登录页或"登录"字样 msg → `SESSION_EXPIRED`。
- Windows PowerShell 下 JSON 参数**写临时文件传路径**，不要内联（引号会被 shell 破坏）。

## 命令契约总览

| 命令 | 读/写 | 作用 |
|---|---|---|
| `session` | 读 | 检查登录态与环境连通 |
| `workflows` | 读 | 确认当前用户可发起「会议申请」（SELECTED / NOT_FOUND） |
| `form` | 读* | 拉字段能力表（可填字段/必填/选项）+ 布局 id + 当前用户，**生成 context id** |
| `rooms [--name X] [--begin yyyy-MM-dd]` | 读 | 全部会议室 / 名称精确或唯一模糊匹配 |
| `people --names 张三,李四` | 读 | 姓名 → HRM id（也接受直接传 15 位以上数字 id） |
| `depts --names 财务资产组` | 读 | 部门名 → 部门 id |
| `conflict CTX --data <文件>` | 读 | 单独跑 4 个冲突检查（prepare 内部也会跑） |
| `prepare CTX --data <文件> --intent draft\|submit` | 读 | 校验/解析/冲突预检，产出待确认预览，存入 context |
| `create CTX --confirm [--submit]` | **写** | 执行六步写入链，返回 requestId/链接并回读 |
| `detail --request-id ID` | 读 | view 态回查单据：会议 id + 全字段值 + 链接 |

\* `form` 的 loadBaseParam 等同浏览器打开发起页，会拿到一个临时 requestId；
不执行 create 就不会产生任何草稿/会议，临时 id 无副作用。

状态值：`READY / SELECTED / FORM_READY / MATCHED / NEEDS_INPUT / BLOCKED /
DRAFT_CREATED / SUBMITTED / UNCERTAIN / NOT_FOUND / ERROR`。
`ok:true` 只表示命令执行成功，**业务是否可继续看 `status`**。

## 标准作业流程（Agent 必须按此顺序）

### 第 0 步：会话检查
`session` → 非 READY 先解决登录，不继续。

### 第 1 步：确认流程
`workflows`（默认按 workflowId `1302788388361633792` 精确确认）。
`NOT_FOUND` → 如实告知无发起权限/流程停用，停止。

### 第 2 步：拉表单能力，拿 context
`form` → 记录输出里的 `ctx`（形如 `mf_xxxxxxxxxx`）。输出含：
- `requiredKeys`：系统实时必填（脚本会自动满足 `frequent`=永不 等默认项；
  真正需要用户给的是 **会议名称、开始时间、结束时间、会议地点**，发起人默认当前用户）；
- `fields[]`：`key/label/itemType/required/options`（提醒方式等选项 id 从这里实时取，禁止硬编码）；
- `currentUser.hrmId`：发起人默认值（人员字段吃 HRM id，不是 userid）。

### 第 3 步：从自然语言提取参数（Agent 侧，不允许猜）
- 时间必须解析成 `yyyy-MM-dd HH:mm`；只说日期没说钟点 → **追问**，不得补 00:00；
  结束必须晚于开始。"开一小时"由 Agent 算出结束时间。
- 会议室/人员/部门可直接在 prepare 传中文名（脚本内部解析），也可先调
  `rooms/people/depts` 预判；解析不唯一时脚本会在 `errors/missing/candidates` 一次列全。

### 第 4 步：prepare（强制）
数据写 JSON 文件，例如：

```json
{
  "name": "空天信息项目周例会",
  "beginDatetime": "2026-10-23 09:00",
  "endDatetime": "2026-10-23 10:30",
  "room": "第一会议室",
  "members": ["sysadmin", "张三"],
  "departments": ["财务资产组"],
  "otherMembers": "外部专家王老师（纯文本）",
  "mtDesc": "讨论 Q4 计划",
  "materials": "投影仪1台、白板笔",
  "remind": true,
  "totalMember": 8
}
```

字段说明见 [references/field-mapping.md](references/field-mapping.md)。
- `room/members/departments` 名称或数字 id 均可；`totalMember` 不传时默认
  `1（发起人）+ 参会人数 + 参会部门数`；`remind:true` 取系统实时提醒选项（当前唯一：系统消息提醒=6）。
- `--intent draft`：存草稿（src=save，不进审批）；`--intent submit`：提交（src=submit，进审批）。
  两者校验相同（写入链都需要完整的名称/时间/会议室）。
- 返回 `NEEDS_INPUT` → 把 `errors` 一次告诉用户，补完重跑 prepare；
  `BLOCKED` → 转述冲突会议（名称/时段/会议室），请用户换时间或会议室。
- 返回 `READY` → `preview` 是给用户看的确认单，逐字呈现，等待明确答复。

### 第 5 步：create（用户确认后）
- 草稿：`create <ctx> --confirm`
- 提交：`create <ctx> --confirm --submit`
- 成功返回 `DRAFT_CREATED/SUBMITTED` + `requestId/requestName/viewUrl` + 服务端 `readback`。
  向用户汇报标题、编号、链接、草稿/审批状态。
- `UNCERTAIN`：不重试；用 `detail --request-id <临时requestId>` 或
  weaver-e10-workflow 的列表查询回查后再决定，告知用户实际情况。

### 第 6 步（可选）：回查
`detail --request-id ID` 给出会议 id 与全部字段值。审批状态/待办走 weaver-e10-workflow：
`workflow-search --category mine --workflow "会议申请(1302788388361633792)"`。

## 冲突预检规则（服务端判定，脚本只执行不解释绕过）

| 检查接口 | 含义 | cansub=false 行为 |
|---|---|---|
| meetingChkRoom | 会议室时段占用 | **阻断**，返回冲突会议 name/时段/roomName |
| meetingChkMember | 参会人时间冲突 | 仅警告（`warnings`），不阻断 |
| meetingChkRoomAttribute | 会议室属性/容量等 | **阻断** |
| meetingChkService | 服务项冲突（本 skill 不传服务项） | **阻断** |

任一检查接口异常 → 视为阻断。选时段前可先用 `conflict` 命令探测。

## 首版边界（不支持，不要硬做）

- 周期会议（frequent 固定发"0=永不"）；
- 附件上传（`mtAccessorys` 报文格式未实测）；
- 参会客户（crmMembers 固定空）、联系人、会议类型（当前系统 0 条）、自定义地点；
- 移动端布局；
- 审批操作（复用 weaver-e10-workflow）。
用户提到这些需求时明确告知不支持并停止，不要发半截报文试探。

## 关键参考

- 字段与入参映射：[references/field-mapping.md](references/field-mapping.md)
- 六步写入链报文契约与坑：[references/write-contract.md](references/write-contract.md)
- context 与状态文件：`state/create_contexts/mf_*.json`（运行时产物，可删）
