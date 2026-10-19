# 六步写入链报文契约（实测 2026-10-16，草稿 src=save 已端到端验证 + 服务端回读）

`create --confirm` 内部顺序（`scripts/meeting_flow.py`）。
**第 2 步冲突预检在任何落库之前**，阻断时零写入；写入一旦开始，异常只报 UNCERTAIN，不重试。

```
loadBaseParam(创建态)
  └─► chk ×4（零写入，阻断即终止）
       └─► saveFormData（formDataId）
            └─► operateMeetingByType（meetingId）
                 └─► createByList.common
                      └─► workflow/core/flow/create（src=save|submit）
```

## 1. loadBaseParam
`POST /api/workflow/core/flowPage/loadBaseParam`
- params：`{workflowId, isCreate:1}`；body：`{workflowId,isCreate:1,isMobile:0}`
- 取 `data.commonParam.{requestId,authStr,authSignatureStr,userCurrentNodeId,identityId}`
- **每次创建态调用都返回新的临时 requestId**；form 阶段的那个不用、不影响写入。
- view 态（回读用）：params/body 均 `{workflowId,requestId}` + `isCreate:0`，得到的 authStr
  base64 内含 `viewChain=...authType=30`，与创建态不通用。

## 2. 冲突检查 ×4（body 相同）
`POST /api/meeting/detail/{meetingChkRoom|meetingChkMember|meetingChkRoomAttribute|meetingChkService}`
```json
{"hrmids":"逗号拼接HRMid","crmids":"","beginDatetime":"yyyy-MM-dd HH:mm","endDatetime":"...",
 "mtId":"","contacter":"","caller":"HRMid","address":"会议室id","serviceItems":"",
 "totalmember":"3","name":"会议名","frequent":"0","module":"","isMobile":false}
```
- `cansub===false` 即冲突：room/roomAttribute/service 阻断；member 仅警告。
- room 冲突明细在 `data.conflictMsg:[{mtId,creator,name,beginDatetime,endDatetime,roomId,roomName}]`。
- 接口异常按阻断处理。

## 3. saveFormData（会议自定义表单）
`POST /api/meeting/form/core/saveFormData?formId=<会议自定义表单id>`（**query 带 formId**）
```json
{"module":"meeting",
 "customParam":{"viewType":"ADD","refResourceId":"","workflowId":"...","requestId":"...","nodeId":"..."},
 "formData":{"module":"meeting",
   "dataDetails":[{"formField":{"id":"1302788014707867664"},"dataText":{"content":"会议物资文本"}}],
   "client":"pc","dataStatus":"submit",
   "form":{"id":"<formId>"},
   "formLayout":{"id":"<PC1具体布局id，实测 1302790548931510275>"}}}
```
- 无物资时 `dataDetails: []`（浏览器原样）。响应 `data.id` = formDataId。

## 4. operateMeetingByType（会议业务字段载体）
`POST /api/meeting/detail/operateMeetingByType`（**不带 query**）
- 完整字段见脚本 `OPERATE_DEFAULTS` + `_build_operate_payload()`，业务值覆盖：
  `name/caller/beginDatetime/endDatetime/address/mtType/mtDesc/hrmMembers/orgMembers/
  otherMembers/totalMember(int)/remindType/formDataId/layoutId/layoutMultiId/
  until=开始日期` 及 `requestId/nodeId/workflowId/authStr/authSignatureStr`。
- **坑 1（会 400 Bad Request server:wvs）**：`customParams` 和 `fromWorkflowParams`
  必须是**对象**，不能 JSON 字符串。
- 非周期会议也必须带全部周期默认字段与中文标签（缺了前端字段会异常）。
- 响应 `data.id` = 会议 id。**非幂等：禁止原样重放，每次都会新建会议。**

## 5. createByList
`POST /api/bcw/common/relevance/createByList.common`
body 固定 `{"module":"meeting","relevances":[]}`。

## 6. flow/create
`POST /api/workflow/core/flow/create`（**不带 query**）
- 模板见脚本 `FLOW_CREATE_DEFAULTS`；关键覆盖：
  `workflowId,identityId=HRMid,requestId,userCurrentNodeId/fixedNodeId=发起节点,
  dataId=会议id,authStr,authSignatureStr,
  pageKey="create_{wfid}_{毫秒时间戳}",src="save"|"submit",isCreate=true`。
- **坑 2**：业务结果在**响应顶层**，不在 `data` 下：
  `{status:true,requestId,requestName,resultType:"SUCCESS_RELOAD_CURRENT_PAGE",
    isDraft:true,flowIsCreateSuccess:true}`。
- 成功判据：`flowIsCreateSuccess===true`。
- `src=submit` 会真实进入审批流（会议室负责人 → 领导审批），只能由用户明确要求时使用。

## 回读链（detail）
1. loadBaseParam view 态 → view authStr；
2. `POST /api/workflow/core/flowPage/loadFrameParam`（isCreate:0）→ 递归找 `dataId` = 会议 id；
3. `GET /api/meeting/detail/getMeetingDetailField`（operateType=UPDATE，带 meetingId、
   urlencoded customParams、authStr/authSignatureStr）
   → `data.meetingFields.items.<key>.value`：
   人员/部门/会议室为对象数组 `[{id,name,content}]`，remindType 为 `["6"]`，totalMember 为数字。

## 发起页/单据链接
- 发起：`/sp/workflow/flowpage/create/{workflowId}`
- 单据：`/sp/workflow/flowpage/view/{requestId}`
