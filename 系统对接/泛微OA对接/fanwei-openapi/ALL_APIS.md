# 泛微 Open API 全量索引

- 版本: `10.0.2026.0201.01`
- 同步时间: `2026-07-06T08:19:46.099734+00:00`
- 文档总数: 505
- API 接口数: 465
- 说明文档数: 34

## e-Builder

- [API] **获取数据总数（V2）** | `-` | `/api/ebuilder/form/dataset/v2/getAllDataCount` | [markdown](markdown/e-Builder/获取数据总数（V2）.md)
- [API] **新建表单数据（V2）** | `-` | `/api/ebuilder/form/dataset/v2/saveFormData` | [markdown](markdown/e-Builder/新建表单数据（V2）.md)
- [API] **修改表单数据（V2）** | `-` | `/api/ebuilder/form/dataset/v2/updateFormData` | [markdown](markdown/e-Builder/修改表单数据（V2）.md)
- [API] **删除表单数据（V2）** | `-` | `/api/ebuilder/form/dataset/v2/deleteData` | [markdown](markdown/e-Builder/删除表单数据（V2）.md)
- [API] **获取数据详情（V2）** | `-` | `/api/ebuilder/form/dataset/v2/getDataById` | [markdown](markdown/e-Builder/获取数据详情（V2）.md)
- [API] **获取分页数据（V2）** | `-` | `/api/ebuilder/form/dataset/v2/getAllData` | [markdown](markdown/e-Builder/获取分页数据（V2）.md)
- [API] **根据数据ID获取表单数据** | `POST` | `/api/ebuilder/form/dataset/v1/getDataById` | [markdown](markdown/e-Builder/根据数据ID获取表单数据.md)
- [API] **获取分页数据** | `POST` | `/api/ebuilder/form/dataset/v1/getAllData` | [markdown](markdown/e-Builder/获取分页数据.md)
- [API] **表单数据删除** | `POST` | `/api/ebuilder/form/dataset/v1/deleteData` | [markdown](markdown/e-Builder/表单数据删除.md)
- [API] **表单数据保存** | `POST` | `/api/ebuilder/form/dataset/v1/saveFormData` | [markdown](markdown/e-Builder/表单数据保存.md)
- [API] **获取表单数据总数** | `POST` | `/api/ebuilder/form/dataset/v1/getAllDataCount` | [markdown](markdown/e-Builder/获取表单数据总数.md)
- [API] **获取表格基本信息** | `POST` | `/api/ebuilder/form/formcfg/list/v1/listInit` | [markdown](markdown/e-Builder/获取表格基本信息.md)
- [API] **获取表格查看权限** | `POST` | `/api/ebuilder/form/formcfg/list/permission/v1/getList` | [markdown](markdown/e-Builder/获取表格查看权限.md)
- [API] **获取表格显示字段** | `POST` | `/api/ebuilder/form/formcfg/list/v1/getListDatas` | [markdown](markdown/e-Builder/获取表格显示字段.md)
- [API] **获取表格筛选条件** | `POST` | `/api/ebuilder/form/formcfg/list/listFilter/v1/getSearchFilters` | [markdown](markdown/e-Builder/获取表格筛选条件.md)
- [API] **获取表单字段信息** | `POST` | `/api/ebuilder/form/dataset/v1/getFields` | [markdown](markdown/e-Builder/获取表单字段信息.md)
- [API] **数据权限校验** | `POST` | `/api/ebuilder/form/dataset/v1/getDetail` | [markdown](markdown/e-Builder/数据权限校验.md)
- [API] **获取组件配置** | `GET` | `/api/ebuilder/coms/common/getConfig` | [markdown](markdown/e-Builder/获取组件配置.md)
- [API] **获取列表数据** | `POST` | `/api/ebuilder/coms/list/getData` | [markdown](markdown/e-Builder/获取列表数据.md)
- [API] **获取幻灯片数据** | `POST` | `/api/ebuilder/coms/slide/getData` | [markdown](markdown/e-Builder/获取幻灯片数据.md)
- [API] **获取图表数据** | `POST` | `/api/ebuilder/coms/chart/getData` | [markdown](markdown/e-Builder/获取图表数据.md)
- [API] **获取导航菜单数据** | `POST` | `/api/ebuilder/coms/navmenu/getData` | [markdown](markdown/e-Builder/获取导航菜单数据.md)

## 业务表单

- [API] **新增表单数据** | `POST` | `/form/v2/create` | [markdown](markdown/业务表单/新增表单数据.md)
- [API] **根据dataKey字段创建数据** | `POST` | `/api/formdatareport/v2/createDataReportByDataKey` | [markdown](markdown/业务表单/根据dataKey字段创建数据.md)
- [API] **创建上报V3** | `POST` | `/form/v3/createDataReportByIdVal` | [markdown](markdown/业务表单/创建上报V3.md)
- [API] **删除表单数据** | `POST` | `/form/v2/delete` | [markdown](markdown/业务表单/删除表单数据.md)
- [API] **更新表单数据** | `POST` | `/form/v2/update` | [markdown](markdown/业务表单/更新表单数据.md)
- [API] **回退表单数据** | `POST` | `/form/v2/back` | [markdown](markdown/业务表单/回退表单数据.md)
- [API] **查询表单分类** | `GET` | `/form/v2/classify` | [markdown](markdown/业务表单/查询表单分类.md)
- [API] **根据分类ID查询表单** | `GET` | `/form/v2/getFormByCategoryId` | [markdown](markdown/业务表单/根据分类ID查询表单.md)
- [API] **根据表单ID查询字段** | `GET` | `/form/v2/getFieldById` | [markdown](markdown/业务表单/根据表单ID查询字段.md)
- [API] **根据表单ID查询表单数据** | `GET` | `/form/v2/getInfoByID` | [markdown](markdown/业务表单/根据表单ID查询表单数据.md)
- [API] **根据表单数据ID查询表单数据（V2）** | `GET` | `/form/v2/queryDataReportById` | [markdown](markdown/业务表单/根据表单数据ID查询表单数据（V2）.md)
- [API] **根据表单数据ID查询表单数据-可返回字段id值（V3）** | `GET` | `/form/v3/queryDataReportById` | [markdown](markdown/业务表单/根据表单数据ID查询表单数据-可返回字段id值（V3）.md)
- [API] **根据人员ID查询待办上报数据** | `GET` | `/form/v2/getTodoData` | [markdown](markdown/业务表单/根据人员ID查询待办上报数据.md)
- [API] **根据人员ID查询已完成上报数据** | `GET` | `/form/v2/getFinfishData` | [markdown](markdown/业务表单/根据人员ID查询已完成上报数据.md)
- [API] **表单支持动态参数查询** | `GET` | `/form/v2/getInfoByIDAndParam` | [markdown](markdown/业务表单/表单支持动态参数查询.md)
- [API] **表单支持动态参数查询（新）** | `POST` | `/form/v2/getDataInfoByIDAndParam` | [markdown](markdown/业务表单/表单支持动态参数查询（新）.md)
- [API] **根据表单id查询时间区间内的增、删、改数据** | `GET` | `/form/v2/queryChangedReportsByFormId` | [markdown](markdown/业务表单/根据表单id查询时间区间内的增、删、改数据.md)
- [API] **根据表单id和单个类型查询时间范围内上报数据** | `GET` | `/form/v2/queryChangedReportsByType` | [markdown](markdown/业务表单/根据表单id和单个类型查询时间范围内上报数据.md)
- [API] **查询时间范围内所有的增删改表单信息** | `GET` | `/form/v2/queryChangedForms` | [markdown](markdown/业务表单/查询时间范围内所有的增删改表单信息.md)
- [API] **根据单个类型查询时间范围内的表单信息** | `GET` | `/form/v2/queryChangedFormsByType` | [markdown](markdown/业务表单/根据单个类型查询时间范围内的表单信息.md)
- [API] **新增表单数据dataJson** | `POST` | `/form/v2/createDataReportByJson` | [markdown](markdown/业务表单/新增表单数据dataJson.md)
- [API] **查询选项字段值** | `GET` | `/api/formdatareport/v2/getFieldOption` | [markdown](markdown/业务表单/查询选项字段值.md)

## 云桥

- [API] **获取第三方APP的accessToken** | `GET` | `/api/eb/open/thirdapi/v1/getAccessToken` | [markdown](markdown/云桥/获取第三方APP的accessToken.md)
- [API] **添加用户绑定关系** | `POST` | `/api/eb/open/hrm/v1/bindUser` | [markdown](markdown/云桥/添加用户绑定关系.md)
- [API] **删除用户绑定关系** | `POST` | `/api/eb/open/hrm/v1/unBindUser` | [markdown](markdown/云桥/删除用户绑定关系.md)
- [API] **根据oa用户id获取第三方用户信息** | `GET` | `/api/eb/open/hrm/v1/getThirdUserByOaEmployeeId` | [markdown](markdown/云桥/根据oa用户id获取第三方用户信息.md)
- [API] **根据oa用户id列表获取第三方用户信息列表** | `POST` | `/api/eb/open/hrm/v1/getThirdUserListByOaEmployeeIdList` | [markdown](markdown/云桥/根据oa用户id列表获取第三方用户信息列表.md)
- [API] **根据第三方用户id获取oa用户id** | `GET` | `/api/eb/open/hrm/v1/getEmployeeIdByThirdUserId` | [markdown](markdown/云桥/根据第三方用户id获取oa用户id.md)
- [API] **根据第三方用户id获取oa用户信息** | `GET` | `/api/eb/open/hrm/v1/getThirdUserByOaEmployeeId` | [markdown](markdown/云桥/根据第三方用户id获取oa用户信息.md)

## 产品

- [API] **新增产品** | `POST` | `/crm/v2/create` | [markdown](markdown/产品/新增产品.md)
- [API] **修改产品** | `POST` | `/crm/v2/update` | [markdown](markdown/产品/修改产品.md)
- [API] **删除产品** | `POST` | `/crm/v2/delete` | [markdown](markdown/产品/删除产品.md)
- [API] **查询产品** | `GET` | `/crm/v2/get` | [markdown](markdown/产品/查询产品.md)
- [API] **搜索产品** | `GET` | `/crm/v2/search` | [markdown](markdown/产品/搜索产品.md)
- [API] **产品获取自定义表单** | `GET` | `/crm/v2/getCustomForms` | [markdown](markdown/产品/产品获取自定义表单.md)
- [API] **产品获取自定义表单字段** | `GET` | `/crm/v2/getCustomFields` | [markdown](markdown/产品/产品获取自定义表单字段.md)

## 人事档案

- [API] **人员编制-同步预减** | `POST` | `/api/hr/hrapi/est/savePreSub` | [markdown](markdown/人事档案/人员编制-同步预减.md)
- [API] **人员编制-编制校验** | `POST` | `/api/hr/hrapi/est/validate` | [markdown](markdown/人事档案/人员编制-编制校验.md)

## 人员

- [API] **同步人员** | `POST` | `/api/hrm/restful/syncEmployee` | [markdown](markdown/人员/同步人员.md)
- [API] **查询人员-高级搜索** | `POST` | `/api/hrm/restful/queryEmployee` | [markdown](markdown/人员/查询人员-高级搜索.md)
- [API] **人员返聘** | `POST` | `/api/hrm/restful/rehireEmployee` | [markdown](markdown/人员/人员返聘.md)
- [API] **新增人员** | `POST` | `/user/v3/createUser` | [markdown](markdown/人员/新增人员.md)
- [API] **新增人员（V4）** | `POST` | `/user/v4/createUser` | [markdown](markdown/人员/新增人员（V4）.md)
- [API] **修改人员（V3）** | `POST` | `/user/v3/updateUser` | [markdown](markdown/人员/修改人员（V3）.md)
- [API] **修改人员（V2）** | `POST` | `/user/v2/updateUser` | [markdown](markdown/人员/修改人员（V2）.md)
- [API] **离职人员** | `POST` | `/user/v2/delete` | [markdown](markdown/人员/离职人员.md)
- [API] **查询人员** | `GET` | `/user/v3/findUser` | [markdown](markdown/人员/查询人员.md)
- [API] **查询所有人员** | `GET` | `/user/v3/findAllUsers` | [markdown](markdown/人员/查询所有人员.md)
- [API] **获取成员信息** | `GET` | `/user/v3/get` | [markdown](markdown/人员/获取成员信息.md)
- [API] **获取部门成员信息** | `GET` | `/user/v3/departmentUsers` | [markdown](markdown/人员/获取部门成员信息.md)
- [API] **按更新时间查询人员信息** | `GET` | `/user/v3/findUpdateUser` | [markdown](markdown/人员/按更新时间查询人员信息.md)
- [DOC] **同步条件矩阵数据** | `POST` | `-` | [markdown](markdown/人员/同步条件矩阵数据.md)
- [API] **查询人事档案自定义字段（V4）** | `GET` | `/user/v4/queryUserInfoFields` | [markdown](markdown/人员/查询人事档案自定义字段（V4）.md)
- [API] **查询所有彻底删除人员id接口（V3）** | `GET` | `/user/v3/findAllPermanentlyDeleteUsers` | [markdown](markdown/人员/查询所有彻底删除人员id接口（V3）.md)
- [API] **根据企业微信ID查找人员（V3）** | `GET` | `/user/v3/findUserByWechatUserId` | [markdown](markdown/人员/根据企业微信ID查找人员（V3）.md)

## 任务

- [API] **新增任务** | `POST` | `/task/v2/create` | [markdown](markdown/任务/新增任务.md)
- [API] **删除任务** | `POST` | `/task/v2/delete` | [markdown](markdown/任务/删除任务.md)
- [API] **修改任务** | `POST` | `/task/v2/update` | [markdown](markdown/任务/修改任务.md)
- [API] **查询任务** | `GET` | `/task/v2/info` | [markdown](markdown/任务/查询任务.md)
- [API] **查询团队任务** | `POST` | `/task/v2/queryTasks` | [markdown](markdown/任务/查询团队任务.md)
- [API] **查询我的任务** | `POST` | `/task/v2/mineInfo` | [markdown](markdown/任务/查询我的任务.md)
- [API] **查询任务类型** | `GET` | `/task/v2/queryTaskTypes` | [markdown](markdown/任务/查询任务类型.md)
- [API] **根据任务类型ID查询自定义字段** | `GET` | `/task/v2/queryFormInfoByTaskType` | [markdown](markdown/任务/根据任务类型ID查询自定义字段.md)
- [API] **根据更新时间查询团队任务** | `POST` | `/task/v2/queryUpdateTasks` | [markdown](markdown/任务/根据更新时间查询团队任务.md)
- [API] **查询团队实际工时** | `POST` | `/task/v2/queryRealWorkingTimes` | [markdown](markdown/任务/查询团队实际工时.md)
- [API] **新增填报工时** | `POST` | `/task/v2/fillRealWorkingTimes` | [markdown](markdown/任务/新增填报工时.md)
- [API] **修改填报工时** | `POST` | `/task/v2/updateRealWorkingTimes` | [markdown](markdown/任务/修改填报工时.md)
- [API] **删除工时** | `POST` | `/task/v2/deleteRealWorkingTimes` | [markdown](markdown/任务/删除工时.md)
- [API] **任务新建接口（支持批量）** | `POST` | `/api/task/v3/create` | [markdown](markdown/任务/任务新建接口（支持批量）.md)
- [API] **任务更新接口（支持批量）** | `POST` | `/api/task/v3/update` | [markdown](markdown/任务/任务更新接口（支持批量）.md)
- [API] **任务可变更状态列表查询接口（支持批量）** | `POST` | `/api/task/v3/status/changeableList` | [markdown](markdown/任务/任务可变更状态列表查询接口（支持批量）.md)

## 会议管理

- [API] **会议室使用情况（V2）** | `-` | `/api/meeting/meetingOpenApi/getRoomUsageEvents` | [markdown](markdown/会议管理/会议室使用情况（V2）.md)
- [API] **查询会议室(V2)** | `-` | `/sapi/meeting/meetingOpenApi/getMeetingRooms` | [markdown](markdown/会议管理/查询会议室(V2).md)
- [API] **获取二维码** | `-` | `/api/meeting/meetingOpenApi/getQrcode` | [markdown](markdown/会议管理/获取二维码.md)
- [API] **下载二维码** | `-` | `/api/meeting/meetingOpenApi/downLoadOrcode` | [markdown](markdown/会议管理/下载二维码.md)
- [API] **新建会议室** | `POST` | `/room/v2/createRoom` | [markdown](markdown/会议管理/新建会议室.md)
- [API] **编辑会议室** | `POST` | `/room/v2/updateRoom` | [markdown](markdown/会议管理/编辑会议室.md)
- [API] **删除会议室** | `POST` | `/room/v2/softDeleteRoom` | [markdown](markdown/会议管理/删除会议室.md)
- [API] **查询会议室** | `POST` | `/room/v2/queryRooms` | [markdown](markdown/会议管理/查询会议室.md)
- [API] **会议室使用情况** | `POST` | `/room/v2/queryEvents` | [markdown](markdown/会议管理/会议室使用情况.md)
- [API] **新建会议** | `-` | `/api/meeting/meetingOpenApi/addMeeting` | [markdown](markdown/会议管理/新建会议.md)
- [API] **获取门户最新会议** | `-` | `/api/meeting/meetingOpenApi/getGatewayNewMeetingPortal` | [markdown](markdown/会议管理/获取门户最新会议.md)
- [API] **查询会议列表** | `-` | `/api/meeting/meetingOpenApi/getMeetingInfoList` | [markdown](markdown/会议管理/查询会议列表.md)
- [API] **变更会议** | `-` | `/api/meeting/meetingOpenApi/changeMeeting` | [markdown](markdown/会议管理/变更会议.md)
- [API] **取消会议** | `-` | `/api/meeting/meetingOpenApi/cancelMeeting` | [markdown](markdown/会议管理/取消会议.md)
- [API] **会议室冲突检测** | `-` | `/api/meeting/meetingOpenApi/meetingChkRoom` | [markdown](markdown/会议管理/会议室冲突检测.md)
- [API] **智能推荐会议室** | `POST` | `/api/meeting/meetingOpenApi/getRecommendRoomEvents` | [markdown](markdown/会议管理/智能推荐会议室.md)

## 免登

- [API] **免登本系统-获取本系统令牌** | `POST` | `/oauth2/get_logintoken` | [markdown](markdown/免登/免登本系统-获取本系统令牌.md)
- [DOC] **免登第三方-获取本系统token** | `-` | `-` | [markdown](markdown/免登/免登第三方-获取本系统token.md)
- [API] **免登第三方-根据本系统token查询用户** | `POST` | `/oauth2/getUserInfo` | [markdown](markdown/免登/免登第三方-根据本系统token查询用户.md)

## 全文搜索

- [API] **全文检索接口** | `POST` | `/api/esearch/search/fullsearch/searchByModule` | [markdown](markdown/全文搜索/全文检索接口.md)
- [API] **获取微搜模块基础信息** | `POST` | `/api/esearch/search/xiaoe/getBaseInfoForXE` | [markdown](markdown/全文搜索/获取微搜模块基础信息.md)
- [API] **获取微搜配置信息** | `POST` | `/api/esearch/search/xiaoe/getSearchSetForXE` | [markdown](markdown/全文搜索/获取微搜配置信息.md)
- [API] **获取关键词补全** | `POST` | `/api/esearch/search/xiaoe/querySuggestForXE` | [markdown](markdown/全文搜索/获取关键词补全.md)
- [API] **根据ID获取数据** | `POST` | `/api/esearch/search/xiaoe/queryByIdsForXE` | [markdown](markdown/全文搜索/根据ID获取数据.md)

## 公文管理

- [API] **获取公文列表数据** | `POST` | `/api/odoc/list/getCustomlistData` | [markdown](markdown/公文管理/获取公文列表数据.md)

## 其它

- [DOC] **datamap传值说明** | `-` | `-` | [markdown](markdown/其它/datamap传值说明.md)
- [DOC] **表单查询datamap传值说明** | `-` | `-` | [markdown](markdown/其它/表单查询datamap传值说明.md)
- [DOC] **dataJson传值说明** | `-` | `-` | [markdown](markdown/其它/dataJson传值说明.md)
- [DOC] **errcode说明** | `-` | `-` | [markdown](markdown/其它/errcode说明.md)
- [DOC] **表单dataDetails（V3）返回值说明** | `-` | `-` | [markdown](markdown/其它/表单dataDetails（V3）返回值说明.md)
- [DOC] **表单dataDetails（V3）明细表返回值说明** | `-` | `-` | [markdown](markdown/其它/表单dataDetails（V3）明细表返回值说明.md)
- [DOC] **更新记录** | `-` | `-` | [markdown](markdown/其它/更新记录.md)

## 发票

- [DOC] **432007274223894528** | `POST` | `-` | [markdown](markdown/发票/432007274223894528.md)

## 合同管理

- [API] **模板创建** | `POST` | `/api/ebd/contract/tplinfo/openAPI/v1/save` | [markdown](markdown/合同管理/模板创建.md)
- [API] **模板基础信息修改** | `POST` | `/api/ebd/contract/tplinfo/openAPI/v1/update` | [markdown](markdown/合同管理/模板基础信息修改.md)
- [API] **模板详情信息（书签）修改** | `POST` | `/api/ebd/contract/tplinfo/openAPI/v1/saveFileData` | [markdown](markdown/合同管理/模板详情信息（书签）修改.md)
- [API] **模板详情信息** | `GET` | `/api/ebd/contract/tplinfo/openAPI/v1/getFileData` | [markdown](markdown/合同管理/模板详情信息.md)
- [API] **模板列表查询** | `GET` | `/api/contract/jxhs/openApi/template/getTemplate` | [markdown](markdown/合同管理/模板列表查询.md)
- [API] **生成模板套用** | `POST` | `/api/contract/jxhs/openApi/template/replaceTemplate` | [markdown](markdown/合同管理/生成模板套用.md)
- [DOC] **合同流程发起执行模板套用** | `-` | `-` | [markdown](markdown/合同管理/合同流程发起执行模板套用.md)

## 商机

- [API] **新增商机** | `POST` | `/crm/v2/create` | [markdown](markdown/商机/新增商机.md)
- [DOC] **商机新增评论** | `POST` | `-` | [markdown](markdown/商机/商机新增评论.md)
- [API] **修改商机** | `POST` | `/crm/v2/update` | [markdown](markdown/商机/修改商机.md)
- [API] **删除商机** | `POST` | `/crm/v2/delete` | [markdown](markdown/商机/删除商机.md)
- [API] **查询商机** | `GET` | `/crm/v2/get` | [markdown](markdown/商机/查询商机.md)

## 国际化

- [API] **获取所有币种** | `POST` | `/api/i18n/currency/v1/getAllCurrencies` | [markdown](markdown/国际化/获取所有币种.md)
- [API] **获取已启用币种** | `POST` | `/api/i18n/currency/v1/getEnabledCurrencies` | [markdown](markdown/国际化/获取已启用币种.md)
- [API] **获取本位币** | `POST` | `/api/i18n/currency/v1/getBaseCurrency` | [markdown](markdown/国际化/获取本位币.md)
- [API] **根据币符或者币种id获取币种** | `POST` | `/api/i18n/currency/v1/getCurrency` | [markdown](markdown/国际化/根据币符或者币种id获取币种.md)
- [API] **获取实时汇率** | `POST` | `/api/i18n/rate/v1/getCurrentFXRate` | [markdown](markdown/国际化/获取实时汇率.md)
- [API] **获取期间汇率** | `POST` | `/api/i18n/rate/v1/getPeriodFXRate` | [markdown](markdown/国际化/获取期间汇率.md)
- [API] **获取指定日期汇率** | `POST` | `/api/i18n/rate/v1/getTargetDateFXRate` | [markdown](markdown/国际化/获取指定日期汇率.md)

## 基础架构

- [API] **账号密码校验** | `POST` | `/api/basicserver/v1/logincheck/checkAccount` | [markdown](markdown/基础架构/账号密码校验.md)
- [API] **pc端退出登录** | `POST` | `/api/basicserver/v1/login/sysLogout` | [markdown](markdown/基础架构/pc端退出登录.md)
- [API] **移动端退出登录** | `POST` | `/api/basicserver/open/mobileOffline` | [markdown](markdown/基础架构/移动端退出登录.md)
- [API] **获取团队人员账号信息** | `-` | `/api/basicserver/v1/login/findAccount` | [markdown](markdown/基础架构/获取团队人员账号信息.md)

## 客户

- [API] **新增客户** | `POST` | `/crm/v2/create` | [markdown](markdown/客户/新增客户.md)
- [API] **删除客户** | `POST` | `/crm/v2/delete` | [markdown](markdown/客户/删除客户.md)
- [API] **修改客户** | `POST` | `/crm/v2/update` | [markdown](markdown/客户/修改客户.md)
- [API] **查询客户** | `GET` | `/crm/v2/get` | [markdown](markdown/客户/查询客户.md)
- [API] **搜索客户** | `GET` | `/crm/v2/search` | [markdown](markdown/客户/搜索客户.md)

## 对接说明

- [DOC] **对接说明** | `-` | `-` | [markdown](markdown/对接说明/对接说明.md)
- [DOC] **开发者认证** | `-` | `-` | [markdown](markdown/对接说明/开发者认证.md)
- [DOC] **创建应用** | `-` | `-` | [markdown](markdown/对接说明/创建应用.md)
- [DOC] **对接示例** | `-` | `-` | [markdown](markdown/对接说明/对接示例.md)
- [DOC] **开放平台sdk使用指南** | `-` | `-` | [markdown](markdown/对接说明/开放平台sdk使用指南.md)
- [API] **开放平台几种认证方式使用说明** | `GET` | `/user/v3/findAllUsers` | [markdown](markdown/对接说明/开放平台几种认证方式使用说明.md)
- [DOC] **接口数据加解密场景** | `-` | `-` | [markdown](markdown/对接说明/接口数据加解密场景.md)
- [DOC] **接口人员信息转换使用说明** | `-` | `-` | [markdown](markdown/对接说明/接口人员信息转换使用说明.md)
- [DOC] **认证参数的多种传递方式** | `-` | `-` | [markdown](markdown/对接说明/认证参数的多种传递方式.md)
- [DOC] **接口发布使用说明** | `-` | `-` | [markdown](markdown/对接说明/接口发布使用说明.md)

## 岗位

- [API] **查询岗位列表（V2）** | `GET` | `/position/v2/list` | [markdown](markdown/岗位/查询岗位列表（V2）.md)
- [API] **同步岗位** | `POST` | `/api/hrm/restful/syncPosition` | [markdown](markdown/岗位/同步岗位.md)

## 工作流程

- [API] **新增流程** | `POST` | `/api/workflow/core/paService/v1/doCreateRequest` | [markdown](markdown/工作流程/新增流程.md)
- [API] **获取流程状态列表数据** | `-` | `/api/workflow/core/paService/v1/getRequestStatusData` | [markdown](markdown/工作流程/获取流程状态列表数据.md)
- [API] **获取流程状态列表数据统计** | `-` | `/api/workflow/core/paService/v1/getRequestStatusDataCount` | [markdown](markdown/工作流程/获取流程状态列表数据统计.md)
- [API] **创建流程实例** | `POST` | `/api/workflow/core/paService/v2/doCreateRequest` | [markdown](markdown/工作流程/创建流程实例.md)
- [API] **查询工作流信息** | `POST` | `/api/workflow/pathdef/openapi/getBaseInfoByCondition` | [markdown](markdown/工作流程/查询工作流信息.md)
- [API] **查询工作流节点信息** | `POST` | `/api/workflow/pathdef/openapi/getNodeInfoByCondition` | [markdown](markdown/工作流程/查询工作流节点信息.md)
- [API] **查询工作流所有版本** | `POST` | `/api/workflow/pathdef/openapi/getAllVersionWfId` | [markdown](markdown/工作流程/查询工作流所有版本.md)
- [API] **查询工作流活动版本** | `POST` | `/api/workflow/pathdef/openapi/getActiveWfId` | [markdown](markdown/工作流程/查询工作流活动版本.md)
- [API] **查询工作流关联的表单信息** | `POST` | `/api/workflow/pathdef/openapi/getFormInfo` | [markdown](markdown/工作流程/查询工作流关联的表单信息.md)
- [API] **查询工作流类型** | `GET` | `/workflow/v2/classify` | [markdown](markdown/工作流程/查询工作流类型.md)
- [API] **创建表单或者修改表单字段** | `-` | `/api/workflow/core/paService/v1/batchSaveFormFieldManage` | [markdown](markdown/工作流程/创建表单或者修改表单字段.md)
- [API] **新建工作流** | `POST` | `/api/workflow/pathdef/openapi/createPath` | [markdown](markdown/工作流程/新建工作流.md)
- [API] **根据工作流类型查询工作流和表单** | `GET` | `/workflow/v2/getFormByCategoryId` | [markdown](markdown/工作流程/根据工作流类型查询工作流和表单.md)
- [API] **根据表单ID查询字段** | `GET` | `/workflow/v2/getFieldById` | [markdown](markdown/工作流程/根据表单ID查询字段.md)
- [API] **查询时间段内新增、更新、删除的工作流列表** | `POST` | `/workflow/v2/queryChangedFormsByType` | [markdown](markdown/工作流程/查询时间段内新增、更新、删除的工作流列表.md)
- [API] **查询时间段内新增、更新、删除三种类型的的工作流列表** | `POST` | `/workflow/v2/queryChangedFormsAllType` | [markdown](markdown/工作流程/查询时间段内新增、更新、删除三种类型的的工作流列表.md)
- [API] **根据表单ID列表查询表单字段** | `POST` | `/workflow/v2/queryFormFieldByFormIds` | [markdown](markdown/工作流程/根据表单ID列表查询表单字段.md)
- [API] **提交/同意流程** | `POST` | `/api/workflow/core/paService/v1/submitRequest` | [markdown](markdown/工作流程/提交-同意流程.md)
- [API] **删除流程** | `POST` | `/api/workflow/core/paService/v1/deleteRequest` | [markdown](markdown/工作流程/删除流程.md)
- [API] **根据流程表单ID获取流程左侧菜单全部数据下的所有相关数据** | `GET` | `/workflow/v2/getAllById` | [markdown](markdown/工作流程/根据流程表单ID获取流程左侧菜单全部数据下的所有相关数据.md)
- [API] **根据人员ID查询待办审批数据** | `GET` | `/workflow/v2/getTodoData` | [markdown](markdown/工作流程/根据人员ID查询待办审批数据.md)
- [API] **根据人员ID查询已办审批数据** | `GET` | `/workflow/v2/getFinfishData` | [markdown](markdown/工作流程/根据人员ID查询已办审批数据.md)
- [API] **流程统计筛选接口** | `POST` | `/workflow/v2/queryStatFormDatasForFlow` | [markdown](markdown/工作流程/流程统计筛选接口.md)
- [API] **查询时间段内新增、更新、删除的流程数据列表** | `POST` | `/workflow/v2/queryChangedFlowsByType` | [markdown](markdown/工作流程/查询时间段内新增、更新、删除的流程数据列表.md)
- [API] **查询时间段内新增、更新、删除三种类型的流程数据列表** | `POST` | `/workflow/v2/queryChangedFlowsAllType` | [markdown](markdown/工作流程/查询时间段内新增、更新、删除三种类型的流程数据列表.md)
- [API] **根据多个流程ID查询多份流程数据** | `POST` | `/workflow/v2/queryFlowInfoByFlowIds` | [markdown](markdown/工作流程/根据多个流程ID查询多份流程数据.md)
- [API] **根据流程表ID列表查询数据，分页返回** | `POST` | `/workflow/v2/queryStatFlowByFormIds` | [markdown](markdown/工作流程/根据流程表ID列表查询数据，分页返回.md)
- [API] **根据人员ID列表查询待办流程数据** | `POST` | `/workflow/v2/queryFlowTodoByUsers` | [markdown](markdown/工作流程/根据人员ID列表查询待办流程数据.md)
- [API] **根据人员ID列表查询已办流程数据** | `POST` | `/workflow/v2/queryFlowFinishedByUsers` | [markdown](markdown/工作流程/根据人员ID列表查询已办流程数据.md)
- [API] **根据类型统计总数（待办、已办、我提交）** | `POST` | `/workflow/v2/queryStatCountByType` | [markdown](markdown/工作流程/根据类型统计总数（待办、已办、我提交）.md)
- [API] **查询待办、已办、我提交类型统计总数** | `POST` | `/workflow/v2/queryStatCountAllType` | [markdown](markdown/工作流程/查询待办、已办、我提交类型统计总数.md)
- [API] **撤回流程** | `POST` | `/api/workflow/core/paService/v1/withdrawRequest` | [markdown](markdown/工作流程/撤回流程.md)
- [API] **退回流程** | `POST` | `/api/workflow/core/paService/v1/rejectRequest` | [markdown](markdown/工作流程/退回流程.md)
- [API] **所有流程数量** | `-` | `/api/workflow/list/paService/v1/getAllWorkflowRequestCount` | [markdown](markdown/工作流程/所有流程数量.md)
- [API] **所有流程列表** | `-` | `/api/workflow/list/paService/v1/getAllWorkflowRequestList` | [markdown](markdown/工作流程/所有流程列表.md)
- [API] **待办流程数量** | `-` | `/api/workflow/list/paService/v1/getToDoWorkflowRequestCount` | [markdown](markdown/工作流程/待办流程数量.md)
- [API] **待办流程列表** | `-` | `/api/workflow/list/paService/v1/getToDoWorkflowRequestList` | [markdown](markdown/工作流程/待办流程列表.md)
- [API] **已办流程数量** | `-` | `/api/workflow/list/paService/v1/getHandledWorkflowRequestCount` | [markdown](markdown/工作流程/已办流程数量.md)
- [API] **已办流程列表** | `-` | `/api/workflow/list/paService/v1/getHandledWorkflowRequestList` | [markdown](markdown/工作流程/已办流程列表.md)
- [API] **我发起的流程数量** | `-` | `/api/workflow/list/paService/v1/getMyWorkflowRequestCount` | [markdown](markdown/工作流程/我发起的流程数量.md)
- [API] **我发起的流程列表** | `-` | `/api/workflow/list/paService/v1/getMyWorkflowRequestList` | [markdown](markdown/工作流程/我发起的流程列表.md)
- [API] **用户前台可发起工作流程数量** | `-` | `/api/workflow/list/paService/v1/getCreateWorkflowCount` | [markdown](markdown/工作流程/用户前台可发起工作流程数量.md)
- [API] **前台可发起工作流列表** | `-` | `/api/workflow/list/paService/v1/getCreateWorkflowList` | [markdown](markdown/工作流程/前台可发起工作流列表.md)
- [API] **强制收回流程** | `POST` | `/api/workflow/core/paService/v1/doForceDrawBack` | [markdown](markdown/工作流程/强制收回流程.md)
- [API] **强制结束流程** | `POST` | `/api/workflow/core/paService/v1/doForceOver` | [markdown](markdown/工作流程/强制结束流程.md)
- [API] **干预流程** | `POST` | `/api/workflow/core/paService/v1/doIntervenor` | [markdown](markdown/工作流程/干预流程.md)
- [API] **保存流程签字意见** | `POST` | `/api/workflow/core/paService/v1/saveRequestLog` | [markdown](markdown/工作流程/保存流程签字意见.md)
- [DOC] **其他列表接口** | `POST` | `-` | [markdown](markdown/工作流程/其他列表接口.md)
- [API] **根据流程表单ID获取流程左侧菜单全部数据下的所有相关数据（支持高级搜索）** | `GET` | `/workflow/v3/getAllById` | [markdown](markdown/工作流程/根据流程表单ID获取流程左侧菜单全部数据下的所有相关数据（支持高级搜索）.md)
- [API] **根据人员id获取监控列表数据** | `POST` | `/api/workflow/list/paService/v1/getMonitorWorkflowRequestList` | [markdown](markdown/工作流程/根据人员id获取监控列表数据.md)
- [API] **根据人员id获取监控列表数量** | `POST` | `/api/workflow/list/paService/v1/getMonitorWorkflowRequestCount` | [markdown](markdown/工作流程/根据人员id获取监控列表数量.md)
- [API] **动态加签** | `-` | `/api/workflow/core/paService/v1/dynamicCreateFreeNode` | [markdown](markdown/工作流程/动态加签.md)
- [API] **转办** | `-` | `/api/workflow/core/paService/v1/doTurnTodo` | [markdown](markdown/工作流程/转办.md)
- [API] **催办** | `-` | `/api/workflow/core/paService/v1/requestSupervise` | [markdown](markdown/工作流程/催办.md)
- [API] **委托** | `-` | `/api/workflow/core/paService/v1/manualAgentRequest` | [markdown](markdown/工作流程/委托.md)
- [API] **意见征询** | `-` | `/api/workflow/core/paService/v1/consul` | [markdown](markdown/工作流程/意见征询.md)
- [API] **传阅** | `-` | `/api/workflow/core/paService/v1/circulate` | [markdown](markdown/工作流程/传阅.md)
- [API] **转发** | `-` | `/api/workflow/core/paService/v1/forward` | [markdown](markdown/工作流程/转发.md)
- [API] **抄送** | `-` | `/api/workflow/core/paService/v1/manualCC` | [markdown](markdown/工作流程/抄送.md)
- [API] **转发收回** | `-` | `/api/workflow/core/paService/v1/doForwardBack` | [markdown](markdown/工作流程/转发收回.md)
- [API] **传阅收回** | `-` | `/api/workflow/core/paService/v1/doCirculateBack` | [markdown](markdown/工作流程/传阅收回.md)
- [API] **退回申请** | `-` | `/api/workflow/core/paService/v1/rejectApply` | [markdown](markdown/工作流程/退回申请.md)
- [API] **拒绝退回申请** | `-` | `/api/workflow/core/paService/v1/refuseRejectApply` | [markdown](markdown/工作流程/拒绝退回申请.md)
- [API] **同意退回申请** | `-` | `/api/workflow/core/paService/v1/agreeRejectApply` | [markdown](markdown/工作流程/同意退回申请.md)
- [API] **征询结束** | `-` | `/api/workflow/core/paService/v1/consulOver` | [markdown](markdown/工作流程/征询结束.md)
- [API] **征询收回** | `-` | `/api/workflow/core/paService/v1/consulBack` | [markdown](markdown/工作流程/征询收回.md)
- [API] **征询转办** | `-` | `/api/workflow/core/paService/v1/consulTurnTodo` | [markdown](markdown/工作流程/征询转办.md)
- [API] **征询回复** | `-` | `/api/workflow/core/paService/v1/consulReply` | [markdown](markdown/工作流程/征询回复.md)
- [API] **通过主流程获取子流程** | `-` | `/api/workflow/core/paService/v1/getSubRequestByMainRequestId` | [markdown](markdown/工作流程/通过主流程获取子流程.md)
- [API] **通过子流程获取主流程** | `-` | `/api/workflow/core/paService/v1/getMainRequestBySubRequestId` | [markdown](markdown/工作流程/通过子流程获取主流程.md)
- [API] **通过子流程获取平行流程** | `-` | `/api/workflow/core/paService/v1/getParallelRequestBySubRequestId` | [markdown](markdown/工作流程/通过子流程获取平行流程.md)
- [API] **通过流程workflowId获取子流程设置** | `-` | `/api/workflow/core/paService/v1/getSubRequestSetByWorkflowId` | [markdown](markdown/工作流程/通过流程workflowId获取子流程设置.md)
- [API] **保存表单** | `-` | `/api/workflow/core/paService/v1/saveFormData` | [markdown](markdown/工作流程/保存表单.md)
- [API] **获取字段下拉框选项** | `-` | `/api/workflow/core/paService/v1/getFieldOption` | [markdown](markdown/工作流程/获取字段下拉框选项.md)
- [API] **添加共享** | `POST` | `/api/workflow/list/paService/v1/addRequestShare` | [markdown](markdown/工作流程/添加共享.md)
- [API] **前台可发起工作流类型列表** | `-` | `/api/workflow/list/paService/v1/getCreateWorkflowTypeList` | [markdown](markdown/工作流程/前台可发起工作流类型列表.md)
- [API] **新建委托接口** | `POST` | `/api/workflow/core/paService/v1/newAgent` | [markdown](markdown/工作流程/新建委托接口.md)
- [API] **批量委托接口** | `POST` | `/api/workflow/core/paService/v1/batchManualAgent` | [markdown](markdown/工作流程/批量委托接口.md)
- [API] **更新流程** | `POST` | `/workflow/v2/update` | [markdown](markdown/工作流程/更新流程.md)
- [DOC] **即将到达的流程列表接口** | `-` | `-` | [markdown](markdown/工作流程/即将到达的流程列表接口.md)
- [API] **判断子流程是否到达指定节点** | `POST` | `/api/workflow/core/paService/v1/judgeSubRequestAllArrived` | [markdown](markdown/工作流程/判断子流程是否到达指定节点.md)
- [API] **判断子流程是否全部归档** | `POST` | `/api/workflow/core/paService/v1/judgeSubRequestAllEnd` | [markdown](markdown/工作流程/判断子流程是否全部归档.md)
- [API] **触发子流程** | `POST` | `/api/workflow/core/paService/v1/triggerSubRequest` | [markdown](markdown/工作流程/触发子流程.md)
- [API] **查询主流程某节点上的所有手动触发子流程设置** | `POST` | `/api/workflow/core/paService/v1/getTriSubRequestMenuSet` | [markdown](markdown/工作流程/查询主流程某节点上的所有手动触发子流程设置.md)
- [API] **流程意见征询指定节点** | `POST` | `/api/workflow/core/paService/v1/consulWithNode` | [markdown](markdown/工作流程/流程意见征询指定节点.md)
- [API] **批量提交** | `POST` | `/api/workflow/core/paService/v1/batchSubmit` | [markdown](markdown/工作流程/批量提交.md)
- [API] **委托收回** | `POST` | `/api/workflow/core/paService/v1/recoverAgent` | [markdown](markdown/工作流程/委托收回.md)
- [API] **批量退回** | `POST` | `/api/workflow/core/paService/v1/batchReject` | [markdown](markdown/工作流程/批量退回.md)
- [API] **流程提交给发送人** | `POST` | `/api/workflow/core/paService/v1/submitToSender` | [markdown](markdown/工作流程/流程提交给发送人.md)
- [API] **减审** | `POST` | `/api/workflow/core/paService/v1/minusOperator` | [markdown](markdown/工作流程/减审.md)
- [API] **抄送收回** | `-` | `/api/workflow/core/paService/v1/doCcBack?access_token=` | [markdown](markdown/工作流程/抄送收回.md)
- [API] **回收站批量还原流程** | `-` | `/api/workflow/core/paService/v1/recover?access_token=` | [markdown](markdown/工作流程/回收站批量还原流程.md)
- [API] **批量校验用户待办节点必填字段是否为空** | `-` | `/api/workflow/core/paService/v1/batchVerifyMustField?access_token=` | [markdown](markdown/工作流程/批量校验用户待办节点必填字段是否为空.md)
- [API] **判断流程能否流转下去** | `-` | `/api/workflow/core/paService/v1/canFlowNextNode?access_token=` | [markdown](markdown/工作流程/判断流程能否流转下去.md)
- [API] **校验人员流程查看权限** | `-` | `/api/workflow/core/paService/v1/verifyRequestViewAuth?access_token=` | [markdown](markdown/工作流程/校验人员流程查看权限.md)
- [API] **流程恢复/启用** | `-` | `/api/workflow/core/paService/v1/open?access_token=` | [markdown](markdown/工作流程/流程恢复-启用.md)
- [API] **流程撤销** | `-` | `/api/workflow/core/paService/v1/cancle?access_token=` | [markdown](markdown/工作流程/流程撤销.md)
- [API] **流程暂停** | `-` | `/api/workflow/core/paService/v1/stop?access_token=` | [markdown](markdown/工作流程/流程暂停.md)
- [API] **保存流程** | `-` | `/api/workflow/core/paService/v1/saveRequest` | [markdown](markdown/工作流程/保存流程.md)
- [API] **根据id收回委托** | `-` | `/api/workflow/core/paService/v1/recoverAgentWithId?access_token=` | [markdown](markdown/工作流程/根据id收回委托.md)
- [API] **批量获取流程基础信息** | `GET` | `/api/workflow/core/paService/v1/batchGetRequestInfo` | [markdown](markdown/工作流程/批量获取流程基础信息.md)
- [API] **获取前台流程图显示数据** | `GET` | `/api/workflow/core/paService/v1/getRequestChart` | [markdown](markdown/工作流程/获取前台流程图显示数据.md)
- [API] **获取节点上下文数据** | `POST` | `/api/workflow/core/paService/v1/getNodeContextInfo` | [markdown](markdown/工作流程/获取节点上下文数据.md)
- [API] **获取待办流程发送人数据** | `POST` | `/api/workflow/core/paService/v1/getTodoSenderInfo` | [markdown](markdown/工作流程/获取待办流程发送人数据.md)
- [API] **获取可退回节点** | `GET` | `/api/workflow/core/paService/v1/getRejectNodes` | [markdown](markdown/工作流程/获取可退回节点.md)
- [API] **批量获取流程未操作者** | `GET` | `/api/workflow/core/paService/v1/batchGetRequestUnOperator` | [markdown](markdown/工作流程/批量获取流程未操作者.md)
- [API] **根据流程数据ID查询审批数据** | `GET` | `/workflow/v2/getInfoByID` | [markdown](markdown/工作流程/根据流程数据ID查询审批数据.md)
- [API] **获取流程流转数据** | `GET` | `/api/workflow/core/paService/v1/getRequestOperatorInfo请求方式：` | [markdown](markdown/工作流程/获取流程流转数据.md)
- [API] **获取流程签字意见** | `GET` | `/api/workflow/core/paService/v1/getRequestLog` | [markdown](markdown/工作流程/获取流程签字意见.md)
- [API] **获取流程信息** | `GET` | `/api/workflow/core/paService/v1/getWorkflowRequest` | [markdown](markdown/工作流程/获取流程信息.md)
- [API] **获取流程状态** | `GET` | `/api/workflow/core/paService/v1/getRequestStatus` | [markdown](markdown/工作流程/获取流程状态.md)
- [API] **获取流程图链接** | `GET` | `/api/workflow/core/paService/v1/getRequestFlowChart` | [markdown](markdown/工作流程/获取流程图链接.md)
- [API] **获取下一节点操作者信息** | `GET` | `/api/workflow/core/paService/v1/getRequestNextOperator` | [markdown](markdown/工作流程/获取下一节点操作者信息.md)
- [API] **获取转发列表** | `-` | `/api/workflow/core/paService/v1/getForwardBackListData` | [markdown](markdown/工作流程/获取转发列表.md)
- [API] **获取传阅列表** | `-` | `/api/workflow/core/paService/v1/getCirculateBackListData` | [markdown](markdown/工作流程/获取传阅列表.md)
- [API] **获取征询列表** | `-` | `/api/workflow/core/paService/v1/getConsulBackList` | [markdown](markdown/工作流程/获取征询列表.md)
- [API] **获取下节点信息** | `-` | `/api/workflow/core/paService/v1/getNextNodeInfo` | [markdown](markdown/工作流程/获取下节点信息.md)
- [API] **获取节点未操作者** | `-` | `/api/workflow/core/paService/v1/getNodeNotOperator` | [markdown](markdown/工作流程/获取节点未操作者.md)
- [API] **获取流程基础信息** | `-` | `/api/workflow/core/paService/v1/getRequestInfo` | [markdown](markdown/工作流程/获取流程基础信息.md)
- [API] **获取节点操作者** | `POST （Content_Type: application/json），备注：access_token放在params中备注  若没传递targetNodeId，则获取当前节点未操作者（可能有多个，全部返回）；  若传递了targetNodeId，且targetNodeId为当前节点，则获取指定节点未操作者；  若传递了targetNodeId，且targetNodeId不为当前节点，若指定节点为发起节点，则获取指定节点最新轮次操作者；  若传递了targetNodeId，且targetNodeId不为当前节点和发起节点，且calculateConfigOperator=true，则获取指定节点操作组配置的操作者；  若传递了targetNodeId，且targetNodeId不为当前节点和发起节点，且calculateConfigOperator=false，则获取指定节点最新轮次操作者；` | `/api/workflow/core/paService/v1/getNodeOperator` | [markdown](markdown/工作流程/获取节点操作者.md)
- [API] **获取抄送列表** | `-` | `/api/workflow/core/paService/v1/getCCBackListData?access_token=` | [markdown](markdown/工作流程/获取抄送列表.md)
- [API] **获取退回操作发送人** | `-` | `/api/workflow/core/paService/v1/getSendOperator?access_token=` | [markdown](markdown/工作流程/获取退回操作发送人.md)
- [API] **获取有权限的右键按钮** | `-` | `/api/workflow/core/paService/v1/rightMenu?access_token=` | [markdown](markdown/工作流程/获取有权限的右键按钮.md)
- [API] **获取可加审减审的相关操作者数据** | `-` | `/api/workflow/core/paService/v1/getAddMinusOperatorInfo?access_token=` | [markdown](markdown/工作流程/获取可加审减审的相关操作者数据.md)
- [API] **获取发起节点提交确认弹框信息** | `-` | `/api/workflow/core/paService/v1/getSubmitShowNodes?access_token=` | [markdown](markdown/工作流程/获取发起节点提交确认弹框信息.md)
- [API] **获取指定流转可选节点及操作者信息** | `-` | `/api/workflow/core/paService/v1/getSelectFlowNodeInfos?access_token=` | [markdown](markdown/工作流程/获取指定流转可选节点及操作者信息.md)
- [API] **获取被征询未回复的记录** | `-` | `/api/workflow/core/paService/v1/getBeConsulLog` | [markdown](markdown/工作流程/获取被征询未回复的记录.md)
- [API] **获取退回直达本节点跳过节点最新轮次操作者** | `-` | `/api/workflow/core/paService/v1/getToRejectNodeOperator` | [markdown](markdown/工作流程/获取退回直达本节点跳过节点最新轮次操作者.md)

## 快速入门

- [DOC] **接入必读** | `-` | `-` | [markdown](markdown/快速入门/接入必读.md)
- [DOC] **企业接入指南** | `-` | `-` | [markdown](markdown/快速入门/企业接入指南.md)
- [DOC] **标准规范** | `-` | `-` | [markdown](markdown/快速入门/标准规范.md)
- [DOC] **通用型应用配置指南** | `-` | `-` | [markdown](markdown/快速入门/通用型应用配置指南.md)
- [DOC] **本系统令牌免登第三方配置指南** | `-` | `-` | [markdown](markdown/快速入门/本系统令牌免登第三方配置指南.md)
- [DOC] **第三方免登本系统配置指南** | `-` | `-` | [markdown](markdown/快速入门/第三方免登本系统配置指南.md)
- [DOC] **e-cology免登本系统配置指南** | `-` | `-` | [markdown](markdown/快速入门/e-cology免登本系统配置指南.md)
- [DOC] **回调集成套件配置指南** | `-` | `-` | [markdown](markdown/快速入门/回调集成套件配置指南.md)

## 报告

- [API] **新建报告** | `POST` | `/workreport/v2/createWorkreport` | [markdown](markdown/报告/新建报告.md)
- [API] **修改报告** | `POST` | `/workreport/v2/updateWorkreport` | [markdown](markdown/报告/修改报告.md)
- [API] **查询报告** | `POST` | `/workreport/v2/queryWorkreport` | [markdown](markdown/报告/查询报告.md)
- [API] **报告统计** | `POST` | `/workreport/v2/queryWorkreportSta` | [markdown](markdown/报告/报告统计.md)

## 数据交换中心

- [API] **获取字段设置列表** | `GET` | `/api/odocexchange/v1/listExchangeField` | [markdown](markdown/数据交换中心/获取字段设置列表.md)
- [API] **获取单位信息** | `GET` | `/api/odocexchange/v1/getDepartment` | [markdown](markdown/数据交换中心/获取单位信息.md)
- [API] **获取单位列表** | `GET` | `/api/odocexchange/v1/listDepartment` | [markdown](markdown/数据交换中心/获取单位列表.md)
- [API] **发送数据（公文）** | `POST` | `/api/odocexchange/v1/sendDocument/api/odocexchange/v1/sendData` | [markdown](markdown/数据交换中心/发送数据（公文）.md)
- [API] **发送公文到其他单位（补发）** | `POST` | `/api/odocexchange/v1/sendDocToOtherDepartment` | [markdown](markdown/数据交换中心/发送公文到其他单位（补发）.md)
- [API] **获取待接收数据（公文）列表** | `GET` | `/api/odocexchange/v1/listNotReceivedDocument数据：/api/odocexchange/v1/listNotReceivedData` | [markdown](markdown/数据交换中心/获取待接收数据（公文）列表.md)
- [API] **获取(公文)业务数据（详情）** | `POST` | `/api/odocexchange/v1/getDocumentDetail/api/odocexchange/v1/getDataDetail` | [markdown](markdown/数据交换中心/获取(公文)业务数据（详情）.md)
- [API] **确认接收公文** | `POST` | `/api/odocexchange/v1/receiveDocument` | [markdown](markdown/数据交换中心/确认接收公文.md)
- [API] **发送反馈意见（发文方撤销、作废）** | `POST` | `/api/odocexchange/v1/sendOperateOpinion` | [markdown](markdown/数据交换中心/发送反馈意见（发文方撤销、作废）.md)
- [API] **发送反馈意见（收文方签收、拒收、退回）** | `POST` | `/api/odocexchange/v1/sendOperateOpinion` | [markdown](markdown/数据交换中心/发送反馈意见（收文方签收、拒收、退回）.md)
- [API] **获取反馈意见（发送方获取接收方签收、拒收、退回反馈意见）** | `POST` | `/api/odocexchange/v1/receiveOperateOpinion` | [markdown](markdown/数据交换中心/获取反馈意见（发送方获取接收方签收、拒收、退回反馈意见）.md)
- [API] **获取反馈意见（接收方获取发送方撤销、作废反馈意见）** | `POST` | `/api/odocexchange/v1/receiveOperateOpinion` | [markdown](markdown/数据交换中心/获取反馈意见（接收方获取发送方撤销、作废反馈意见）.md)
- [API] **批量操作** | `POST` | `/api/odocexchange/v1/batchReceiveData` | [markdown](markdown/数据交换中心/批量操作.md)
- [API] **获取指定编码单位信息** | `GET` | `/api/odocexchange/v1/getDepartmentByCodes` | [markdown](markdown/数据交换中心/获取指定编码单位信息.md)
- [API] **获取接入系统租户信息** | `GET` | `/api/odocexchange/v1/getOATenantByCode` | [markdown](markdown/数据交换中心/获取接入系统租户信息.md)
- [API] **获取平台交换应用ID** | `GET` | `/api/odocexchange/v1/getPlatAppId` | [markdown](markdown/数据交换中心/获取平台交换应用ID.md)
- [API] **获取应用模板信息** | `GET` | `/api/odocexchange/v1/getPlatAppTemplate` | [markdown](markdown/数据交换中心/获取应用模板信息.md)
- [API] **获取当前单位管理员** | `GET` | `/api/odocexchange/v1/getPlatFormAdminInfo` | [markdown](markdown/数据交换中心/获取当前单位管理员.md)
- [API] **获取租户信息** | `GET` | `/api/odocexchange/v1/getPlatFormInfo` | [markdown](markdown/数据交换中心/获取租户信息.md)
- [API] **获取平台数据状态** | `POST` | `/api/odocexchange/v1/getUnReceiveStatus` | [markdown](markdown/数据交换中心/获取平台数据状态.md)
- [API] **获取指定范围收文数据** | `POST` | `/api/odocexchange/v1/getReceiveDatas` | [markdown](markdown/数据交换中心/获取指定范围收文数据.md)
- [API] **获取收文状态** | `POST` | `/api/odocexchange/v1/getReceiveStatus` | [markdown](markdown/数据交换中心/获取收文状态.md)
- [API] **获取所有单位** | `GET` | `/api/odocexchange/v1/listAllDepartment` | [markdown](markdown/数据交换中心/获取所有单位.md)
- [API] **获取单位组列表** | `GET` | `/api/odocexchange/v1/listDepartmentGroup` | [markdown](markdown/数据交换中心/获取单位组列表.md)
- [API] **获取单位文员信息** | `POST` | `/api/odocexchange/v1/listUserByCode` | [markdown](markdown/数据交换中心/获取单位文员信息.md)
- [API] **刷新第三方平台数据** | `GET` | `/api/odocexchange/v1/refreshThirdPlatformData` | [markdown](markdown/数据交换中心/刷新第三方平台数据.md)
- [API] **重发外部第三方系统单位** | `POST` | `/api/odocexchange/v1/sendDocToThirdDept` | [markdown](markdown/数据交换中心/重发外部第三方系统单位.md)
- [API] **发送公文前校验** | `POST` | `/api/odocexchange/v1/verifySendDocument` | [markdown](markdown/数据交换中心/发送公文前校验.md)
- [API] **查看收文（更新平台查看时间）** | `GET` | `/api/odocexchange/v1/viewReceiveDoc` | [markdown](markdown/数据交换中心/查看收文（更新平台查看时间）.md)

## 日报

- [API] **新建日报** | `POST` | `/blog/v2/createBlog` | [markdown](markdown/日报/新建日报.md)
- [API] **编辑日报** | `POST` | `/blog/v2/updateBlog` | [markdown](markdown/日报/编辑日报.md)
- [API] **查询日报** | `POST` | `/blog/v2/queryBlog` | [markdown](markdown/日报/查询日报.md)
- [API] **日报统计** | `POST` | `/blog/v2/queryBlogStatistic` | [markdown](markdown/日报/日报统计.md)
- [API] **按更新时间查询团队日报** | `POST` | `/blog/v2/queryDateBlog` | [markdown](markdown/日报/按更新时间查询团队日报.md)

## 日程

- [API] **查询我的日程** | `POST` | `/api/calendar/openapi/v1/queryIndexAgenda` | [markdown](markdown/日程/查询我的日程.md)
- [API] **批量新建日程** | `-` | `/api/calendar/openapi/v1/batchCreateAgenda` | [markdown](markdown/日程/批量新建日程.md)
- [API] **查询日程类型** | `-` | `/api/calendar/openapi/v1/queryTypes` | [markdown](markdown/日程/查询日程类型.md)
- [API] **查询日程紧急程度** | `-` | `/api/calendar/openapi/v1/queryUrgency` | [markdown](markdown/日程/查询日程紧急程度.md)
- [API] **创建日程** | `-` | `/api/calendar/openapi/v1/createAgenda` | [markdown](markdown/日程/创建日程.md)
- [API] **删除日程** | `-` | `/api/calendar/openapi/v1/deleteById` | [markdown](markdown/日程/删除日程.md)
- [API] **根据id查询日程** | `-` | `/api/calendar/openapi/v1/queryById` | [markdown](markdown/日程/根据id查询日程.md)
- [API] **获取当前登录人有权限的日程** | `-` | `/api/calendar/openapi/v1/querySearchAgenda` | [markdown](markdown/日程/获取当前登录人有权限的日程.md)
- [API] **修改日程** | `-` | `/api/calendar/openapi/v1/updateById` | [markdown](markdown/日程/修改日程.md)
- [API] **批量修改日程字段** | `-` | `/api/calendar/openapi/v1/batchUpdateAgenda` | [markdown](markdown/日程/批量修改日程字段.md)

## 档案管理

- [API] **档案接收接口数据推送** | `POST` | `/api/archive/core/openapi/dataToArchive` | [markdown](markdown/档案管理/档案接收接口数据推送.md)

## 消息中心

- [API] **发送消息** | `POST` | `/api/mc/msg/sendMsg` | [markdown](markdown/消息中心/发送消息.md)
- [API] **删除消息** | `POST` | `/api/mc/msg/deleteMsg` | [markdown](markdown/消息中心/删除消息.md)
- [API] **标记消息** | `POST` | `/api/mc/msg/markMsg` | [markdown](markdown/消息中心/标记消息.md)
- [API] **查询关注列表** | `POST` | `/api/my/watch/queryAllWatch` | [markdown](markdown/消息中心/查询关注列表.md)
- [API] **查询待办接口** | `POST` | `/api/my/workWait/queryWorkWaitList` | [markdown](markdown/消息中心/查询待办接口.md)
- [API] **批量添加关注** | `POST` | `/api/my/watch/batchAddWatch` | [markdown](markdown/消息中心/批量添加关注.md)
- [API] **批量取消关注** | `POST` | `/api/my/watch/batchCancelWatch` | [markdown](markdown/消息中心/批量取消关注.md)
- [API] **发送营销短信接口** | `POST` | `/api/mc/msg/sendMarketingSms` | [markdown](markdown/消息中心/发送营销短信接口.md)
- [API] **添加事项标签** | `POST` | `app :/api/app/my/tag/addEntityTag?accessToken=` | [markdown](markdown/消息中心/添加事项标签.md)
- [DOC] **删除事项标签** | `POST` | `-` | [markdown](markdown/消息中心/删除事项标签.md)

## 电子签

- [API] **初始化绑定服务** | `POST` | `/api/signcenter/server/initServerSetting` | [markdown](markdown/电子签/初始化绑定服务.md)

## 电子费控

- [API] **获取流程信息** | `-` | `/api/fna/workflow/core/paService/v1/getWorkflowRequest` | [markdown](markdown/电子费控/获取流程信息.md)
- [API] **保存表单数据** | `-` | `/api/fna/workflow/core/paService/v1/saveFormData` | [markdown](markdown/电子费控/保存表单数据.md)

## 知识文档

- [API] **文件上传** | `POST` | `/api/file/v2/common/upload` | [markdown](markdown/知识文档/文件上传.md)
- [API] **文件下载** | `GET` | `/api/file/v2/common/download/{fileId}` | [markdown](markdown/知识文档/文件下载.md)
- [API] **base64上传** | `POST` | `/api/file/v2/common/upload/base64` | [markdown](markdown/知识文档/base64上传.md)
- [API] **查询文档附件列表** | `GET` | `/api/doc/v2/attList/{docId}` | [markdown](markdown/知识文档/查询文档附件列表.md)
- [API] **删除文档** | `POST` | `/api/doc/document/v2/destory` | [markdown](markdown/知识文档/删除文档.md)
- [API] **文档详情tab页** | `GET` | `/api/doc/document/v2/tabInfo` | [markdown](markdown/知识文档/文档详情tab页.md)
- [API] **文档详情-文档内容** | `GET` | `/api/doc/document/v2/info` | [markdown](markdown/知识文档/文档详情-文档内容.md)
- [API] **文档属性** | `GET` | `/api/doc/document/v2/property` | [markdown](markdown/知识文档/文档属性.md)
- [API] **获取文档版本** | `GET` | `/api/doc/document/v2/versions` | [markdown](markdown/知识文档/获取文档版本.md)
- [API] **文档日志** | `GET` | `/api/doc/document/v2/logs` | [markdown](markdown/知识文档/文档日志.md)
- [API] **创建文档总数** | `POST` | `/api/doc/document/v2/docCount` | [markdown](markdown/知识文档/创建文档总数.md)
- [API] **获取指定目录下的文档列表** | `POST` | `/api/doc/document/v2/folderDocList` | [markdown](markdown/知识文档/获取指定目录下的文档列表.md)
- [API] **新建、编辑文档-保存** | `POST` | `/api/doc/document/v2/saveDoc` | [markdown](markdown/知识文档/新建、编辑文档-保存.md)
- [API] **新建、编辑文档-是否签出验证** | `POST` | `/api/doc/document/v2/checkEditLock` | [markdown](markdown/知识文档/新建、编辑文档-是否签出验证.md)
- [API] **文档详情-添加文档阅读记录** | `POST` | `/api/doc/document/v2/addDocumentLog` | [markdown](markdown/知识文档/文档详情-添加文档阅读记录.md)
- [API] **文档失效** | `POST` | `/api/doc/document/v2/invalidate` | [markdown](markdown/知识文档/文档失效.md)
- [API] **全部文档列表** | `POST` | `/api/doc/documents/list/all` | [markdown](markdown/知识文档/全部文档列表.md)
- [API] **我的文档列表** | `POST` | `/api/doc/documents/list/mine` | [markdown](markdown/知识文档/我的文档列表.md)
- [API] **获取文档总数** | `POST` | `/api/doc/documents/list/getAllCount` | [markdown](markdown/知识文档/获取文档总数.md)
- [API] **查询对应知识库下面的文件夹节点** | `POST` | `/api/doc/folder/tree/rootNodes` | [markdown](markdown/知识文档/查询对应知识库下面的文件夹节点.md)
- [API] **查询文件夹的子节点** | `POST` | `/api/doc/folder/tree/subNodes` | [markdown](markdown/知识文档/查询文件夹的子节点.md)
- [API] **文件夹列表** | `POST` | `/api/doc/folder/list` | [markdown](markdown/知识文档/文件夹列表.md)
- [API] **添加文档共享** | `POST` | `/api/doc/shareentry/v2/addShare` | [markdown](markdown/知识文档/添加文档共享.md)
- [API] **新建文档** | `POST` | `/api/doc/document/v2/create` | [markdown](markdown/知识文档/新建文档.md)
- [API] **查询文件信息** | `POST` | `/api/file/v2/common/file/queryFileInfo` | [markdown](markdown/知识文档/查询文件信息.md)
- [API] **获取文件版本** | `POST` | `/api/file/v2/common/file/getFileVersion` | [markdown](markdown/知识文档/获取文件版本.md)
- [API] **下载E9文件** | `GET` | `/api/file/v2/common/download/e9` | [markdown](markdown/知识文档/下载E9文件.md)
- [API] **获取文件第三方预览地址** | `POST` | `/api/file/online/getFilePreviewUrl` | [markdown](markdown/知识文档/获取文件第三方预览地址.md)
- [API] **文件加水印** | `POST` | `/api/file/online/addWatermark` | [markdown](markdown/知识文档/文件加水印.md)
- [API] **创建轻文档** | `POST` | `/api/doc/lightDoc/createDoc` | [markdown](markdown/知识文档/创建轻文档.md)
- [API] **重新上传接口** | `POST` | `/api/file/v2/common/upload/reUpload` | [markdown](markdown/知识文档/重新上传接口.md)

## 系统权限

- [API] **新增角色** | `POST` | `/api/auth/role/v1/batchSave` | [markdown](markdown/系统权限/新增角色.md)
- [API] **更新角色** | `POST` | `/api/auth/role/v1/batchUpdate` | [markdown](markdown/系统权限/更新角色.md)
- [API] **删除角色** | `POST` | `/api/auth/role/v1/batchDelete` | [markdown](markdown/系统权限/删除角色.md)
- [API] **查询角色** | `POST` | `/api/auth/role/v1/getRoleByCondition` | [markdown](markdown/系统权限/查询角色.md)
- [API] **新增角色成员** | `POST` | `/api/auth/role/user/v1/batchSave` | [markdown](markdown/系统权限/新增角色成员.md)
- [API] **更新角色成员** | `POST` | `/api/auth/role/user/v1/batchUpdate` | [markdown](markdown/系统权限/更新角色成员.md)
- [API] **删除角色成员** | `POST` | `/api/auth/role/user/v1/batchDelete` | [markdown](markdown/系统权限/删除角色成员.md)
- [API] **查询角色成员** | `POST` | `/api/auth/role/user/v1/getUserRoleByCondition` | [markdown](markdown/系统权限/查询角色成员.md)
- [API] **新建自定义菜单** | `POST` | `/api/auth/custom/permission/v1/batchCreateCustomMenu` | [markdown](markdown/系统权限/新建自定义菜单.md)
- [API] **更新自定义菜单** | `POST` | `/api/auth/custom/permission/v1/batchUpdateCustomMenu` | [markdown](markdown/系统权限/更新自定义菜单.md)
- [API] **删除自定义菜单** | `POST` | `/api/auth/custom/permission/v1/batchDeleteCustomMenu` | [markdown](markdown/系统权限/删除自定义菜单.md)
- [API] **新增自定义权限项** | `POST` | `/api/auth/custom/permission/v1/batchCreateCustomPermissionSet` | [markdown](markdown/系统权限/新增自定义权限项.md)
- [API] **更新自定义权限项** | `POST` | `/api/auth/custom/permission/v1/batchUpdateCustomPermissionSet` | [markdown](markdown/系统权限/更新自定义权限项.md)
- [API] **删除自定义权限项** | `POST` | `/api/auth/custom/permission/v1/batchDeleteCustomPermissionSet` | [markdown](markdown/系统权限/删除自定义权限项.md)
- [API] **新增自定义接口权限** | `POST` | `/api/auth/custom/permission/v1/batchCreateCustomPermission` | [markdown](markdown/系统权限/新增自定义接口权限.md)
- [API] **更新自定义接口权限** | `POST` | `/api/auth/custom/permission/v1/batchUpdateCustomPermission` | [markdown](markdown/系统权限/更新自定义接口权限.md)
- [API] **删除自定义接口权限** | `POST` | `/api/auth/custom/permission/v1/batchDeleteCustomPermission` | [markdown](markdown/系统权限/删除自定义接口权限.md)
- [API] **获取有权限的接口路径** | `GET` | `/api/auth/custom/permission/v1/getCustomUserApiPath` | [markdown](markdown/系统权限/获取有权限的接口路径.md)

## 系统集成

- [API] **接收流程数据** | `-` | `/api/open_intunifytodo/server_engine/receiveRequestInfo` | [markdown](markdown/系统集成/接收流程数据.md)
- [API] **档案集成归档同步** | `POST` | `/api/intiascore/v1/doSync` | [markdown](markdown/系统集成/档案集成归档同步.md)

## 线索

- [API] **新增线索** | `POST` | `/crm/v2/create` | [markdown](markdown/线索/新增线索.md)
- [API] **删除线索** | `POST` | `/crm/v2/delete` | [markdown](markdown/线索/删除线索.md)
- [API] **查询线索** | `GET` | `/crm/v2/get` | [markdown](markdown/线索/查询线索.md)
- [API] **搜索线索** | `GET` | `/crm/v2/search` | [markdown](markdown/线索/搜索线索.md)

## 考勤

- [API] **考勤签到签退** | `POST` | `/attend/v2/check` | [markdown](markdown/考勤/考勤签到签退.md)
- [API] **获取工作时长-每日统计列表数据** | `POST` | `/api/attend/web/dailyStatis/getAttendDailyStatisReport` | [markdown](markdown/考勤/获取工作时长-每日统计列表数据.md)
- [API] **同步考勤数据** | `POST` | `/api/attend/web/open/syncMachineData` | [markdown](markdown/考勤/同步考勤数据.md)
- [API] **查询旷工日期** | `POST` | `/attend/v2/getAbsenteeism` | [markdown](markdown/考勤/查询旷工日期.md)
- [API] **查询缺勤明细** | `POST` | `/attend/v2/getAbsence` | [markdown](markdown/考勤/查询缺勤明细.md)
- [API] **查询法定节假日** | `POST` | `/attend/v2/getHoliday` | [markdown](markdown/考勤/查询法定节假日.md)
- [API] **查询未打卡明细** | `POST` | `/attend/v2/getUnchecked` | [markdown](markdown/考勤/查询未打卡明细.md)
- [API] **查询迟到明细** | `POST` | `/attend/v2/getLate` | [markdown](markdown/考勤/查询迟到明细.md)
- [API] **查询早退明细** | `POST` | `/attend/v2/getEarlyOut` | [markdown](markdown/考勤/查询早退明细.md)
- [API] **查询申诉明细** | `POST` | `/attend/v2/getAppeals` | [markdown](markdown/考勤/查询申诉明细.md)
- [API] **查询工作日明细** | `POST` | `/attend/v2/getWorkDay` | [markdown](markdown/考勤/查询工作日明细.md)
- [API] **查询节假日出勤明细** | `POST` | `/attend/v2/getHolidayWork` | [markdown](markdown/考勤/查询节假日出勤明细.md)
- [API] **查询非工作日出勤明细** | `POST` | `/attend/v2/getPlayWork` | [markdown](markdown/考勤/查询非工作日出勤明细.md)
- [API] **查询请假明细** | `POST` | `/attend/v2/getLeave` | [markdown](markdown/考勤/查询请假明细.md)
- [API] **查询出差明细** | `POST` | `/attend/v2/getBusinessTrip` | [markdown](markdown/考勤/查询出差明细.md)
- [API] **查询外出明细** | `POST` | `/attend/v2/getOut` | [markdown](markdown/考勤/查询外出明细.md)
- [API] **查询汇总明细** | `POST` | `/attend/v2/getCollect` | [markdown](markdown/考勤/查询汇总明细.md)
- [API] **查询加班明细** | `POST` | `/attend/v2/getOverTime` | [markdown](markdown/考勤/查询加班明细.md)
- [API] **人员假期余额查询** | `POST` | `/api/attend/web/open/getVacationBalance` | [markdown](markdown/考勤/人员假期余额查询.md)
- [API] **签到接口查询** | `POST` | `/api/attend/web/open/getSignInData` | [markdown](markdown/考勤/签到接口查询.md)
- [API] **签退接口查询** | `POST` | `/api/attend/web/open/getSignOutData` | [markdown](markdown/考勤/签退接口查询.md)
- [API] **考勤流程保存** | `-` | `/api/generic/invoke/attend/saveFlowData` | [markdown](markdown/考勤/考勤流程保存.md)
- [API] **获取考勤流程时长计算** | `POST` | `/api/attend/web/open/getFlowDuration` | [markdown](markdown/考勤/获取考勤流程时长计算.md)
- [API] **获取考勤日期类型** | `POST` | `/api/attend/web/open/getDayTypeByAttendDate` | [markdown](markdown/考勤/获取考勤日期类型.md)

## 职级

- [API] **获取职级列表（V2）** | `GET` | `/grade/v2/list` | [markdown](markdown/职级/获取职级列表（V2）.md)
- [API] **同步兼职信息** | `POST` | `/api/hrm/restful/syncExtra` | [markdown](markdown/职级/同步兼职信息.md)

## 联系人

- [API] **新增联系人** | `POST` | `/crm/v2/create` | [markdown](markdown/联系人/新增联系人.md)
- [API] **联系记录查询** | `POST` | `/api/crm/v2/employeeComment` | [markdown](markdown/联系人/联系记录查询.md)
- [API] **删除联系人** | `POST` | `/crm/v2/delete` | [markdown](markdown/联系人/删除联系人.md)
- [API] **修改联系人** | `POST` | `/crm/v2/update` | [markdown](markdown/联系人/修改联系人.md)
- [API] **查询联系人** | `GET` | `/crm/v2/get` | [markdown](markdown/联系人/查询联系人.md)
- [API] **搜索联系人** | `GET` | `/crm/v2/search` | [markdown](markdown/联系人/搜索联系人.md)

## 订单

- [API] **新增订单** | `POST` | `/crm/v2/create` | [markdown](markdown/订单/新增订单.md)
- [API] **修改订单** | `POST` | `/crm/v2/update` | [markdown](markdown/订单/修改订单.md)
- [API] **删除订单** | `POST` | `/crm/v2/delete` | [markdown](markdown/订单/删除订单.md)
- [API] **查询订单** | `GET` | `/crm/v2/get` | [markdown](markdown/订单/查询订单.md)
- [API] **搜索订单** | `GET` | `/crm/v2/search` | [markdown](markdown/订单/搜索订单.md)
- [API] **订单获取自定义表单** | `GET` | `/crm/v2/getCustomForms` | [markdown](markdown/订单/订单获取自定义表单.md)
- [API] **订单获取自定义表单字段** | `GET` | `/crm/v2/getCustomFields` | [markdown](markdown/订单/订单获取自定义表单字段.md)
- [API] **获取增删改的订单** | `GET` | `/crm/v2/getChanged` | [markdown](markdown/订单/获取增删改的订单.md)
- [API] **订单新建期次、回款、付款、开票** | `POST` | `/crm/v2/addPayment` | [markdown](markdown/订单/订单新建期次、回款、付款、开票.md)
- [API] **订单删除期次、回款、付款、开票等** | `POST` | `/crm/v2/deletePayment` | [markdown](markdown/订单/订单删除期次、回款、付款、开票等.md)
- [API] **订单查询期次、回款、付款、开票等** | `POST` | `/crm/v2/getPayment` | [markdown](markdown/订单/订单查询期次、回款、付款、开票等.md)
- [API] **订单搜索期次、回款、付款、开票等** | `POST` | `/crm/v2/searchPayment` | [markdown](markdown/订单/订单搜索期次、回款、付款、开票等.md)

## 认证

- [API] **获取code信息** | `GET、POST` | `/oauth2/authorize` | [markdown](markdown/认证/获取code信息.md)
- [API] **获取accessToken信息** | `POST` | `/oauth2/access_token` | [markdown](markdown/认证/获取accessToken信息.md)
- [API] **刷新accessToken信息** | `-` | `/oauth2/refresh_token` | [markdown](markdown/认证/刷新accessToken信息.md)

## 资金

- [API] **创建资金** | `POST` | `/crm/v2/create` | [markdown](markdown/资金/创建资金.md)
- [API] **删除资金** | `POST` | `/crm/v2/delete` | [markdown](markdown/资金/删除资金.md)
- [API] **修改资金** | `POST` | `/crm/v2/update` | [markdown](markdown/资金/修改资金.md)
- [API] **查询资金** | `GET` | `/crm/v2/get` | [markdown](markdown/资金/查询资金.md)
- [API] **搜索资金** | `GET` | `/crm/v2/search` | [markdown](markdown/资金/搜索资金.md)
- [API] **资金充值** | `POST` | `/crm/v2/rechargeCapital` | [markdown](markdown/资金/资金充值.md)
- [API] **资金转出** | `POST` | `/crm/v2/divertCapital` | [markdown](markdown/资金/资金转出.md)

## 通知公告

- [API] **通知公告数据查询** | `POST` | `/api/placard/v1/allDatas` | [markdown](markdown/通知公告/通知公告数据查询.md)

## 邮件

- [API] **发送内部邮件** | `POST` | `/api/mail/send/v1/sendInternalMail` | [markdown](markdown/邮件/发送内部邮件.md)
- [DOC] **获取邮件详情SAPI接口** | `POST` | `-` | [markdown](markdown/邮件/获取邮件详情SAPI接口.md)
- [DOC] **获取邮件未读数SAPI接口** | `GET` | `-` | [markdown](markdown/邮件/获取邮件未读数SAPI接口.md)

## 部门

- [API] **同步部门** | `POST` | `/api/hrm/restful/syncDepartment` | [markdown](markdown/部门/同步部门.md)
- [API] **同步分部** | `POST` | `/api/hrm/restful/syncSubcompany` | [markdown](markdown/部门/同步分部.md)
- [API] **组织（含分部、部门）查询** | `POST` | `/api/hrm/restful/queryOrg` | [markdown](markdown/部门/组织（含分部、部门）查询.md)
- [API] **启用部门** | `POST` | `/api/hrm/restful/enableDepartment` | [markdown](markdown/部门/启用部门.md)
- [API] **停用部门** | `POST` | `/api/hrm/restful/disableDepartment` | [markdown](markdown/部门/停用部门.md)
- [API] **新增部门** | `POST` | `/department/v2/create` | [markdown](markdown/部门/新增部门.md)
- [API] **修改部门** | `POST` | `/department/v2/update` | [markdown](markdown/部门/修改部门.md)
- [API] **删除部门** | `POST` | `/department/v2/delete` | [markdown](markdown/部门/删除部门.md)
- [API] **查询部门** | `GET` | `/department/v2/get` | [markdown](markdown/部门/查询部门.md)
- [API] **查询部门列表** | `GET` | `/department/v2/list` | [markdown](markdown/部门/查询部门列表.md)
- [API] **按更新时间查询部门信息** | `POST` | `/department/v2/findUpdateDepartment` | [markdown](markdown/部门/按更新时间查询部门信息.md)

## 项目

- [API] **新增项目** | `POST` | `/mainline/v2/create` | [markdown](markdown/项目/新增项目.md)
- [API] **删除项目** | `POST` | `/mainline/v2/delete` | [markdown](markdown/项目/删除项目.md)
- [API] **修改项目** | `POST` | `/mainline/v2/update` | [markdown](markdown/项目/修改项目.md)
- [API] **查询项目** | `GET` | `/mainline/v2/info` | [markdown](markdown/项目/查询项目.md)
- [API] **查询团队项目** | `POST` | `/mainline/v2/queryMainlines` | [markdown](markdown/项目/查询团队项目.md)
- [API] **查询我的项目** | `POST` | `/mainline/v2/mineInfo` | [markdown](markdown/项目/查询我的项目.md)
- [API] **项目查询计划任务** | `POST` | `/mainline/v2/queryMainlineTasks` | [markdown](markdown/项目/项目查询计划任务.md)
- [API] **查询项目关联事项** | `POST` | `/mainline/v2/queryMainlineRelevances` | [markdown](markdown/项目/查询项目关联事项.md)
- [API] **查询项目分类** | `GET` | `/mainline/v2/queryMainlineCategories` | [markdown](markdown/项目/查询项目分类.md)
- [API] **根据项目分类ID查询自定义字段** | `GET` | `/mainline/v2/queryFormInfoByMainlineGroup` | [markdown](markdown/项目/根据项目分类ID查询自定义字段.md)
- [API] **按更新时间查询团队项目** | `POST` | `/mainline/v2/queryUpdateMainlines` | [markdown](markdown/项目/按更新时间查询团队项目.md)

