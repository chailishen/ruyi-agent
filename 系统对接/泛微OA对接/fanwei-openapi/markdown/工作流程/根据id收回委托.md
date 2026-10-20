# 根据id收回委托

- **文档 ID**: `408044690571526144`
- **业务模块**: 工作流程
- **是否 API 接口**: 是
- **请求 URL**: `{OpenApiOrigin}/api/workflow/core/paService/v1/recoverAgentWithId?access_token=`

## 请求参数

| 参数名 | 必选 | 类型 | 说明 |
| --- | --- | --- | --- |
| access_token |  | String |  |
| userid |  | long | 用户ID |
| agentIds |  | String | 委托设置id；多个id以,分割 |
| recoverPendingWf |  | int | 是否收回流转中的代理；0：否、1：是（默认） |

## 返回参数

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| errcode | String | 返回码 |
| errmsg | String | 提示信息 |
| requestId | long | 流程ID |
