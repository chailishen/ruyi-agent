# 查询所有彻底删除人员id接口（V3）

- **文档 ID**: `840675131816247296`
- **业务模块**: 人员
- **是否 API 接口**: 是
- **请求 URL**: `{OpenApiOrigin}/user/v3/findAllPermanentlyDeleteUsers`
- **请求方式**: `GET`

## 请求参数

| 参数名 | 必选 | 类型 | 说明 |
| --- | --- | --- | --- |
| access_token | 是 | string | 调用接口凭证 获取accessToken信息 |

## 返回参数

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| errcode | String | 返回码 |
| errmsg | String | 返回信息 |
| data | List | 人员ID列表 |
