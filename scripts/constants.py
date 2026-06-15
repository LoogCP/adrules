from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

CONFIG_DIR = BASE_DIR / "config"

DATA_DIR = BASE_DIR / "data"

OUTPUT_DIR = BASE_DIR / "output"

UPSTREAM_FILE = CONFIG_DIR / "upstream.yaml"

WHITELIST_FILE = CONFIG_DIR / "whitelist.yaml"

DATABASE_FILE = DATA_DIR / "dns_rules.db"

FETCH_TIMEOUT = 60

MAX_CONCURRENT = 10

MAX_RETRIES = 3

USER_AGENT = (
    "Mozilla/5.0 "
    "(GitHubActions DNS Rules Builder)"
)

SCHEDULE = "0 */6 * * *"
