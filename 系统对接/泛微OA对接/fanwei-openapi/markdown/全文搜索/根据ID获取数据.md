# 根据ID获取数据

- **文档 ID**: `367844910646165504`
- **业务模块**: 全文搜索
- **是否 API 接口**: 是
- **请求 URL**: `{OpenApiOrigin}/api/esearch/search/xiaoe/queryByIdsForXE`
- **请求方式**: `POST`

## 请求参数

| 参数名 | 必选 | 类型 | 说明 |
| --- | --- | --- | --- |
| ids | 是 | List<String> | 数据id |
| tenantKey | 是 | tenantKey | 租户Key |
| moduleKey | 是 | moduleKey | 模块编码 |

## 返回参数

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| code | String | 返回码 |
| msg | String | 返回信息 |
| id | String | 数据id |
| tenantKey | String | 租户编码 |
| moduleKey | String | 模块编码 |
| title | String | 标题 |
| contents | String | 内容 |
| createTime | String | 创建时间 |
| updateTime | String | 更新时间 |
