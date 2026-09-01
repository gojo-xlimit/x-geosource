import urllib.request, re

DOMAIN_REGEX = re.compile(r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$')

def fetch_domains(url):
    domains = set()
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            for line in resp:
                line = line.decode('utf-8', errors='ignore').strip()
                if not line or line.startswith(('#', '!', '//')): continue
                line = re.sub(r'^(0\.0\.0\.0|127\.0\.0\.1|\|\||\*\.)\s*', '', line)
                line = re.sub(r'[\^@#].*$', '', line).strip().lower()
                if DOMAIN_REGEX.match(line):
                    domains.add(line)
        return domains
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return set()

def prune_subdomains(domain_set):
    sorted_domains = sorted(list(domain_set), key=lambda d: len(d.split('.')))
    root_set = set()
    for dom in sorted_domains:
        parts = dom.split('.')
        is_sub = False
        for i in range(1, len(parts) - 1):
            parent = '.'.join(parts[i:])
            if parent in root_set:
                is_sub = True
                break
        if not is_sub:
            root_set.add(dom)
    return root_set

bughosts = {"crashlytics.com", "firebaseio.com", "firebase-settings.crashlytics.com"}

print("Fetching Tier 1 (Pro)...")
pro_raw = fetch_domains("https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/pro.txt") - bughosts
pro_pruned = prune_subdomains(pro_raw)
print(f"Tier 1: {len(pro_raw)} -> {len(pro_pruned)} compressed root domains")

print("Fetching Tier 2 (Pro++)...")
proplus_raw = fetch_domains("https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/pro.plus.txt") - bughosts
proplus_pruned = prune_subdomains(proplus_raw)
print(f"Tier 2: {len(proplus_raw)} -> {len(proplus_pruned)} compressed root domains")

print("Fetching Tier 3 (Ultimate)...")
ultimate_raw = fetch_domains("https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/ultimate.txt") - bughosts
ultimate_pruned = prune_subdomains(ultimate_raw)
print(f"Tier 3: {len(ultimate_raw)} -> {len(ultimate_pruned)} compressed root domains")

# Write standalone full sets (with domain: wildcard prefix)
with open("custom_data/ads-normal", "w") as f:
    f.write("\n".join(f"domain:{d}" for d in sorted(list(pro_pruned))) + "\n")

with open("custom_data/ads-standard", "w") as f:
    f.write("\n".join(f"domain:{d}" for d in sorted(list(proplus_pruned))) + "\n")

with open("custom_data/ads-advanced", "w") as f:
    f.write("\n".join(f"domain:{d}" for d in sorted(list(ultimate_pruned))) + "\n")
