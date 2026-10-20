# 获取邮件详情SAPI接口

- **文档 ID**: `410184098531770368`
- **业务模块**: 邮件
- **是否 API 接口**: 否（说明文档）
- **请求方式**: `POST`

## 请求参数

| 参数名 | 必选 | 类型 | 说明 |
| --- | --- | --- | --- |
| access_token | 是 | String | 调用接口凭证 获取accessToken信息 |
| mailId | 是 | String | 邮件主键id |
| resourceWorkCode | 是 | String | 邮件归属人工号 |

## 返回参数

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| errmsg | String | 失败原因 |
| errcode | String | 错误码 |
| mailSubject | String | 邮件主题 |
| clobContent | String | 邮件内容 |
| sendFrom | String | 发件人 |
| sendFromMap | Object | 外部邮件发件人详情 |
| sendFromInternalMap | Map | 内部邮件发件人详情 |
| toMap | Map | 收件人 |
| ccMap | Map | 抄送人 |
| bccMap | Map | 密送人 |
| priority | int | 重要性 |
| sendDate | String | 发送时间 |
| folderId | long | 文件夹id |
| needReceipt | int | 需要回执 |
| readStatus | int | 阅读状态 |
| internal | int | 是否内部邮件 |
| star | int | 是否标星 |
| waitdeal | int | 是否待办 |
| recallState | int | 邮件撤回状态 |
| fileInfos | Map | 邮件附件详情 |
| secretLevel | int | 邮件密级 |
| secretDeadline | String | 保密期限 |
| classificationRight | int | 密级权限 |
| countryLevel | long | 国家 |

## 正文

### 支持版本：
- 251001
### 请求URL：
- /sapi/mail/base/v1/getMailView
### 请求方式：
- POST
### 请求参数：
| 参数名 | 必选 | 类型 | 说明 |
| --- | --- | --- | --- |
| access_token | 是 | String | 调用接口凭证 获取accessToken信息 |
| mailId | 是 | String | 邮件主键id |
| resourceWorkCode | 是 | String | 邮件归属人工号 |
### 请求示例：
### query方式返回示例：
### 返回参数说明：
| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| errmsg | String | 失败原因 |
| errcode | String | 错误码 |
| mailSubject | String | 邮件主题 |
| clobContent | String | 邮件内容 |
| sendFrom | String | 发件人 |
| sendFromMap | Object | 外部邮件发件人详情 |
| sendFromInternalMap | Map | 内部邮件发件人详情 |
| toMap | Map | 收件人 |
| ccMap | Map | 抄送人 |
| bccMap | Map | 密送人 |
| priority | int | 重要性 |
| sendDate | String | 发送时间 |
| folderId | long | 文件夹id |
| needReceipt | int | 需要回执 |
| readStatus | int | 阅读状态 |
| internal | int | 是否内部邮件 |
| star | int | 是否标星 |
| waitdeal | int | 是否待办 |
| recallState | int | 邮件撤回状态 |
| fileInfos | Map | 邮件附件详情 |
| secretLevel | int | 邮件密级 |
| secretDeadline | String | 保密期限 |
| classificationRight | int | 密级权限 |
| countryLevel | long | 国家 |
