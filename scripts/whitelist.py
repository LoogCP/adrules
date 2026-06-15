from scripts.config_loader import load_whitelist


def build_whitelist(parsed_white, external_white):

    cfg = load_whitelist()

    result = set()

    result.update(parsed_white)
    result.update(external_white)
    result.update(cfg["domains"])

    return result


def get_external_sources():

    return load_whitelist()["sources"]
