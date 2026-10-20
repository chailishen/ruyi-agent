# 根据分类ID查询表单

- **文档 ID**: `840716174430576641`
- **业务模块**: 业务表单
- **是否 API 接口**: 是
- **请求 URL**: `{OpenApiOrigin}/form/v2/getFormByCategoryId`
- **请求方式**: `GET`

## 请求参数

| 参数名 | 必选 | 类型 | 说明 |
| --- | --- | --- | --- |
| access_token | 是 | String | 调用接口凭证 获取accessToken信息 |
| userid | 是 | Long | 用户ID 获取用户ID |
| categoryId | 是 | Long | 分类ID 获取表单分类ID |

## 返回参数

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| errcode | String | 返回码 |
| errmsg | String | 返回信息 |
| id | String | 表单ID |
| name | String | 表单名称 |
