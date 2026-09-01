import urllib.request, re

DOMAIN_REGEX = re.compile(r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$')

def fetch_and_clean_adblock(url, filename, exclusions=set()):
    domains = set()
    print(f"[*] Fetching Security Feed ({filename})...")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            for line in resp:
                line = line.decode('utf-8', errors='ignore').strip()
                if not line or line.startswith(('#', '!', '//')): continue
                line = re.sub(r'^(0\.0\.0\.0|127\.0\.0\.1|\|\||\*\.)\s*', '', line)
                line = re.sub(r'[\^@#].*$', '', line).strip().lower()
                if DOMAIN_REGEX.match(line) and line not in exclusions:
                    domains.add(line)
        with open(f"custom_data/{filename}", "w") as f:
            f.write("\n".join(sorted(list(domains))) + "\n")
        print(f"[✓] {filename}: {len(domains)} active domains")
    except Exception as e:
        print(f"[!] Error {filename}: {e}")

def fetch_and_normalize_clash(url, filename):
    domains = set()
    print(f"[*] Fetching & Normalizing Clash/Surge Feed ({filename})...")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            for line in resp:
                line = line.decode('utf-8', errors='ignore').strip()
                if not line or line.startswith(('#', '//')): continue
                # Match DOMAIN-SUFFIX, DOMAIN, DOMAIN-KEYWORD
                parts = line.split(',')
                if len(parts) >= 2:
                    rule_type = parts[0].strip().upper()
                    target = parts[1].strip().lower()
                    if rule_type == "DOMAIN-SUFFIX":
                        domains.add(f"domain:{target}")
                    elif rule_type == "DOMAIN":
                        domains.add(f"full:{target}")
                    elif rule_type == "DOMAIN-KEYWORD":
                        domains.add(f"keyword:{target}")
                elif DOMAIN_REGEX.match(line):
                    domains.add(f"domain:{line.lower()}")
        with open(f"custom_data/{filename}", "w") as f:
            f.write("\n".join(sorted(list(domains))) + "\n")
        print(f"[✓] {filename}: {len(domains)} rules normalized")
    except Exception as e:
        print(f"[!] Error {filename}: {e}")

def fetch_raw_xray(url, filename):
    domains = set()
    print(f"[*] Fetching Xray List ({filename})...")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            for line in resp:
                line = line.decode('utf-8', errors='ignore').strip()
                if line and not line.startswith(('#', '//')):
                    domains.add(line)
        with open(f"custom_data/{filename}", "w") as f:
            f.write("\n".join(sorted(list(domains))) + "\n")
        print(f"[✓] {filename}: {len(domains)} entries")
    except Exception as e:
        print(f"[!] Error {filename}: {e}")

bughosts = {"crashlytics.com", "firebaseio.com", "firebase-settings.crashlytics.com"}

# 1. SECURITY & ADULT
fetch_and_clean_adblock("https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/pro.txt", "ads", bughosts)
fetch_and_clean_adblock("https://nsfw.oisd.nl/domainswild", "porn")

# 2. GAMING (Blackmatrix7 Aggregated Games Rule)
fetch_and_normalize_clash("https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Game/Game.list", "games")

# 3. STREAMING (1-Stream Xray List)
fetch_raw_xray("https://raw.githubusercontent.com/1-stream/1stream-public-utils/main/stream.xray.list", "media")

# 4. CURATED PH & ASIA FINTECH/INFRA (Zero-Hallucination Local Mapping)
ph_rules = [
    "domain:ph", "domain:gov.ph", "domain:mil.ph", "domain:edu.ph",
    "domain:gcash.com", "domain:mynt.xyz", "domain:paymaya.com", "domain:maya.ph",
    "domain:unionbankph.com", "domain:rcbc.com", "domain:rcbconlinebanking.com",
    "domain:securitybank.com", "domain:landbank.com", "domain:bdo.com.ph",
    "domain:bpi.com.ph", "domain:pldt.com", "domain:pldthome.com",
    "domain:smart.com.ph", "domain:globe.com.ph", "domain:dito.ph",
    "domain:convergeict.com", "domain:grab.com", "domain:shopee.ph",
    "domain:lazada.com.ph", "domain:smtickets.com", "domain:vivamax.net", "domain:iwanttfc.com"
]
with open("custom_data/ph", "w") as f:
    f.write("\n".join(ph_rules) + "\n")

# 5. LAN / BYPASS
with open("custom_data/private", "w") as f:
    f.write("domain:localhost\ndomain:local\n")
