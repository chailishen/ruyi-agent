# 通过流程workflowId获取子流程设置

- **文档 ID**: `874490929781153792`
- **业务模块**: 工作流程
- **是否 API 接口**: 是
- **请求 URL**: `{OpenApiOrigin}/api/workflow/core/paService/v1/getSubRequestSetByWorkflowId`
- **Content-Type**: `application/json`

## 备注

- POST （Content_Type: application/json），备注：access_token放在params中

## 请求参数

| 参数名 | 必选 | 类型 | 说明 |
| --- | --- | --- | --- |
| access_token | 是 | String | 调用接口凭证 获取accessToken信息 |
| userIdStr | 是 | Long | 用户ID |
| workflowId | 是 | Long | 流程workflowId |
| enable | 否 | boolean | 是否查询开启的子流程设置，false表示查询所有子流程设置，true表示查询仅开启的子流程设置，默认为false。 |

## 返回参数

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| errcode | String | 返回码 |
| errmsg | String | 返回信息 |
| data | Map | 流程数据 |
