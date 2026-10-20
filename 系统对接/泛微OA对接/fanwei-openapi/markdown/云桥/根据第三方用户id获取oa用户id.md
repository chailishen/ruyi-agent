# 根据第三方用户id获取oa用户id

- **文档 ID**: `908343788977938433`
- **业务模块**: 云桥
- **是否 API 接口**: 是
- **请求 URL**: `{OpenApiOrigin}/api/eb/open/hrm/v1/getEmployeeIdByThirdUserId`
- **请求方式**: `GET`

## 请求参数

| 参数名 | 必选 | 类型 | 说明 |
| --- | --- | --- | --- |
| access_token | 是 | string | 调用接口凭证  获取accessToken信息 |
| corpKey | 是 | string | 企业key |
| thirdUserId | 是 | string | 第三方用户id |

## 返回参数

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| errcode | String | 返回码 |
| errmsg | String | 返回信息 |
| data | String | oa用户id |
