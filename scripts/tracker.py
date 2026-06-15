import json
from scripts.constants import OUTPUT_DIR
from scripts.utils import utc_now


def write_status(
    sources_status,
    before_merge,
    blacklist,
    whitelist,
):

    OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

    status = {
        "run_at": utc_now(),
        "sources": sources_status,
        "before_merge": before_merge,
        "blacklist": len(blacklist),
        "whitelist": len(whitelist),
        "total": len(blacklist) + len(whitelist),
    }

    status_file = OUTPUT_DIR / "status.json"

    with open(status_file, "w", encoding="utf-8") as f:
        json.dump(status, f, indent=2)


def write_markdown(status_json):

    md_file = OUTPUT_DIR / "status.md"

    lines = []

    lines.append("# DNS Rules Status")
    lines.append("")
    lines.append(f"Run time: {status_json['run_at']}")
    lines.append("")
    lines.append("## Summary")
    lines.append(f"- Blacklist: {status_json['blacklist']}")
    lines.append(f"- Whitelist: {status_json['whitelist']}")
    lines.append(f"- Total: {status_json['total']}")

    with open(md_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
