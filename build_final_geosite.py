import urllib.request, re

DOMAIN_REGEX = re.compile(r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$')

def fetch_and_clean(url, exclusions=None):
    print(f"[*] Fetching {url.split('/')[-1]}...")
    domains = set()
    if exclusions is None: exclusions = set()
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            for line in resp:
                line = line.decode('utf-8', errors='ignore').strip()
                if not line or line.startswith(('#', '!', '//')): continue
                line = re.sub(r'^(0\.0\.0\.0|127\.0\.0\.1|\|\||\*\.)\s*', '', line)
                line = re.sub(r'[\^@#].*$', '', line).strip().lower()
                if DOMAIN_REGEX.match(line) and line not in exclusions:
                    domains.add(line)
    except Exception as e:
        print(f"[!] Error: {e}")
    return domains

bughosts = {"crashlytics.com", "firebaseio.com", "firebase-settings.crashlytics.com"}

# MOBILE OPTIMIZED: HaGeZi Normal (Ads + Active Malware only, no TIF bloat)
ads = fetch_and_clean("https://raw.githubusercontent.com/hagezi/dns-blocklists/main/wildcard/normal.txt", bughosts)
with open("custom_data/set-ads", "w") as f: f.write("\n".join(sorted(list(ads))) + "\n")

# ADULT: OISD NSFW (Same as before)
porn = fetch_and_clean("https://nsfw.oisd.nl/domainswild")
with open("custom_data/set-porn", "w") as f: f.write("\n".join(sorted(list(porn))) + "\n")

# TARGET: PH SmartRoute
ph_domains = [
    "domain:ph", "gcash.com", "mynt.xyz", "paymaya.com", "maya.ph", 
    "unionbankph.com", "rcbc.com", "rcbconlinebanking.com", "securitybank.com", 
    "landbank.com", "bdo.com.ph", "bpi.com.ph", "pldt.com", "pldthome.com", 
    "convergeict.com", "grab.com", "smtickets.com", "vivamax.net", "iwanttfc.com"
]
with open("custom_data/set-ph", "w") as f: f.write("\n".join(ph_domains) + "\n")

# TARGET: Proxy
proxy_domains = [
    "domain:google.com", "domain:googleapis.com", "domain:gvt1.com", "domain:gvt2.com", 
    "domain:ggpht.com", "domain:googleusercontent.com", "domain:ytimg.com",
    "domain:facebook.com", "domain:fbcdn.net", "domain:messenger.com", 
    "domain:instagram.com", "domain:cdninstagram.com", "domain:netflix.com", 
    "domain:nflxext.com", "domain:nflxvideo.net"
]
with open("custom_data/set-proxy", "w") as f: f.write("\n".join(proxy_domains) + "\n")

# CORE: Local
with open("custom_data/private", "w") as f: f.write("localhost\nlocal\n")
