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

# Mga ayaw mong ma-block (Bughosts/Telemetry exceptions)
bughosts = {"crashlytics.com", "firebaseio.com", "firebase-settings.crashlytics.com"}

print("Fetching Tier 1 (Pro)...")
pro_set = fetch_domains("https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/pro.txt") - bughosts

print("Fetching Tier 2 (Pro++)...")
proplus_set = fetch_domains("https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/pro.plus.txt") - bughosts

print("Fetching Tier 3 (Ultimate)...")
ultimate_set = fetch_domains("https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/ultimate.txt") - bughosts

# Pure Deltas (Tinatanggal ang duplicates mula sa lower tiers)
delta_standard = proplus_set - pro_set
delta_advanced = ultimate_set - proplus_set

# Write raw files
with open("custom_data/ads-normal", "w") as f:
    f.write("\n".join(sorted(list(pro_set))) + "\n")

with open("custom_data/ads-standard", "w") as f:
    f.write("\n".join(sorted(list(delta_standard))) + "\n")

with open("custom_data/ads-advanced", "w") as f:
    f.write("\n".join(sorted(list(delta_advanced))) + "\n")

print(f"ads-normal: {len(pro_set)} base domains")
print(f"ads-standard: {len(delta_standard)} unique delta domains")
print(f"ads-advanced: {len(delta_advanced)} unique delta domains")
