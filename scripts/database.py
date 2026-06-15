import aiosqlite

from scripts.constants import DATABASE_FILE


async def connect_db():

    DATABASE_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    db = await aiosqlite.connect(
        DATABASE_FILE
    )

    db.row_factory = aiosqlite.Row

    return db


async def init_db():

    async with await connect_db() as db:

        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS source (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE,
                hash TEXT,
                etag TEXT,
                last_modified TEXT,
                last_fetch_at TEXT,
                status INTEGER,
                entry_count INTEGER
            )
            """
        )

        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS source_rule (
                source_id INTEGER,
                domain TEXT,
                action TEXT,
                updated_at TEXT,
                PRIMARY KEY (
                    source_id,
                    domain,
                    action
                )
            )
            """
        )

        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS run_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_time TEXT,
                sources INTEGER,
                before_merge INTEGER,
                blacklist INTEGER,
                whitelist INTEGER,
                dedup_rate REAL
            )
            """
        )

        await db.commit()


async def upsert_source(
    url,
    hash_value,
    etag,
    last_modified,
    last_fetch_at,
    status,
    entry_count,
):

    async with await connect_db() as db:

        await db.execute(
            """
            INSERT INTO source (
                url,
                hash,
                etag,
                last_modified,
                last_fetch_at,
                status,
                entry_count
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(url) DO UPDATE SET
                hash=excluded.hash,
                etag=excluded.etag,
                last_modified=excluded.last_modified,
                last_fetch_at=excluded.last_fetch_at,
                status=excluded.status,
                entry_count=excluded.entry_count
            """
        , (
            url,
            hash_value,
            etag,
            last_modified,
            last_fetch_at,
            status,
            entry_count,
        ))

        await db.commit()


async def get_source(url):

    async with await connect_db() as db:

        cursor = await db.execute(
            "SELECT * FROM source WHERE url=?",
            (url,),
        )

        return await cursor.fetchone()


async def insert_rules(
    source_id,
    blacklist,
    whitelist,
):

    async with await connect_db() as db:

        rows = []

        for d in blacklist:
            rows.append((source_id, d, "black"))

        for d in whitelist:
            rows.append((source_id, d, "white"))

        await db.executemany(
            """
            INSERT OR REPLACE INTO source_rule
            (source_id, domain, action, updated_at)
            VALUES (?, ?, ?, datetime('now'))
            """,
            rows,
        )

        await db.commit()


async def load_all_rules():

    async with await connect_db() as db:

        cursor = await db.execute(
            """
            SELECT s.url, sr.domain, sr.action
            FROM source_rule sr
            JOIN source s ON s.id = sr.source_id
            """
        )

        return await cursor.fetchall()


async def add_run_stats(
    run_time,
    sources,
    before_merge,
    blacklist,
    whitelist,
    dedup_rate,
):

    async with await connect_db() as db:

        await db.execute(
            """
            INSERT INTO run_stats (
                run_time,
                sources,
                before_merge,
                blacklist,
                whitelist,
                dedup_rate
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """
        , (
            run_time,
            sources,
            before_merge,
            blacklist,
            whitelist,
            dedup_rate,
        ))

        await db.commit()
