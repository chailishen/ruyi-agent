# 免登第三方-根据本系统token查询用户

- **文档 ID**: `840673671426703360`
- **业务模块**: 免登
- **是否 API 接口**: 是
- **请求 URL**: `{OpenApiOrigin}/oauth2/getUserInfo`
- **请求方式**: `POST`

## 备注

- 备注：

## 请求参数

| 参数名 | 必选 | 类型 | 说明 |
| --- | --- | --- | --- |
| eteams_token | 是 | String | 获取本系统token |

## 返回参数

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| errcode | String | 返回码 |
| errmsg | String | 返回信息 |
