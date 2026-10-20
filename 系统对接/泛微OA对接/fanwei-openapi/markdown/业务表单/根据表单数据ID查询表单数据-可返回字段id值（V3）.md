# 根据表单数据ID查询表单数据-可返回字段id值（V3）

- **文档 ID**: `840716436416069632`
- **业务模块**: 业务表单
- **是否 API 接口**: 是
- **请求 URL**: `{OpenApiOrigin}/form/v3/queryDataReportById`
- **请求方式**: `GET`

## 备注

- 备注：

## 请求参数

| 参数名 | 必选 | 类型 | 说明 |
| --- | --- | --- | --- |
| access_token | 是 | String | 调用接口凭证 获取accessToken信息 |
| userid | 是 | Long | 用户ID 获取用户ID |
| id | 是 | Long | 表单数据ID 获取表单数据ID |

## 返回参数

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| errcode | String | 返回码 |
| errmsg | String | 返回信息 |
| createTime | String | 表单数据提交时间 |
| module | String | 所属模块 |
| name | String | 表单数据名称 |
| dataStatus | String | 状态 |
| dataDetails | String | 各字段详情 dataDetails返回示例 dataDetails明细表返回示例 |
| fileDownload_Urls | Object | 附件下载地址 |
