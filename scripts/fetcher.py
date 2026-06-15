import asyncio

import aiohttp

from tenacity import retry, stop_after_attempt, wait_exponential

from scripts.constants import (
    FETCH_TIMEOUT,
    MAX_CONCURRENT,
    MAX_RETRIES,
    USER_AGENT,
)

from scripts.database import get_source

from scripts.utils import sha256_text


@retry(
    stop=stop_after_attempt(MAX_RETRIES),
    wait=wait_exponential(multiplier=2, min=2, max=20),
)
async def request(session, url):

    headers = {
        "User-Agent": USER_AGENT,
    }

    source = await get_source(url)

    if source:

        if source["etag"]:
            headers["If-None-Match"] = source["etag"]

        if source["last_modified"]:
            headers["If-Modified-Since"] = source["last_modified"]

    return await session.get(url, headers=headers)


async def fetch_one(semaphore, session, url):

    async with semaphore:

        try:

            resp = await request(session, url)

            if resp.status == 304:

                return {
                    "url": url,
                    "status": 304,
                }

            if resp.status != 200:

                return {
                    "url": url,
                    "status": resp.status,
                }

            text = await resp.text(errors="ignore")

            return {
                "url": url,
                "status": 200,
                "content": text,
                "sha256": sha256_text(text),
                "etag": resp.headers.get("ETag"),
                "last_modified": resp.headers.get("Last-Modified"),
            }

        except Exception as e:

            return {
                "url": url,
                "status": -1,
                "error": str(e),
            }


async def fetch_all(urls):

    semaphore = asyncio.Semaphore(MAX_CONCURRENT)

    timeout = aiohttp.ClientTimeout(total=FETCH_TIMEOUT)

    async with aiohttp.ClientSession(timeout=timeout) as session:

        tasks = [
            fetch_one(semaphore, session, url)
            for url in urls
        ]

        return await asyncio.gather(*tasks)
