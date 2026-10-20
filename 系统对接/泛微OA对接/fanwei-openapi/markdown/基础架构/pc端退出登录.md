# pc端退出登录

- **文档 ID**: `233077060837310464`
- **业务模块**: 基础架构
- **是否 API 接口**: 是
- **请求 URL**: `{OpenApiOrigin}/api/basicserver/v1/login/sysLogout`
- **请求方式**: `POST`

## 请求参数

| 参数名 | 必选 | 类型 | 说明 |
| --- | --- | --- | --- |
| access_token | 是 | String | 调用接口凭证 获取accessToken信息 |
| userid | 否 | Long | 人员id 获取用户id 当type为userId时必填type |
| type | 是 | String | userId人员id,loginName登录名,jobNum工号,account账号,mobile电话,email邮箱 |
| account | shi | String | 账号 当type为非userId时必填 |

## 返回参数

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| code | String | 返回码 |
| msg | String | 返回信息 |
