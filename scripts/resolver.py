from scripts.config_loader import source_order_map


def resolve_rules(rows):

    order_map = source_order_map()

    grouped = {}

    for url, domain, action in rows:

        if domain not in grouped:
            grouped[domain] = []

        grouped[domain].append(
            (action, order_map.get(url, 999999))
        )

    resolved = {}

    for domain, rules in grouped.items():

        whites = [r for r in rules if r[0] == "white"]

        if whites:

            best = min(whites, key=lambda x: x[1])

            resolved[domain] = "white"

            continue

        best = min(rules, key=lambda x: x[1])

        resolved[domain] = "black"

    return resolved


def split_rules(resolved):

    black = []
    white = []

    for d in sorted(resolved):

        if resolved[d] == "white":
            white.append(d)
        else:
            black.append(d)

    return black, white
