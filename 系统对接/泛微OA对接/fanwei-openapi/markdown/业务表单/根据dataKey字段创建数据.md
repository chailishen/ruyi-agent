# 根据dataKey字段创建数据

- **文档 ID**: `192722769341841408`
- **业务模块**: 业务表单
- **是否 API 接口**: 是
- **请求 URL**: `{OpenApiOrigin}/api/formdatareport/v2/createDataReportByDataKey`
- **请求方式**: `POST`

## 请求参数

| 参数名 | 必选 | 类型 | 说明 |
| --- | --- | --- | --- |
| access_token | 是 | String | 调用接口凭证 获取accessToken信息 |
| userid | 是 | Long | 用户ID 获取用户ID |
| formId | 是 | Long | 表单ID 获取表单ID |
| dataMap | 是 | String | 表单自定义字段集合 datamap传值说明 |
| layoutId | 否 | Long | 布局ID |

## 返回参数

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| errcode | String | 返回码 |
| errmsg | String | 返回信息 |
| reportId | Long | 表单数据ID |
