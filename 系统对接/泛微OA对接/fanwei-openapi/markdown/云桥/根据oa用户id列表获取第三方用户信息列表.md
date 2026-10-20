# 根据oa用户id列表获取第三方用户信息列表

- **文档 ID**: `908343007256723457`
- **业务模块**: 云桥
- **是否 API 接口**: 是
- **请求 URL**: `{OpenApiOrigin}/api/eb/open/hrm/v1/getThirdUserListByOaEmployeeIdList`
- **请求方式**: `POST`
- **Content-Type**: `application/json`

## 备注

- 注：body中需要传递oa用户id列表；Content-Type：application/json

## 请求参数

| 参数名 | 必选 | 类型 | 说明 |
| --- | --- | --- | --- |
| access_token | 是 | string | 调用接口凭证  获取accessToken信息 |
| corpKey | 是 | string | 企业key |

## 返回参数

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| errcode | String | 返回码 |
| errmsg | String | 返回信息 |
| data | String | 第三方用户信息 |
