# 根据表单ID列表查询表单字段

- **文档 ID**: `840712712611438592`
- **业务模块**: 工作流程 / 工作流管理
- **是否 API 接口**: 是
- **请求 URL**: `{OpenApiOrigin}/workflow/v2/queryFormFieldByFormIds`
- **请求方式**: `POST`

## 请求参数

| 参数名 | 必选 | 类型 | 说明 |
| --- | --- | --- | --- |
| access_token | 是 | String | 调用接口凭证 获取accessToken信息 |
| userid | 是 | Long | 用户ID 获取用户ID |
| formIds | 是 | List<Long> | 表单ID列表（最大10） 获取表单ID |

## 返回参数

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| errcode | String | 返回码 |
| errmsg | String | 返回信息 |
| fieldMaps | Map<String,List> | 表单ID对应的字段列表 |
| componentKey | String | 字段类型 |
| delete | Boolean | 是否删除 |
| id | Long | 字段Id |
| required | Boolean | 是否必填 |
| title | String | 字段名称 |
