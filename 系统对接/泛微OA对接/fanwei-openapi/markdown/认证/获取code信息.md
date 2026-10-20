# 获取code信息

- **文档 ID**: `840673181800431617`
- **业务模块**: 认证
- **是否 API 接口**: 是
- **请求 URL**: `{OpenApiOrigin}/oauth2/authorize`
- **请求方式**: `GET、POST`

## 请求参数

| 参数名 | 必选 | 类型 | 说明 |
| --- | --- | --- | --- |
| corpid | 是 | String | 注册企业corpId 开发者资料中查看corpId |
| response_type | 是 | String | 返回类型，此时固定为：code |
| state | 是 | String | 重定向后会带上state参数，企业可以填写a-zA-Z0-9的参数值，长度不可超过128个字节 |

## 返回参数

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| errcode | String | 返回码 |
| errmsg | String | 返回信息 |
| code | String | code信息，有效时间为10分钟且只能使用一次 |
