# 根据流程数据ID查询审批数据

- **文档 ID**: `840693883516755968`
- **业务模块**: 工作流程 / 获取流程信息
- **是否 API 接口**: 是
- **请求 URL**: `{OpenApiOrigin}/workflow/v2/getInfoByID`
- **请求方式**: `GET`

## 请求参数

| 参数名 | 必选 | 类型 | 说明 |
| --- | --- | --- | --- |
| access_token | 是 | String | 调用接口凭证 获取accessToken信息 |
| userid | 是 | Long | 用户ID 获取用户ID |
| id | 是 | Long | 审批数据ID 获取审批数据ID |

## 返回参数

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| errcode | String | 返回码 |
| errmsg | String | 返回信息 |
| formData | String | 审批表数据详情 |
| createTime | String | 审批表数据创建时间 |
| module | String | 模块名称 |
| name | String | 审批数据名称 |
| dataStatus | String | 审批数据状态 |
| dataDetails | String | 审批数据各字段详情 |
| fileDownload_Urls | Object | 附件下载地址 |
| creator | String | 审批提交人信息 |
| formId | Long | 表单ID |
| id | Long | 审批数据ID |
| statusType | String | 分别是’unSubmit’:待提交（草稿箱的不算待提交）, ‘inProcess’:审批中, ‘finish’:已结束 |
