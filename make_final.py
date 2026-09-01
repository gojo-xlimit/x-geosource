import urllib.request, re

DOMAIN_REGEX = re.compile(r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$')

def fetch_adblock(url, filename, exclusions=set()):
    domains = set()
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
    except Exception as e:
        print(f"Error {filename}: {e}")

def fetch_clash_games(url, filename):
    rules = set()
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            for line in resp:
                line = line.decode('utf-8', errors='ignore').strip()
                if not line or line.startswith(('#', '//')): continue
                parts = line.split(',')
                if len(parts) >= 2:
                    rtype = parts[0].strip().upper()
                    target = parts[1].strip().lower()
                    if rtype == "DOMAIN-SUFFIX":
                        rules.add(f"domain:{target}")
                    elif rtype == "DOMAIN":
                        rules.add(f"full:{target}")
                    elif rtype == "DOMAIN-KEYWORD":
                        rules.add(f"keyword:{target}")
        with open(f"custom_data/{filename}", "w") as f:
            f.write("\n".join(sorted(list(rules))) + "\n")
    except Exception as e:
        print(f"Error {filename}: {e}")

def fetch_clean_stream(url, filename):
    rules = set()
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            for line in resp:
                line = line.decode('utf-8', errors='ignore').strip()
                if not line or line.startswith(('#', '//', '!')): continue
                cleaned = re.sub(r'["\',]', '', line).strip()
                if cleaned.startswith(('domain:', 'full:', 'keyword:', 'regexp:')) or DOMAIN_REGEX.match(cleaned):
                    rules.add(cleaned)
        with open(f"custom_data/{filename}", "w") as f:
            f.write("\n".join(sorted(list(rules))) + "\n")
    except Exception as e:
        print(f"Error {filename}: {e}")

bughosts = {"crashlytics.com", "firebaseio.com", "firebase-settings.crashlytics.com"}

fetch_adblock("https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/pro.txt", "ads", bughosts)
fetch_adblock("https://nsfw.oisd.nl/domainswild", "porn")
fetch_clash_games("https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Game/Game.list", "games")
fetch_clean_stream("https://raw.githubusercontent.com/1-stream/1stream-public-utils/main/stream.xray.list", "media")

ph_data = [
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
    f.write("\n".join(ph_data) + "\n")

with open("custom_data/private", "w") as f:
    f.write("domain:localhost\ndomain:local\n")
