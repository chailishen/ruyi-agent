# 根据表单id和单个类型查询时间范围内上报数据

- **文档 ID**: `840717093637464065`
- **业务模块**: 业务表单
- **是否 API 接口**: 是
- **请求 URL**: `{OpenApiOrigin}/form/v2/queryChangedReportsByType`
- **请求方式**: `GET`

## 请求参数

| 参数名 | 必选 | 类型 | 说明 |
| --- | --- | --- | --- |
| access_token | 是 | String | 调用接口凭证 |
| userid | 是 | Long | 用户ID 获取用户ID |
| id | 是 | Long | 表单ID 获取表单ID |
| type | 是 | String | 新建create、编辑update、删除delete |
| datamap | 是 | String | 查询日期区间 |
| pageNo | 否 | Int | 页码 |
| pageSize | 否 | Int | 每页显示条数 |

## 返回参数

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| errcode | String | 返回码 |
| errmsg | String | 返回信息 |
| formData | String | 表单数据ID |
| id | String | 表单ID |
| reporter | String | 提交人信息 |
| status | String | 状态 |
