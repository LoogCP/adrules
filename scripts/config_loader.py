import yaml

from scripts.constants import UPSTREAM_FILE
from scripts.constants import WHITELIST_FILE


def _load_yaml(path):

    if not path.exists():
        return {}

    with open(
        path,
        "r",
        encoding="utf-8",
    ) as f:

        return yaml.safe_load(f) or {}


def load_upstreams() -> list[str]:

    data = _load_yaml(
        UPSTREAM_FILE
    )

    return [
        url.strip()
        for url in data.get(
            "sources",
            [],
        )
        if isinstance(url, str)
        and url.strip()
    ]


def load_whitelist() -> dict:

    data = _load_yaml(
        WHITELIST_FILE
    )

    domains = {
        domain.strip().lower()
        for domain in data.get(
            "domains",
            [],
        )
        if isinstance(domain, str)
        and domain.strip()
    }

    sources = [
        url.strip()
        for url in data.get(
            "sources",
            [],
        )
        if isinstance(url, str)
        and url.strip()
    ]

    return {
        "domains": domains,
        "sources": sources,
    }


def source_order_map() -> dict:

    upstreams = load_upstreams()

    return {
        url: index
        for index, url in enumerate(upstreams)
    }
