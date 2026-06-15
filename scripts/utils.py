from datetime import datetime, timezone, timedelta
import hashlib

# 北京时间 UTC+8
CST = timezone(timedelta(hours=8))


def utc_now() -> str:
    return datetime.now(CST).isoformat()


def sha256_text(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def safe_int(value, default=0):
    try:
        return int(value)
    except:
        return default


def safe_float(value, default=0.0):
    try:
        return float(value)
    except:
        return default


def domain_depth(domain: str) -> int:
    return len(domain.split("."))
