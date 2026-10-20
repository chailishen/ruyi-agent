# 根据企业微信ID查找人员（V3）

- **文档 ID**: `840675183213248513`
- **业务模块**: 人员
- **是否 API 接口**: 是
- **请求 URL**: `{OpenApiOrigin}/user/v3/findUserByWechatUserId`
- **请求方式**: `GET`

## 请求参数

| 参数名 | 必选 | 类型 | 说明 |
| --- | --- | --- | --- |
| access_token | 是 | String | 调用接口凭证 获取accessToken信息 |
| wechatUserId | 是 | String | 企业微信账号（可以在通讯录-人员详情-基本信息页面找到） |

## 返回参数

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| errcode | String | 返回码 |
| errmsg | String | 返回信息 |
| userid | String | 用户ID |
| name | String | 用户名 |
| department | List | 部门列表 |
| mobile | String | 手机号码 |
| email | String | 邮箱 |
| jobNum | String | 工号 |
| hireDdate | String | 入职日期 |
| sex | String | 性别 |
| status | String | 成员状态：在职normal、离职unavailable、已邀请invited |
| account | String | 帐号 |
| telephone | String | 电话 |
| otherDepartments | String | 兼职部门ID列表 |
| position | String | 岗位 |
| otherPositions | String | 兼职岗位列表 |
| grade | String | 职级 |
| superior | String | 上级ID |
| education | String | 学历 |
| degree | String | 学位 |
| graduate_School | String | 毕业院校 |
| graduate_Date | String | 毕业日期（时间戳，毫秒级） |
| formData | Object | 自定义字段信息 |
| updateTime | String | 基本信息更新时间 |
| id_No | String | 身份证 |
| birthday | String | 出生日期 （时间戳，毫秒级） |
| age | Integer | 年龄 |
| marital_Status | String | 婚姻状况：married：已婚、unmarried：未婚、​divorced：离异 |
| native_Place | String | 籍贯 |
| nation | String | 民族 |
| householdType | String | 户口类型 |
| politicsStatus | String | 政治面貌 |
| residence_Place | String | 现居住地 |
| family_Contact | String | 家庭联系方式 |
| work_Year | Double | 个人工龄 |
| child_Status | String | 子女状态 |
