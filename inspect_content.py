import urllib.request, re
from collections import defaultdict

def analyze_games():
    url = "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Game/Game.list"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    print("=== GAMES & GAMING PLATFORMS (Blackmatrix7) ===")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            lines = [l.decode('utf-8', errors='ignore').strip() for l in resp]
            
        categories = defaultdict(list)
        for line in lines:
            if not line or line.startswith(('#', '//', '!')): continue
            domain = line.split(',')[-1].strip().lower()
            
            if any(k in domain for k in ['steam', 'valvesoftware']): categories['Steam / Valve'].append(domain)
            elif any(k in domain for k in ['riot', 'leagueoflegends', 'pvp.net', 'val']): categories['Riot Games (LoL/Valorant)'].append(domain)
            elif any(k in domain for k in ['epicgames', 'unrealengine', 'fortnite']): categories['Epic Games / Fortnite'].append(domain)
            elif any(k in domain for k in ['ea.com', 'origin', 'electronicarts', 'respawn']): categories['EA / Origin / Apex'].append(domain)
            elif any(k in domain for k in ['blizzard', 'battle.net', 'activision', 'callofduty']): categories['Blizzard / Activision'].append(domain)
            elif any(k in domain for k in ['playstation', 'sonyentnetwork', 'playstationnetwork']): categories['Sony PlayStation'].append(domain)
            elif any(k in domain for k in ['xbox', 'xboxlive', 'xboxservices']): categories['Microsoft Xbox'].append(domain)
            elif any(k in domain for k in ['nintendo', 'nintendowifi']): categories['Nintendo'].append(domain)
            elif any(k in domain for k in ['garena', 'sea.com']): categories['Garena / Free Fire'].append(domain)
            elif any(k in domain for k in ['roblox', 'rbxcdn']): categories['Roblox'].append(domain)
            elif any(k in domain for k in ['ubisoft', 'ubi.com']): categories['Ubisoft / Uplay'].append(domain)
            elif any(k in domain for k in ['rockstar', 'rsg.sc']): categories['Rockstar Games (GTA)'].append(domain)
            elif any(k in domain for k in ['genshin', 'hoyoverse', 'mihoyo']): categories['HoYoverse (Genshin/HSR)'].append(domain)
            elif any(k in domain for k in ['unity', 'unreal', 'godot']): categories['Game Engines / Middleware'].append(domain)
            else: categories['Other Game Servers / CDNs'].append(domain)

        for cat, doms in sorted(categories.items()):
            print(f"\n[{cat}] - {len(doms)} endpoints/domains")
            print("Sample:", ", ".join(doms[:4]))
    except Exception as e:
        print(f"Error reading games: {e}")

def analyze_media():
    url = "https://raw.githubusercontent.com/1-stream/1stream-public-utils/main/stream.xray.list"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    print("\n\n=== STREAMING & MEDIA PLATFORMS (1-Stream) ===")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            lines = [l.decode('utf-8', errors='ignore').strip() for l in resp]
            
        platforms = defaultdict(list)
        current_section = "General / Unknown"
        for line in lines:
            if line.startswith("# >") or line.startswith("# -"):
                current_section = line.replace("#", "").replace(">", "").replace("-", "").strip()
                continue
            if not line or line.startswith('#'): continue
            clean = re.sub(r'["\',]', '', line).strip()
            if clean:
                platforms[current_section].append(clean)

        for plat, doms in sorted(platforms.items()):
            print(f"\n[{plat}] - {len(doms)} endpoints")
            print("Sample:", ", ".join(doms[:3]))
    except Exception as e:
        print(f"Error reading media: {e}")

analyze_games()
analyze_media()
