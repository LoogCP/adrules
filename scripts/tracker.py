import json
from scripts.constants import OUTPUT_DIR
from scripts.utils import utc_now


def write_status(sources_status, before_merge, blacklist, whitelist):

    OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

    status = {
        "run_at": utc_now(),
        "sources": sources_status,
        "before_merge": before_merge,
        "blacklist": len(blacklist),
        "whitelist": len(whitelist),
        "total": len(blacklist) + len(whitelist),
        "dedup_rate": round(
            1 - (len(blacklist) + len(whitelist)) / max(before_merge, 1),
            4,
        ),
    }

    with open(OUTPUT_DIR / "status.json", "w", encoding="utf-8") as f:
        json.dump(status, f, indent=2, ensure_ascii=False)

    return status


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
        lines.append(
            f"- {s['url']} → {s.get('status')} ({s.get('entry_count', 0)})"
        )

    with open(md, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
