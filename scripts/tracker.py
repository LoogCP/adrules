def write_markdown(status):

    md = OUTPUT_DIR / "status.md"

    lines = []

    lines.append("# 🧠 DNS Rules Dashboard")
    lines.append("")
    lines.append(f"⏰ Last Update: {status['run_at']}")
    lines.append("")
    lines.append("## 📊 Overview")
    lines.append(f"- Sources: {len(status['sources'])}")
    lines.append(f"- Before Merge: {status['before_merge']}")
    lines.append(f"- Blacklist: {status['blacklist']}")
    lines.append(f"- Whitelist: {status['whitelist']}")
    lines.append(f"- Total: {status['total']}")
    lines.append(f"- Dedup Rate: {status['dedup_rate']}")
    lines.append("")
    lines.append("## 🌐 Sources Status")

    for s in status["sources"]:
        lines.append(f"- {s['url']} → {s.get('status')} ({s.get('entry_count', 0)})")

    with open(md, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
