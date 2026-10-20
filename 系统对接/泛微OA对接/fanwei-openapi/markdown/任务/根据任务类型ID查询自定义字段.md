# 根据任务类型ID查询自定义字段

- **文档 ID**: `840678722449973249`
- **业务模块**: 任务
- **是否 API 接口**: 是
- **请求 URL**: `{OpenApiOrigin}/task/v2/queryFormInfoByTaskType`
- **请求方式**: `GET`

## 请求参数

| 参数名 | 必选 | 类型 | 说明 |
| --- | --- | --- | --- |
| access_token | 是 | String | 调用接口凭证 获取accessToken信息 |
| taskTypeId | 是 | String | 任务类型ID 获取任务类型ID，当不传或为空时，查询通用自定义字段 |

## 返回参数

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| errcode | String | 返回码 |
| errmsg | String | 返回信息 |
| form.id | String | 任务自定义字段表单ID |
| form.title | String | 控件名称 |
| fields.fieldId | String | 控件ID |
| selectionId | String | 选项型控件选项ID |
| name | String | 选项名称 |
