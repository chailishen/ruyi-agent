# 根据人员ID查询待办审批数据

- **文档 ID**: `840712150130106369`
- **业务模块**: 工作流程
- **是否 API 接口**: 是
- **请求 URL**: `{OpenApiOrigin}/workflow/v2/getTodoData`
- **请求方式**: `GET`

## 请求参数

| 参数名 | 必选 | 类型 | 说明 |
| --- | --- | --- | --- |
| access_token | 是 | String | 调用接口凭证 获取accessToken信息 |
| userid | 是 | Long | 用户ID 获取用户ID |
| pageNo | 否 | Int | 分页页码 |
| pageSize | 否 | Int | 分页展示数据数，默认最大20 |

## 返回参数

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| errcode | String | 返回码 |
| errmsg | String | 返回信息 |
| creator | String | 审批提交人信息 |
| delete | String | 是否删除 |
| id | String | 审批数据ID |
| name | String | 审批数据名称 |
