import urllib.request, os, re

def process_feed(url, filename, exclusions=None):
    if exclusions is None: exclusions = set()
    domains = set()
    print(f"[*] Downloading {filename}...")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            for line in resp:
                line = line.decode('utf-8', errors='ignore').strip()
                if not line or line.startswith(('#', '!', '//')): continue
                line = re.sub(r'^(0\.0\.0\.0|127\.0\.0\.1|\|\||\*\.)\s*', '', line)
                line = re.sub(r'[\^@#].*$', '', line).strip().lower()
                if len(line) > 3 and line not in exclusions:
                    domains.add(f"domain:{line}")
    except Exception as e:
        print(f"[!] Error {filename}: {e}")
    
    with open(f"custom_data/{filename}", "w") as f:
        f.write("\n".join(sorted(list(domains))) + "\n")
    print(f"[+] Successfully compiled {len(domains)} rules for {filename}")

bughosts = {"crashlytics.com", "firebaseio.com", "firebase-settings.crashlytics.com"}

# Process valid feeds with explicit domain: prefix
process_feed("https://raw.githubusercontent.com/hagezi/dns-blocklists/main/wildcard/normal.txt", "set-ads", bughosts)
process_feed("https://nsfw.oisd.nl/domainswild", "set-porn")

# PH SmartRoute
with open("custom_data/set-ph", "w") as f:
    f.write("domain:ph\ndomain:gcash.com\ndomain:mynt.xyz\ndomain:paymaya.com\ndomain:maya.ph\ndomain:unionbankph.com\ndomain:rcbc.com\ndomain:rcbconlinebanking.com\ndomain:securitybank.com\ndomain:landbank.com\ndomain:bdo.com.ph\ndomain:bpi.com.ph\ndomain:pldt.com\ndomain:pldthome.com\ndomain:convergeict.com\ndomain:grab.com\ndomain:smtickets.com\ndomain:vivamax.net\ndomain:iwanttfc.com\n")

# Proxy Targets
with open("custom_data/set-proxy", "w") as f:
    f.write("domain:google.com\ndomain:googleapis.com\ndomain:gvt1.com\ndomain:gvt2.com\ndomain:ggpht.com\ndomain:googleusercontent.com\ndomain:ytimg.com\ndomain:facebook.com\ndomain:fbcdn.net\ndomain:messenger.com\ndomain:instagram.com\ndomain:cdninstagram.com\ndomain:netflix.com\ndomain:nflxext.com\ndomain:nflxvideo.net\n")

# Local
with open("custom_data/private", "w") as f:
    f.write("domain:localhost\ndomain:local\n")
