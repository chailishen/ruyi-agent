# 根据人员id获取监控列表数量

- **文档 ID**: `874488657642790913`
- **业务模块**: 工作流程
- **是否 API 接口**: 是
- **请求 URL**: `{OpenApiOrigin}/api/workflow/list/paService/v1/getMonitorWorkflowRequestCount`
- **请求方式**: `POST`

## 备注

- 备注

## 请求参数

| 参数名 | 必选 | 类型 | 说明 |
| --- | --- | --- | --- |
| access_token | 是 | String | 调用接口凭证 获取accessToken信息 |
| userid | 是 | Long | 用户ID 获取用户ID |
| condition | 否 | Object | 高级搜索条件 下方所有都是其中的参数 |
| requestname | 否 | String | 审批标题 |
| createdate | 否 | String | 发起日期（日期枚举类，包括本日,本周,本月,本年等枚举。注意：参数不传发起日期时默认查询本年数据，传发起日期时，根据发起日期查询数据） |
| requestlevel | 否 | Int | 紧急程度0：正常 1：重要 2：紧急 |
| creatorDepartment | 否 | Long | 发起人所在部门 |
| creatorSubCompany | 否 | Long | 发起人所在分部 |
| creatorcode | 否 | String | 发起人工号 |
| creater | 否 | long | 创建人 |
| requestmark | 否 | String | 审批编号 |
| workflowid | 否 | String | 审批流id集合(多个以,分隔，不会自动转换多版本，如需获取多个版本的流程，请传递对应版本的workflowid) |
| workflowtype | 否 | String | 审批流类型id集合(多个以,分隔) |
| flowStatusList | 否 | list | 流程流转的状态;0-草稿,1-审批中,2-已退回,3-正常归档,4-强制结束,5-已作废,6-待提交,7-暂停,8-撤销,-99-已删除(多个以,分隔) |

## 返回参数

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| errcode | String | 状态码 0：成功，1.接口内部异常，2.必填字段异常 |
| errmsg | String | 返回信息 |
| count | String | 数量 |
