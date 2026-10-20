# 根据id查询日程

- **文档 ID**: `908341242109050881`
- **业务模块**: 日程
- **是否 API 接口**: 是
- **请求 URL**: `{OpenApiOrigin}/api/calendar/openapi/v1/queryById`
- **Content-Type**: `application/json`

## 备注

- POSTContent-Type：application/json

## 请求参数

| 参数名 | 必选 | 类型 | 说明 |
| --- | --- | --- | --- |
| access_token | 是 | String | 调用接口凭证 获取accessToken信息 |
| id | 是 | Long | 日程id |
| userId | 是 | Long | 用户id 获取用户ID |

## 返回参数

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| id | String | 日程id |
| deleteType | Integer | 是否删除（0：否，1：是） |
| name | String | 日程名称 |
| creator | Object | 日程创建人 |
| createTime | Long | 日程创建时间 |
| commentCount | Integer | 日程评论条数 |
| watched | Boolean | 是否关注 |
| unread | Boolean | 是否未读 |
| finished | Boolean | 是否完成 |
| manager | Object | 日程负责人 |
| content | String | 日程详情 |
| startDate | Long | 日程开始时间 |
| endDate | Long | 日程结束时间 |
| allDay | Boolean | 是否全天（开启：true，关闭：false） |
| secret | String | 公开程度（normal：上级可见，self：仅自己可见，dept：本部门可见，all：公开） |
| repeat | Boolean | 是否重复日程 |
| priority | String | 日程紧急程度 |
| calendarStatus | String | 日程状态（todo:进行中，finished：已完成） |
| repeatNum | Integer | 周期日程重复次数 |
| placeType | String | 地点 |
| receiptSwitch | String | 参与人回执开关（开启：open，关闭：close） |
| calendarType | String | 日程类型 |
| signType | String | 日程签到（无：none，扫码签到：scan，定位签到：position） |
| errcode | String | 返回码 |
| errmsg | String | 返回信息 |
