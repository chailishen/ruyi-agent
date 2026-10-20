# 根据表单ID查询字段

- **文档 ID**: `840693801988751360`
- **业务模块**: 工作流程 / 工作流管理
- **是否 API 接口**: 是
- **请求 URL**: `{OpenApiOrigin}/workflow/v2/getFieldById`
- **请求方式**: `GET`

## 请求参数

| 参数名 | 必选 | 类型 | 说明 |
| --- | --- | --- | --- |
| access_token | 是 | String | 调用接口凭证 获取accessToken信息 |
| userid | 是 | Long | 用户ID 获取用户ID |
| id | 是 | Long | 表单ID 表单ID |

## 返回参数

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| errcode | String | 返回码 |
| errmsg | String | 返回信息 |
| componentKey | String | 字段类型 |
| id | Long | 字段ID |
| title | String | 字段名称 |
| subFormId | Long | 明细表id 主表字段为-1，明细字段为实际明细表id |
| subFormTitle | String | 明细表标题 |
| Text | 文本输入框 |  |
| Textarea | 多行文本框 |  |
| RadioBox | 单选框 |  |
| Select | 下拉菜单 |  |
| DateComponent | 日期 |  |
| NumberComponent | 数字输入框 |  |
| Money | 金额 |  |
| Email | 邮箱 |  |
| Phone | 电话 |  |
| Mobile | 手机 |  |
| Monitor | 运算控件 |  |
| Raty | 评分控件 |  |
| ProgressBar | 进度条 |  |
| IDCard | 身份证 |  |
| PositionComponent | 地理位置 |  |
| CheckBox | 复选框 |  |
| DateInterval | 日期区间 |  |
| ComboSelect | 多级下拉框 |  |
| Mainline | 关联项目 |  |
| Task | 关联任务 |  |
| Document | 关联文档 |  |
| Workflow | 关联审批 |  |
| AgendaComponent | 关联日程 |  |
| FormComponent | 关联表单数据 |  |
| CustomerComponent | 关联客户 |  |
| ClueComponent | 关联线索 |  |
| OrderComponent | 关联订单 |  |
| ContactComponent | 客户联系人 |  |
| ChanceComponent | 关联商机 |  |
| ProductionComponent | 关联产品 |  |
| ContractComponent | 关联合同 |  |
| Employee | 人员 |  |
| Department | 部门 |  |
