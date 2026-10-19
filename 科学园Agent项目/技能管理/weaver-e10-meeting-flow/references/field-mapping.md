# 字段映射（会议申请 · 雄安科学园 E10）

> 字段能力（必填/可见/选项）以 `form` 命令实时返回为准；本表是 2026-10-16 实测基线与入参对照。
> 所有 id 按字符串处理。

## prepare 入参 JSON 字段

| 入参键 | 必填 | 含义与取值 | 落到 operate 报文 |
|---|---|---|---|
| `name` | 是 | 会议名称（文本）。流程标题系统自动生成 `会议申请-{姓名}-{发起日期}`，不要自造 | `name` |
| `beginDatetime` | 是 | 开始时间，严格 `yyyy-MM-dd HH:mm` | `beginDatetime` |
| `endDatetime` | 是 | 结束时间，严格 `yyyy-MM-dd HH:mm`，必须晚于开始 | `endDatetime` |
| `room` | 是 | 会议室：全称/包含匹配名，或会议室 id（`address`/`roomId` 同义） | `address` |
| `members` | 否 | 参会**人员**数组：姓名（走 `/complete/resource` 解析）或 HRM id；逗号字符串也接受 | `hrmMembers`（逗号拼接） |
| `departments` | 否 | 参会**部门**数组：名称或部门 id | `orgMembers`（逗号拼接） |
| `otherMembers` | 否 | 其他人员，纯文本（外部来宾） | `otherMembers` |
| `mtDesc`（别名 `subject`） | 否 | 会议内容，多行文本 | `mtDesc` |
| `materials` | 否 | 会议物资（会议自定义表单 TextArea，走 saveFormData 的 dataDetails，**不进 operate**） | `dataDetails[].dataText.content` |
| `remind` | 否 | `true`/选项名/选项 id 数组；`true` 取实时第一项（当前=6 系统消息提醒）；false/缺省=不提醒 | `remindType`（如 `"6"`，落库回读为 `["6"]`） |
| `totalMember` | 否 | 应到人数（整数）；缺省 = 1 发起人 + 参会人数 + 参会部门数 | `totalMember`（int） |
| `caller` | 否 | 发起人 HRM id；缺省 = `form` 拿到的当前用户 | `caller` |

## 固定/自动字段（用户不输入）

`frequent:"0"`（永不，系统必填但脚本自动满足）、`crmMembers:""`、`crmTotalMember:0`、
`contacter:""`、`mtType:""`（会议类型当前 0 条）、`customizeAddress:""`、
提醒子项全 0（`remindImmediately/remindBeforeStart/remindBeforeEnd/remindToCreater/
remindHours*/remindTimes*`、`remindStartList/remindEndList`）、
周期默认项（`byDateType:0,count:0,finishAt:2,interval:1,until:开始日期,byDay/byMonth/
byMonthDay/byDayCount:""`）、中文标签（`NoLabel/eachLabel/weekLabel/monthLabel/
dayLabel/yearLabel/timesLabel/occurLabel/roomUsageLink`）、
`hasVideo:0,meetingStatus:0,serviceItems:"",mtAccessorys:"",sort:0,tenantKey:""`。

## 会议自定义表单（formId 动态 = createBaseData.EBFormId，实测 `1302787649769865266`）

- 18 个表单项（fieldId 段 `1302787649769865225–265`）随会议组件自动渲染，业务值由
  operate 接口承载，不需要脚本逐字段提交。
- 唯一需要走 saveFormData `dataDetails` 的自定义文本域：
  - **会议物资 hywz，fieldId `1302788014707867664`**（不在 PC 布局/getMeetingDetailField
    ADD 响应里，部署期实测，脚本内 `CUSTOM_TEXT_FIELDS.materials`）。
  - 提交形态：`{"formField":{"id":"1302788014707867664"},"dataText":{"content":"..."}}`。

## 名称解析接口（全部运行时动态，禁止硬编码选项 id）

| 用途 | 接口 | 体要点 | 取值 |
|---|---|---|---|
| 会议室 | POST `/api/meeting/roomUsage/getAllRoomUrl` | `{currentdate,bywhat:4,type:"day",mode:"my,other"}` | `data[].id/name`（实测 8 间） |
| 人员 | POST `/api/meeting/common/browser/complete/resource` | `{searchValue,newly:0,browserMultiple:false,showPartTime:true}` | `data.data[].id`=HRM id |
| 部门 | POST `/api/meeting/common/browser/complete/department` | `{searchValue,newly:0,browserMultiple:false}` | `data.data[].id/name` |
| 提醒选项 | `form` 响应 `items.remindType.options` | — | 唯一选项 id=6 内容=系统消息提醒 |

匹配规则：精确名称优先；包含匹配唯一命中才采用；多命中/零命中 → NEEDS_INPUT 并带候选。

## 两类 id 不要混

- HRM id（人员，如 sysadmin=`1248936314680606736`）：`members/caller/identityId/chk.hrmids` 用它；
  不是 userid（`8077399064530596909`）。
- 部门 id（财务资产组=`1255539887080341532`）：`orgMembers` 用它。
