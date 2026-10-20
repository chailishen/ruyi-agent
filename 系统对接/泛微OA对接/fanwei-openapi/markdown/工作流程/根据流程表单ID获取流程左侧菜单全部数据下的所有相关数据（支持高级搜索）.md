# 根据流程表单ID获取流程左侧菜单全部数据下的所有相关数据（支持高级搜索）

- **文档 ID**: `840715538717573121`
- **业务模块**: 工作流程
- **是否 API 接口**: 是
- **请求 URL**: `{OpenApiOrigin}/workflow/v3/getAllById`
- **请求方式**: `GET`

## 请求参数

| 参数名 | 必选 | 类型 | 说明 |
| --- | --- | --- | --- |
| access_token | 是 | String | 调用接口凭证 获取accessToken信息 |
| userid | 是 | Long | 用户ID 获取用户ID |
| id | 是 | Long | 表单ID 获取表单ID |
| param | 是 | String | 高级搜索条件（参数JSON格式） |
| pageNo | 否 | Int | 分页页码 |
| pageSize | 否 | Int | 分页展示数据数，默认最大200 |

## 返回参数

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| flowName | String | 流程名称数组 |
| flowStatus | String | 流程状态：审批中notFinish、已结束finish |
| flowFinishTime | String | 结束时间区间(startTime、endTime) |
| flowSubmitTime | String | 提交时间区间(startTime、endTime) |
| flowCreator | Long | 申请人列表 |
| flowCreatorDepartment | Long | 申请人部门列表 |
| errcode | String | 返回码 |
| errmsg | String | 返回信息 |
| creator | String | 申请人信息 |
| delete | String | 是否删除 |
| id | String | 流程数据ID |
| requestTime | Date | 流程提交时间 |
| finishTime | Date | 流程结束时间 |
| flowSequence | Long | 固定流程表id-workflowid |
| formData | Long | 表单数据Id |
| formId | Long | 表单id |
| serNum | serNum | serNum |
| statusType | String | 流程状态类型（已结束：finish审批中：inProcess待提交（草稿箱的不算待提交）：unSubmit） |
