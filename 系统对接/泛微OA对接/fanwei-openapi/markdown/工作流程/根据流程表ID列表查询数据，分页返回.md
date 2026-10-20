# 根据流程表ID列表查询数据，分页返回

- **文档 ID**: `840712854371401729`
- **业务模块**: 工作流程
- **是否 API 接口**: 是
- **请求 URL**: `{OpenApiOrigin}/workflow/v2/queryStatFlowByFormIds`
- **请求方式**: `POST`

## 请求参数

| 参数名 | 必选 | 类型 | 说明 |
| --- | --- | --- | --- |
| access_token | 是 | String | 调用接口凭证 获取accessToken信息 |
| userid | 是 | Long | 用户ID 获取用户ID |
| formIds | 是 | List<Long> | 审批表ID列表（最大10） 获取审批表ID |
| pageNo | 否 | Integer | 分页页码 |
| pageSize | 否 | Integer | 每页数量（最大200） |

## 返回参数

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| errcode | String | 返回码 |
| errmsg | String | 返回信息 |
| flowMaps | List | 流程列表 |
