import re
import sys
import yaml
import urllib.request
from urllib.error import URLError
from concurrent.futures import ThreadPoolExecutor, as_completed

# ---------- 正则预编译 ----------
_RE_HOSTS   = re.compile(r'^(?:0\.0\.0\.0|127\.0\.0\.1|0)\s+(\S+)', re.IGNORECASE)
_RE_ADBLOCK = re.compile(r'^(@@)?\|\|([^/$^*]+)')   # 捕获 @@ 和域名
_RE_PURE    = re.compile(r'^(\*?\.?[a-zA-Z0-9\-_.]+\.[a-zA-Z]{2,})(?:[#\$\^\s]|$)')

def is_valid_domain(domain: str) -> bool:
    return re.fullmatch(r'[a-zA-Z0-9\-.]+\.[a-zA-Z]{2,}', domain) is not None

def extract_rule_from_line(line: str) -> tuple[str, bool] | None:
    """
    从一行中提取 (域名, 是否为白名单) 或 None
    keep_wildcard: 是否保留泛域名（domain 规则始终保留，hosts 无泛域名）
    """
    line = line.strip()
    if not line or line.startswith(('!', '#', '[')):
        return None
    # 去掉行内注释
    if ' #' in line:
        line = line[:line.index(' #')]

    # 1. hosts 格式（一定是黑名单）
    m = _RE_HOSTS.match(line)
    if m:
        domain = m.group(1).lower().split('#')[0].strip()
        if is_valid_domain(domain):
            return (domain, False)          # False 表示黑名单
        return None

    # 2. AdBlock 规则（可能带 @@ 白名单前缀）
    m = _RE_ADBLOCK.search(line)
    if m:
        is_white = (m.group(1) == '@@')
        domain = m.group(2).lower().strip()
        if is_valid_domain(domain):
            return (domain, is_white)
        return None

    # 3. 纯域名 / 泛域名（无修饰符的默认视为黑名单）
    m = _RE_PURE.match(line)
    if m:
        domain = m.group(1).lower().lstrip('.')
        # 泛域名保留 *，否则只保留普通域名
        if domain.startswith('*.'):
            if is_valid_domain(domain[2:]):
                return (domain, False)
        else:
            if is_valid_domain(domain):
                return (domain, False)
    return None

# ---------- 下载 ----------
def download_rules(url: str, retries=2) -> list[str]:
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=60) as resp:
                return resp.read().decode('utf-8', errors='ignore').splitlines()
        except Exception as e:
            print(f"下载 {url} 失败 (尝试 {attempt+1}/{retries+1}): {e}", file=sys.stderr)
    return []

def batch_download(urls: list[str], max_workers=5) -> list[list[str]]:
    results = [None] * len(urls)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_idx = {executor.submit(download_rules, url): i for i, url in enumerate(urls)}
        for future in as_completed(future_to_idx):
            idx = future_to_idx[future]
            results[idx] = future.result()
    return results

# ---------- 白名单覆盖判断 ----------
def build_whitelist_lookup(whitelist: set[str]):
    """拆分为精确白名单和泛域名后缀白名单"""
    exact = set()
    wild_suffixes = set()
    for rule in whitelist:
        if rule.startswith('*.'):
            wild_suffixes.add(rule[2:])
        elif rule.startswith('.'):
            wild_suffixes.add(rule[1:])
        else:
            exact.add(rule)
    return exact, wild_suffixes

def is_whitelisted(domain: str, exact: set[str], wild_suffixes: set[str]) -> bool:
    if domain in exact:
        return True
    parts = domain.split('.')
    for i in range(1, len(parts)):      # 从第二个标签开始检查后缀
        suffix = '.'.join(parts[i:])
        if suffix in wild_suffixes and domain != suffix:
            return True
    return False

# ---------- 主流程 ----------
def main():
    with open('sources.yaml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    host_urls = config['sources'].get('hosts', [])
    domain_urls = config['sources'].get('domain', [])

    print(f"下载 {len(host_urls)} 个 hosts 源，{len(domain_urls)} 个 domain 源")

    # 并行下载
    all_host_lines = []
    for lines in batch_download(host_urls):
        all_host_lines.extend(lines)

    all_domain_lines = []
    for lines in batch_download(domain_urls):
        all_domain_lines.extend(lines)

    print(f"原始行数 -> hosts: {len(all_host_lines)}, domain: {len(all_domain_lines)}")

    # 收集域名
    black_hosts = set()
    black_domain = set()
    white_set = set()

    for line in all_host_lines:
        res = extract_rule_from_line(line)
        if res:
            domain, is_white = res
            # hosts 源理论上全黑，但严谨处理
            if not is_white:
                black_hosts.add(domain)
            else:
                white_set.add(domain)

    for line in all_domain_lines:
        res = extract_rule_from_line(line)
        if res:
            domain, is_white = res
            if is_white:
                white_set.add(domain)
            else:
                black_domain.add(domain)

    print(f"提取 -> hosts 黑 {len(black_hosts)}, domain 黑 {len(black_domain)}, 白 {len(white_set)}")

    # 合并黑名单
    all_black = black_hosts.union(black_domain)

    # 构建白名单查找结构
    exact_w, wild_w = build_whitelist_lookup(white_set)
    print(f"白名单结构：精确 {len(exact_w)}，泛域名后缀 {len(wild_w)}")

    # 去重：从黑名单中移除被白名单覆盖的域名
    final_black = set()
    for d in all_black:
        if not is_whitelisted(d, exact_w, wild_w):
            final_black.add(d)

    print(f"白名单剔除后，黑名单 {len(final_black)} 条")

    # 排序
    def sort_key(d: str):
        return d.replace('*.', '').lstrip('.')

    sorted_black = sorted(final_black, key=sort_key)
    sorted_white = sorted(white_set, key=sort_key)

    # 输出
    with open('blacklist.txt', 'w', encoding='utf-8') as f:
        for d in sorted_black:
            f.write(f"{d}\n")

    with open('whitelist.txt', 'w', encoding='utf-8') as f:
        for d in sorted_white:
            f.write(f"{d}\n")

    print(f"生成 blacklist.txt ({len(sorted_black)} 条) 和 whitelist.txt ({len(sorted_white)} 条)")

if __name__ == '__main__':
    main()
