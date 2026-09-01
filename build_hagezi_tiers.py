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

bughosts = {"crashlytics.com", "firebaseio.com", "firebase-settings.crashlytics.com"}

print("Fetching Tier 1: Pro...")
pro_set = fetch_domains("https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/pro.txt") - bughosts

print("Fetching Tier 2: Pro++...")
proplus_set = fetch_domains("https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/pro.plus.txt") - bughosts

print("Fetching Tier 3: Ultimate...")
ultimate_set = fetch_domains("https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/ultimate.txt") - bughosts

# Calculate Deltas
delta_standard = proplus_set - pro_set
delta_advanced = ultimate_set - proplus_set

# Write ads-normal
with open("custom_data/ads-normal", "w") as f:
    f.write("\n".join(sorted(list(pro_set))) + "\n")

# Write ads-standard (Includes ads-normal)
with open("custom_data/ads-standard", "w") as f:
    f.write("include:ads-normal\n")
    f.write("\n".join(sorted(list(delta_standard))) + "\n")

# Write ads-advanced (Includes ads-standard)
with open("custom_data/ads-advanced", "w") as f:
    f.write("include:ads-standard\n")
    f.write("\n".join(sorted(list(delta_advanced))) + "\n")

print(f"Tier 1 (ads-normal): {len(pro_set)} base domains")
print(f"Tier 2 (ads-standard): {len(delta_standard)} delta domains (+ include:ads-normal)")
print(f"Tier 3 (ads-advanced): {len(delta_advanced)} delta domains (+ include:ads-standard)")
