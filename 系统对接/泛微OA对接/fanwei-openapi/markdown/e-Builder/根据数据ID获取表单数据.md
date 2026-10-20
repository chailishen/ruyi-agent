# 根据数据ID获取表单数据

- **文档 ID**: `840721255360987136`
- **业务模块**: e-Builder / 应用建模 / 表单数据操作
- **是否 API 接口**: 是
- **请求 URL**: `{OpenApiOrigin}/api/ebuilder/form/dataset/v1/getDataById`
- **请求方式**: `POST`

## 备注

- 备注：

## 请求参数

| 参数名 | 必选 | 类型 | 说明 |
| --- | --- | --- | --- |
| access_token | 是 | String | 调用接口凭证 获取accessToken信息 |
| userid | 是 | Long | 用户ID 获取用户ID |
| datajson | 是 | Object | 数据信息 |

## 返回参数

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| id | Long | 数据id |
| objId | Long | 表单id |
| isReturnDetail | String | 是否需要返回明细(默认不返回; y返回; n不返回) |
| code | String | 返回码 |
| msg | String | 返回信息 |
| creator | String | 创建人 |
| obj_id | String | 表单id |
| id | String | 数据id |
| name | String | 数据标题 |
| fieldKey | String | 字段类型 |
| fieldName | String | 字段显示名 |
| value | String | 字段值 |
| showName | String | 字段显示值 |
| subFormId | Long | 字段id |
| dataIndex | int | 明细下标id |
| fieldOptionId | String | 字段选项id |
| fieldOptionName | String | 字段选项名 |
