# DNS Rules Builder

自动聚合多个广告规则源，生成 Blocky / Technitium 兼容规则。

## Features

- 多规则格式支持（hosts / adblock / adguard / wildcard）
- SQLite 增量更新
- ETag / Last-Modified / 304
- 白名单支持
- 自动冲突解析
- GitHub Actions 定时更新

## Output

- output/blocklist.txt
- output/whitelist.txt
- output/status.json
- output/status.md

## Run locally

```bash
pip install -r requirements.txt
python -m scripts.main
