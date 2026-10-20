# 根据oa用户id获取第三方用户信息

- **文档 ID**: `908342826938818561`
- **业务模块**: 云桥
- **是否 API 接口**: 是
- **请求 URL**: `{OpenApiOrigin}/api/eb/open/hrm/v1/getThirdUserByOaEmployeeId`
- **请求方式**: `GET`

## 请求参数

| 参数名 | 必选 | 类型 | 说明 |
| --- | --- | --- | --- |
| access_token | 是 | string | 调用接口凭证  获取accessToken信息 |
| corpKey | 是 | string | 企业key |
| oaEmployeeId | 是 | string | oa用户id |

## 返回参数

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| errcode | String | 返回码 |
| errmsg | String | 返回信息 |
| data | String | 第三方用户信息 |
