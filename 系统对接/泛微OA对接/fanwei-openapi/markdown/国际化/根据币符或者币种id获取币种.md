# 根据币符或者币种id获取币种

- **文档 ID**: `249279858977275904`
- **业务模块**: 国际化 / 货币
- **是否 API 接口**: 是
- **请求 URL**: `{OpenApiOrigin}/api/i18n/currency/v1/getCurrency`
- **请求方式**: `POST`

## 请求参数

| 参数名 | 必选 | 类型 | 说明 |
| --- | --- | --- | --- |
| access_token | 是 | String | 调用接口凭证 获取accessToken信息 |
| symbol | 否 | String | 币符。币符和币种ID二选一，如果同时传递，则取币种ID |
| unitId | 否 | long | 币种ID。币符和币种ID二选一，如果同时传递，则取币种ID |

## 返回参数

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| code | String | 状态码 200：成功 , 500：系统异常 |
| msg | String | 响应信息 |
| status | boolean | 状态 |
| data | List | 币种信息 |
| data.id | long | 币种ID |
| data.currencyName | String | 币种名称 |
| data.symbol | String | 币符 |
| data.isEnable | int | 是否启用 1：启用 0：未启用 |
| data.labelId | long | 币种名称标签ID |
| data.isBase | int | 是否本位币 1：是 0：不是 |
| fail | boolean | 是否失败 |
