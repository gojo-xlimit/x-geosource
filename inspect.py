import urllib.request

urls = {
    "blackmatrix_games": "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Game/Game.list",
    "1stream_media": "https://raw.githubusercontent.com/1-stream/1stream-public-utils/main/stream.xray.list",
    "govedu_sample": "https://raw.githubusercontent.com/thu-jzl/GovEduDomains/main/active_domains.txt",
    "acl4ssr_sample": "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/Steam.list"
}

for name, url in urls.items():
    print(f"=== {name} ===")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            lines = [resp.readline().decode('utf-8', errors='ignore').strip() for _ in range(15)]
            for line in lines:
                if line:
                    print(line)
    except Exception as e:
        print(f"Error: {e}")
    print()
