# DNS Rules Builder

自动聚合广告规则源，生成 Blocky / Technitium 兼容规则。

---

## 📊 Live Dashboard

> 自动生成状态（GitHub Actions 每日更新）

<!-- START_DASHBOARD -->

<div>

## 🧠 DNS Rules Status

**⚠️ 该内容由 GitHub Actions 自动生成**

</div>

<!-- 直接展示 status.md 内容（避免 ``` 冲突） -->

<!-- DASHBOARD_START -->
<!-- DASHBOARD_END -->

---

## 📁 Output Files

- output/blocklist.txt
- output/whitelist.txt
- output/status.json
- output/status.md

---

## ⚙️ Features

- 多规则格式支持
- 增量更新（ETag / 304）
- SQLite 缓存
- 白名单系统
- 自动冲突解析
- GitHub Actions 自动运行

---

## ⏱ Schedule

- 每天 00:00（北京时间）自动更新
- upstream.yaml 变更自动触发
