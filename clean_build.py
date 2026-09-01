import urllib.request, re
DOMAIN_REGEX = re.compile(r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$')

def fetch(url, filename, exclusions=set()):
    domains = set()
    print(f"[*] Downloading {filename}...")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=30) as resp:
        for line in resp:
            line = line.decode('utf-8', errors='ignore').strip()
            if not line or line.startswith(('#', '!', '//')): continue
            # Nililinis nito ang adblock format (||domain^) para maging pure domain
            line = re.sub(r'^(0\.0\.0\.0|127\.0\.0\.1|\|\||\*\.)\s*', '', line)
            line = re.sub(r'[\^@#].*$', '', line).strip().lower()
            if DOMAIN_REGEX.match(line) and line not in exclusions:
                domains.add(line)
    with open(f"custom_data/{filename}", "w") as f:
        f.write("\n".join(sorted(list(domains))) + "\n")
    print(f"[+] Saved {filename}")

bughosts = {"crashlytics.com", "firebaseio.com", "firebase-settings.crashlytics.com"}

# UPDATED URL: Changed to adblock/multi.txt (Formerly normal.txt)
fetch("https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/multi.txt", "ads", bughosts)
fetch("https://nsfw.oisd.nl/domainswild", "porn")

# Manual target lists
with open("custom_data/ph", "w") as f:
    f.write("\n".join(["domain:ph", "gcash.com", "mynt.xyz", "paymaya.com", "maya.ph", "unionbankph.com", "rcbc.com", "rcbconlinebanking.com", "securitybank.com", "landbank.com", "bdo.com.ph", "bpi.com.ph", "pldt.com", "pldthome.com", "convergeict.com", "grab.com", "smtickets.com", "vivamax.net", "iwanttfc.com"]) + "\n")

with open("custom_data/private", "w") as f:
    f.write("localhost\nlocal\n")
