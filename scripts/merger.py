from collections import defaultdict


def build_domain_depth(

    domain,

):

    return len(

        domain.split(

            "."

        )

    )


def merge_rules(

    rows,

):

    grouped = defaultdict(

        list

    )

    for (

        domain,

        action,

        source_order,

        depth,

    ) in rows:

        grouped[domain].append(

            {

                "action": action,

                "source_order": source_order,

                "depth": depth,

            }

        )

    merged = {}

    for domain, rules in grouped.items():

        rules.sort(

            key=lambda x: (

                x["source_order"],

                -x["depth"],

            )

        )

        whitelist = [

            x

            for x in rules

            if x["action"]

            == "white"

        ]

        if whitelist:

            merged[domain] = {

                "action": "white",

                "source_order": min(

                    x["source_order"]

                    for x in whitelist

                ),

                "depth": build_domain_depth(

                    domain

                ),

            }

            continue

        merged[domain] = {

            "action": "black",

            "source_order": rules[0][

                "source_order"

            ],

            "depth": build_domain_depth(

                domain

            ),

        }

    return merged


def split_rules(

    merged,

):

    blacklist = []

    whitelist = []

    for domain in sorted(

        merged.keys()

    ):

        action = merged[domain][

            "action"

        ]

        if action == "white":

            whitelist.append(

                domain

            )

        else:

            blacklist.append(

                domain

            )

    return (

        blacklist,

        whitelist,

    )
