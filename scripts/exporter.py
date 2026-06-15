from scripts.constants import OUTPUT_DIR


def write_files(blacklist, whitelist):

    OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

    block_file = OUTPUT_DIR / "blocklist.txt"
    white_file = OUTPUT_DIR / "whitelist.txt"

    with open(block_file, "w", encoding="utf-8") as f:
        f.write("\n".join(sorted(blacklist)))

    with open(white_file, "w", encoding="utf-8") as f:
        f.write("\n".join(sorted(whitelist)))
