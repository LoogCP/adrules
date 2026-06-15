import asyncio

from scripts.config_loader import load_upstreams
from scripts.fetcher import fetch_all
from scripts.parser import parse
from scripts.database import (
    init_db,
    upsert_source,
    insert_rules,
    load_all_rules,
    add_run_stats,
)
from scripts.resolver import resolve_rules, split_rules
from scripts.exporter import write_files
from scripts.tracker import write_status, write_markdown
from scripts.git_commit import commit_and_push
from scripts.utils import utc_now


async def run():

    await init_db()

    urls = load_upstreams()

    fetched = await fetch_all(urls)

    sources_status = []

    before_merge_count = 0

    for item in fetched:

        if item["status"] == 200:

            parsed = parse(item["content"])

            black = parsed["black"]
            white = parsed["white"]

            before_merge_count += len(black) + len(white)

            await insert_rules(
                source_id=1,
                blacklist=black,
                whitelist=white,
            )

            await upsert_source(
                url=item["url"],
                hash_value=item.get("sha256"),
                etag=item.get("etag"),
                last_modified=item.get("last_modified"),
                last_fetch_at=utc_now(),
                status=200,
                entry_count=len(black) + len(white),
            )

            sources_status.append(
                {
                    "url": item["url"],
                    "status": 200,
                    "entry_count": len(black) + len(white),
                }
            )

        else:

            sources_status.append(
                {
                    "url": item["url"],
                    "status": item["status"],
                }
            )

    rows = await load_all_rules()

    resolved = resolve_rules(rows)

    blacklist, whitelist = split_rules(resolved)

    write_files(blacklist, whitelist)

    total = len(blacklist) + len(whitelist)

    dedup_rate = (
        1 - total / max(before_merge_count, 1)
    )

    status = {
        "run_at": utc_now(),
        "sources": sources_status,
        "before_merge": before_merge_count,
        "blacklist": len(blacklist),
        "whitelist": len(whitelist),
        "total": total,
        "dedup_rate": round(dedup_rate, 4),
    }

    write_status(
        sources_status,
        before_merge_count,
        blacklist,
        whitelist,
    )

    write_markdown(status)

    await add_run_stats(
        run_time=status["run_at"],
        sources=len(urls),
        before_merge=before_merge_count,
        blacklist=len(blacklist),
        whitelist=len(whitelist),
        dedup_rate=status["dedup_rate"],
    )

    commit_and_push()


if __name__ == "__main__":
    asyncio.run(run())
