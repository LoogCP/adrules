import idna


COMMENT_PREFIX = (
    "#",
    "!",
)


def normalize_domain(domain: str):

    domain = domain.strip()

    domain = domain.lower()

    domain = domain.rstrip(".")

    domain = domain.replace("^", "")

    domain = domain.replace("*.", "")

    domain = domain.strip()

    if not domain:
        return None

    if "#" in domain:
        domain = domain.split(
            "#",
            1,
        )[0]

    if "$" in domain:
        domain = domain.split(
            "$",
            1,
        )[0]

    invalid_chars = (
        "/",
        ":",
        " ",
        "\t",
    )

    if any(
        char in domain
        for char in invalid_chars
    ):
        return None

    try:
        return idna.encode(
            domain
        ).decode()

    except Exception:
        return None


def parse_line(line: str):

    line = line.strip()

    if not line:
        return None

    if line.startswith(
        COMMENT_PREFIX
    ):
        return None

    is_whitelist = False

    if line.startswith("@@"):

        is_whitelist = True

        line = line[2:]

    # AdGuard Home
    if line.startswith("address=/"):

        line = line.removeprefix(
            "address=/"
        )

        parts = line.split("/")

        if not parts:
            return None

        line = parts[0]

    # AdBlock
    elif line.startswith("||"):

        line = line.removeprefix(
            "||"
        )

    # hosts
    elif line.startswith(
        "0.0.0.0 "
    ):

        parts = line.split()

        if len(parts) < 2:
            return None

        line = parts[1]

    elif line.startswith(
        "127.0.0.1 "
    ):

        parts = line.split()

        if len(parts) < 2:
            return None

        line = parts[1]

    domain = normalize_domain(
        line
    )

    if not domain:
        return None

    return (
        domain,
        is_whitelist,
    )


def parse(content: str):

    blacklist = set()

    whitelist = set()

    for line in content.splitlines():

        result = parse_line(
            line
        )

        if not result:
            continue

        domain, is_whitelist = result

        if is_whitelist:

            whitelist.add(
                domain
            )

        else:

            blacklist.add(
                domain
            )

    blacklist -= whitelist

    return {
        "black": blacklist,
        "white": whitelist,
    }
