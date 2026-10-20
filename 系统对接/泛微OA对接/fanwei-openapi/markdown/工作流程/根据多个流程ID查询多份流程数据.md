# 根据多个流程ID查询多份流程数据

- **文档 ID**: `840712785760100353`
- **业务模块**: 工作流程
- **是否 API 接口**: 是
- **请求 URL**: `{OpenApiOrigin}/workflow/v2/queryFlowInfoByFlowIds`
- **请求方式**: `POST`

## 请求参数

| 参数名 | 必选 | 类型 | 说明 |
| --- | --- | --- | --- |
| access_token | 是 | String | 调用接口凭证 获取accessToken信息 |
| userid | 是 | Long | 用户ID 获取用户ID |
| flowIds | 是 | List<Long> | 审批数据ID列表（最大10） 获取审批数据ID |

## 返回参数

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| errcode | String | 返回码 |
| errmsg | String | 返回信息 |
| flowInfos | List | 已办列表 |
| formData | Object | 流程数据详情 |
| fileDownload_Urls | Object | 附件下载地址 |
| flowRequest | Object | 流程数据 |
