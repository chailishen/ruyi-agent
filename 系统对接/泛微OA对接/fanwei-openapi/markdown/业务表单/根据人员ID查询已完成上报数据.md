# 根据人员ID查询已完成上报数据

- **文档 ID**: `840716780047007745`
- **业务模块**: 业务表单
- **是否 API 接口**: 是
- **请求 URL**: `{OpenApiOrigin}/form/v2/getFinfishData`
- **请求方式**: `GET`

## 请求参数

| 参数名 | 必选 | 类型 | 说明 |
| --- | --- | --- | --- |
| access_token | 是 | String | 调用接口凭证 获取accessToken信息 |
| userid | 是 | Long | 用户ID 获取用户ID |
| pageNo | 否 | Int | 分页页码 |
| pageSize | 否 | Int | 分页展示数据数，默认最大20 |

## 返回参数

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| errcode | String | 返回码 |
| errmsg | String | 返回信息 |
| id | String | 表单数据ID |
| name | String | 表单数据名称 |
| reporter | String | 表单数据提交人信息 |
| status | String | 表单数据状态 |
| tenantKey | String | 所属团队识别码 |
