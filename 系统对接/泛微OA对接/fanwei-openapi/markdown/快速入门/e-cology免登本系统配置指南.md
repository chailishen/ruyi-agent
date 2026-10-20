# e-cology免登本系统配置指南

- **文档 ID**: `949873915010760705`
- **业务模块**: 快速入门
- **是否 API 接口**: 否（说明文档）

## 备注

- 备注：如果出现如下情况，请参考后续的解决步骤：

## 正文

## e-cology免登本系统配置指南
注：由于此方案实现老版本e-cology免登本系统配置过于复杂，可联系集成组以第三方免登的方式实现e-cology免登本系统
##### 场景：
在e-cology门户页面集成登录元素，点击后免登到本系统（前提：e-cology用户配置的移动电话或电子邮件是本系统的登录账号，优先用移动电话免登）。
##### 业务流：
本系统开放平台新建免登套件并审核通过 -> e-cology门户页面集成登录元素 -> 点击免登到本系统。
##### 详细操作步骤：
###### 一、在本系统开放平台新建免登套件
在本系统开放平台中新建e-cology免登本系统应用，审批通过后可看到app_key、app_secret。
###### 二、e-cology项目配置
1.将本系统ip地址（120.26.103.173,121.40.74.89,120.26.103.174,120.26.103.175,121.40.74.90）配置到e-cology项目HrmWebserviceIP.properties配置文件中并重启。2.检查e-cology用户是否配置了移动电话或电子邮件（移动电话或电子邮件至少要配置一个并且是本系统的登录账号）:3.e-cology中的人员姓名必须和本系统的姓名一致
4.检查web service是否已部署:在浏览器中输入http://{ecology系统访问地址}/services，应显示如下页面（如: http://E10环境地址/services）：
如果未出现上述页面，则web service未部署成功，请与e-cology项目人员联系。
###### 三、在e-cology系统集成登录
(1)到集成中心新建集成登录      入口：登录e-cology系统->后端应用中心->集成中心->集成登录->新建
(2)在集成中填写相关配置要求：    1).内网地址、外网地址固定填写：{OpenApiOrigin}/oauth2/ecologyToEteams
2).请求方式必须为post；
3).登录系统编码必须为UTF-8；
4).账号参数名称必须为account，且必须选中"使用ecology账号"；
5).密码参数名称必须为pwd，且必须选中"使用ecology密码"；
6).部门参数名必须为dept，参数值选择“部门”；
7).自定义参数名app_key，参数值选择“固定值”，从已审核免登套件查看并填写，如：83d45cdfa2077e92c06749ef3f01a354；
8).自定义参数名app_security，参数值选择“固定值”，从已审核免登套件查看并填写，如：aa1101bf1ad02f59eebe73c54d678fb；
9).单点登录地址：/interface/Entrance.jsp；
10).标识：后面步骤会使用到。
(3)在登录页面集成免登元素（前端实现方法一）新建登录后页面入口：门户引擎->门户页面->登陆后门户
新建门户页面的要求：    1).必须启用；    2).页面地址如：http://ip/interface/Entrance.jsp?id=HR&module=workflow&hideHead=0&hideIM=0&redirect_uri=跳转地址（其中IP是用户的ec对应地址或者域名，id是步骤2中的标识，module是指向eteams的功能模块，其他几个参数为固定值）
效果：点击配置的页面即可免登到本系统组织
（4）集成免登到工具菜单配置（前端实现方法二）新建工具栏菜单入口：门户引擎->门户菜单->工具栏菜单
新建工具栏菜单的要求：    1).必须启用；    2).URL配置如：/interface/Entrance.jsp?id=HR&module=workflow&hideHead=0&hideIM=0&redirect_uri=https://跳转地址
（其中id是步骤2中的标识，module是指向eteams的功能模块，其他几个参数为固定值）
效果图：点击配置的工具栏菜单即可免登到本系统组织
备注：如果出现如下情况，请参考后续的解决步骤：
步骤一：Chrome浏览器，地址栏输入chrome://flags/步骤二：搜索"SameSite by default cookies"步骤三：找到"SameSite by default cookies"和"Cookies without SameSite must be secure"，将这两项设置为Disable步骤四：重启浏览器
