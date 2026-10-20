# 刷新accessToken信息

- **文档 ID**: `228362355153567744`
- **业务模块**: 认证
- **是否 API 接口**: 是
- **请求 URL**: `{OpenApiOrigin}/oauth2/refresh_token`
- **Content-Type**: `application/json`

## 备注

- POSTContent-Type: application/json
- 备注：

## 请求参数

| 参数名 | 必选 | 类型 | 说明 |
| --- | --- | --- | --- |
| grant_type | 是 | String | 授权类型，固定：refresh_token |
| refresh_token | 是 | String | 刷新令牌凭证，有效时间默认为24小时 |

## 返回参数

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| errcode | String | 返回码 |
| errmsg | String | 返回信息 |
| accessToken | String | 接口凭证，有效时间默认为2小时 |
| refreshToken | String | 刷新令牌，有效时间默认为24小时 |
| expire_in | Int | 有效时间，单位为秒 |
