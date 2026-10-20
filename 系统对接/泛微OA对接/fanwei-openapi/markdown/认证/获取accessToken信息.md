# 获取accessToken信息

- **文档 ID**: `840673319280451584`
- **业务模块**: 认证
- **是否 API 接口**: 是
- **请求 URL**: `{OpenApiOrigin}/oauth2/access_token`
- **请求方式**: `POST`
- **Content-Type**: `application/json`

## 备注

- Content-Type: application/json

## 请求参数

| 参数名 | 必选 | 类型 | 说明 |
| --- | --- | --- | --- |
| app_key | 是 | String | 应用app_key 应用审核通过后显示 |
| app_secret | 是 | String | 应用app_secret 应用审核通过后显示 |
| grant_type | 是 | String | 授权类型，固定：authorization_code |
| code | 是 | String | 身份票据 获取code信息 |

## 返回参数

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| errcode | String | 返回码 |
| errmsg | String | 返回信息 |
| accessToken | String | 接口凭证，有效时间默认为2小时 |
| refreshToken | String | 刷新令牌，有效时间默认为24小时 |
| expires_in | Int | 有效时间，单位为秒 |
