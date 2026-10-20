# 获取第三方APP的accessToken

- **文档 ID**: `908342328668667904`
- **业务模块**: 云桥
- **是否 API 接口**: 是
- **请求 URL**: `{OpenApiOrigin}/api/eb/open/thirdapi/v1/getAccessToken`
- **请求方式**: `GET`

## 请求参数

| 参数名 | 必选 | 类型 | 说明 |
| --- | --- | --- | --- |
| access_token | 是 | string | 调用接口凭证 获取accessToken信息 |
| agentKey | 是 | string | 应用key |

## 返回参数

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| errcode | String | 返回码 |
| errmsg | String | 返回信息 |
| data | String | 第三方APP的accessToken |
