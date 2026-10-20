# 文档详情tab页

- **文档 ID**: `908307006718631936`
- **业务模块**: 知识文档
- **是否 API 接口**: 是
- **请求 URL**: `{OpenApiOrigin}/api/doc/document/v2/tabInfo`
- **请求方式**: `GET`

## 请求参数

| 参数名 | 必选 | 类型 | 说明 |
| --- | --- | --- | --- |
| access_token | 是 | String | 调用接口凭证 获取accessToken信息 |

## 返回参数

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| message | object | 返回结果信息 |
| message.errcode | string | 0-成功，其他-失败 |
| message.errmsg | string | 失败原因 |
| data | string | tab页（doc-正文,attach-附件,log-日志,property-属性,share-共享,version-版本） |
