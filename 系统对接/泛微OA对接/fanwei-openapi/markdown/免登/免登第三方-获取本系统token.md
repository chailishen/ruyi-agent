# 免登第三方-获取本系统token

- **文档 ID**: `840673581315399680`
- **业务模块**: 免登
- **是否 API 接口**: 否（说明文档）

## 备注

- 备注：

## 请求参数

| 参数名 | 必选 | 类型 | 说明 |
| --- | --- | --- | --- |
| app_key | 是 | string | 应用app_key |
| redirect_uri | 是 | string | 第三方系统接收身份令牌地址 |

## 返回参数

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| eteams_token | String | 三方系统的免登本系统令牌 |

## 正文

## 免登第三方-获取本系统token
#### 开放平台免登套件
详见：{origin}/sp/openapi/base/doc/kit/auth
简要描述：
- 用于从本系统免登到第三方业务系统
请求URL：
- {origin}/api/bs/open/auth/third?app_key=%s&redirect_uri=%s
备注：
此请求发起触发必须在本系统中进行，大家可通过构建应用或者菜单设置功能，添加url类型菜单指向该地址实现免登。
参数：
| 参数名 | 必选 | 类型 | 说明 |
| --- | --- | --- | --- |
| app_key | 是 | string | 应用app_key |
| redirect_uri | 是 | string | 第三方系统接收身份令牌地址 |
请求示例：
redirect示例
返回参数说明
| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| eteams_token | String | 三方系统的免登本系统令牌 |
