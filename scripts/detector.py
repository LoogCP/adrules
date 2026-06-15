import re


HOSTS = re.compile(

    r"^(0\.0\.0\.0|127\.0\.0\.1)\s+"

)

DOMAIN = re.compile(

    r"^[a-z0-9.-]+\.[a-z]{2,}$",

    re.I,

)


def detect(content: str):

    lines = []

    for line in content.splitlines():

        line = line.strip()

        if not line:

            continue

        if line.startswith("#"):

            continue

        if line.startswith("!"):

            continue

        lines.append(line)

        if len(lines) >= 50:

            break

    if not lines:

        return "unknown"

    score = {

        "hosts": 0,

        "adblock": 0,

        "wildcard": 0,

        "domain": 0,

    }

    for line in lines:

        if HOSTS.match(line):

            score["hosts"] += 1

        if line.startswith("||"):

            score["adblock"] += 1

        if line.startswith("@@||"):

            score["adblock"] += 1

        if line.startswith("*."):

            score["wildcard"] += 1

        if DOMAIN.match(line):

            score["domain"] += 1

    return max(

        score,

        key=score.get,

    )
