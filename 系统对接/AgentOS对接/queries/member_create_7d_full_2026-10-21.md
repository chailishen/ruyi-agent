# 最近 7 天创建账号完整清单

- 查询时间：2026-10-21（Asia/Shanghai）
- 数据源：`audit_events`（`action = member.create`），关联 `users` / `orgs` / `teams`
- 含后来被删除或从 `users` 清除的账号
- 共 **11** 条

| # | 创建时间 | 操作人 | 人员姓名 | 邮箱 | 角色 | 组织 | 团队 | 创建时状态 | 当前状态 | 人员ID |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2026-10-15 14:37:26 | 柴立身 | 周辰 | macchen0326@163.com | member | 雄安科学园 | 雄安科学园 · 产业投资中心 | ready | 仍存在 | user_a7988e32a24a |
| 2 | 2026-10-17 15:30:36 | AgentOS Admin | QA 功能验收 A 20261017 | qa-functional-a-f51d1f6a@example.com | member | 雄安科学园 | Default | ready | 已从 users 清除 | user_d6b28543d242 |
| 3 | 2026-10-17 15:31:05 | AgentOS Admin | QA 功能验收 B 20261017 | qa-functional-b-004bbab1@example.com | member | 雄安科学园 | Default | ready | 已从 users 清除 | user_e8de5923ad9a |
| 4 | 2026-10-17 15:48:42 | AgentOS Admin | QA 功能验收 C 20261017 20069c08 | qa-functional-c-20069c08@example.com | member | 雄安科学园 | Default | ready | 已从 users 清除 | user_03f9b4d8f993 |
| 5 | 2026-10-17 17:50:49 | AgentOS Admin | QA Expert 9d458f6519 | expert-9d458f6519@example.com | member | 雄安科学园 | 雄安科学园 · 综合行政组 | ready | 已从 users 清除 | user_5b773fdad450 |
| 6 | 2026-10-17 17:50:49 | AgentOS Admin | Knowledge QA ff8240f38a | knowledge-primary-ff8240f38a@example.com | member | 雄安科学园 | 雄安科学园 · 综合行政组 | ready | 已从 users 清除 | user_98e7f0e36d0b |
| 7 | 2026-10-17 17:51:19 | AgentOS Admin | Knowledge QA ff8240f38a | knowledge-same-display-ff8240f38a@example.com | member | 雄安科学园 | 雄安科学园 · 综合行政组 | ready | 仍存在 | user_f2432bd44fa8 |
| 8 | 2026-10-17 18:56:26 | AgentOS Admin | Knowledge Default QA 6f64f62082 | knowledge-default-6f64f62082@example.com | member | 雄安科学园 | 雄安科学园 · 综合行政组 | ready | 仍存在 | user_fdd2f983e3e3 |
| 9 | 2026-10-17 19:48:29 | AgentOS Admin | Knowledge Default QA 0c1b63ec08 | knowledge-default-0c1b63ec08@example.com | member | 雄安科学园 | 雄安科学园 · 综合行政组 | ready | 仍存在 | user_de7712173e4d |
| 10 | 2026-10-18 01:37:02 | AgentOS Admin | Default R5 Synthetic QA a2db4a0c0a6760ef | default-r5-a2db4a0c0a6760ef@example.com | member | 雄安科学园 | 雄安科学园 · 综合行政组 | ready | 已从 users 清除 | user_bff372eb5bdb |
| 11 | 2026-10-21 10:10:39 | 柴立身 | 刘育铨 | 1029825294@qq.com | member | 雄安科学园 | 雄安科学园 · 科技创新组 | ready | 仍存在 | user_9ad8ad1cc780 |

## 摘要

| 类型 | 数量 |
| --- | ---: |
| 真人业务账号（仍存在） | 2（周辰、刘育铨） |
| QA / 测试账号 | 9 |
| 其中已从 users 清除 | 6 |
| 结果均为 success | 11 |
