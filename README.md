DNS Rules Builder

自动聚合广告规则源，生成 Blocky / Technitium / SmartDNS 兼容规则。

---

📊 Live Dashboard

«自动生成状态（GitHub Actions 每日更新）»

<!-- START_DASHBOARD --><div>🧠 DNS Rules Status

⚠️ 该内容由 GitHub Actions 自动生成

</div><!-- 直接展示 status.md 内容（避免 ``` 冲突） --><!-- DASHBOARD_START --><!-- DASHBOARD_END -->---

📁 Output Files

以下文件由 GitHub Actions 自动生成并直接提交到仓库：

- "Blocky / Technitium 黑名单" (https://github.com/LoogCP/adrules/blob/main/output/blocklist.txt) — 纯域名格式
- "Blocky / Technitium 白名单" (https://github.com/LoogCP/adrules/blob/main/output/whitelist.txt) — 纯域名格式
- "SmartDNS 规则集" (https://github.com/LoogCP/adrules/blob/main/output/smartdns.conf) — SmartDNS 配置规则
- "运行状态 JSON" (https://github.com/LoogCP/adrules/blob/main/output/status.json) — 自动生成的运行统计
- "运行状态 Markdown" (https://github.com/LoogCP/adrules/blob/main/output/status.md) — 自动生成的状态报告

---

⚙️ Features

- 多规则格式支持
- Blocky / Technitium 纯域名规则输出
- SmartDNS 规则集输出
- 增量更新（ETag / 304）
- SQLite 缓存
- 白名单系统
- 自动冲突解析
- GitHub Actions 自动运行

---

⏱ Schedule

- 每天 00:00（北京时间）自动更新
- "upstream.yaml" 变更自动触发
