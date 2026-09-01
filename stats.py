import urllib.request

targets = {
    "Blackmatrix Game (Full)": "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Game/Game.list",
    "1-Stream Media (Full)": "https://raw.githubusercontent.com/1-stream/1stream-public-utils/main/stream.xray.list",
    "ACL4SSR Steam": "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/Steam.list",
    "ACL4SSR Media": "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/Streaming.list"
}

for name, url in targets.items():
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            lines = [l.decode('utf-8', errors='ignore').strip() for l in resp if l.strip()]
            valid_rules = [l for l in lines if not l.startswith(('#', '//', '!'))]
            print(f"{name}: {len(valid_rules)} total functional rules (Lines: {len(lines)})")
    except Exception as e:
        print(f"{name}: Error ({e})")
