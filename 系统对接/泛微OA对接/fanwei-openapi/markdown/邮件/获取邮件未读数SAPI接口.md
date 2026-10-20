# 获取邮件未读数SAPI接口

- **文档 ID**: `410224735809437696`
- **业务模块**: 邮件
- **是否 API 接口**: 否（说明文档）
- **请求方式**: `GET`

## 请求参数

| 参数名 | 必选 | 类型 | 说明 |
| --- | --- | --- | --- |
| access_token | 是 | String | 调用接口凭证 获取accessToken信息 |
| resourceWorkCode | 是 | String | 邮件归属人工号 |
| mailBox | 否 | String | 文件夹（默认inbox）收件箱：inbox已删除：deleted垃圾箱：trash待办：todo标星：star所有邮件：Allmessages |

## 返回参数

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| errmsg | String | 失败原因 |
| errcode | String | 错误码 |
| count | int | 未读邮件数量 |

## 正文

### 支持版本：
- 251001
### 请求URL：
- /sapi/mail/base/v1/getMailUnReadCount
### 请求方式：
- GET
### 请求参数：
| 参数名 | 必选 | 类型 | 说明 |
| --- | --- | --- | --- |
| access_token | 是 | String | 调用接口凭证 获取accessToken信息 |
| resourceWorkCode | 是 | String | 邮件归属人工号 |
| mailBox | 否 | String | 文件夹（默认inbox）收件箱：inbox已删除：deleted垃圾箱：trash待办：todo标星：star所有邮件：Allmessages |
### 请求示例：
### 返回示例：
### 返回参数说明：
| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| errmsg | String | 失败原因 |
| errcode | String | 错误码 |
| count | int | 未读邮件数量 |
