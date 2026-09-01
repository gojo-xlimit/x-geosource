import os

source_file = os.path.expanduser("~/storage/downloads/FQDN_SAN_Root_Domain.txt")
out_dir = "custom_data"

categories = {
    "ph-routing": [".ph", "pldt", "converge", "abs-cbn", "gma", "rappler", "inquirer", "bdo", "bpi"],
    "multiverse-games": ["moonton", "riot", "epicgames", "steampowered", "roblox", "ea.com", "playstation", "xbox", "nintendo", "games", "gaming", "battlenet", "activision", "ubisoft"],
    "shopping-fintech": ["alipay", "taobao", "shopee", "lazada", "amazon", "alibaba", "bank", "pay"],
    "entertainment": ["netflix", "spotify", "disney", "hbo", "youtube", "tiktok", "twitch", "viu", "paramount", "peacock", "crunchyroll", "viva"],
    "productivity-ai": ["openai", "anthropic", "notion", "canva", "chatgpt", "midjourney", "perplexity", "claude", "ai.", ".ai"],
    "security-tools": ["kaspersky", "eset", "avast", "nordvpn", "expressvpn", "mullvad", "proton", "mcafee", "bitdefender", "security"],
    "education-learning": ["canvas", "blackboard", "khanacademy", "coursera", "udemy", "edx", "schoology", "quizlet"],
    "global-ecosystem": ["google", "microsoft", "apple", "cloudflare", "akamai", "fastly", "aws", "azure", "oracle", "ibm", "cisco", "meta", "facebook", "twitter", "instagram"]
}

files = {k: open(os.path.join(out_dir, k), 'w') for k in categories.keys()}
files["uncategorized"] = open(os.path.join(out_dir, "uncategorized"), 'w')

with open(source_file, 'r') as f:
    for line in f:
        domain = line.strip().lower()
        if not domain: continue
        
        matched = False
        for cat, keywords in categories.items():
            if any(kw in domain for kw in keywords):
                files[cat].write(domain + "\n")
                matched = True
                break
        
        if not matched:
            files["uncategorized"].write(domain + "\n")

for f in files.values():
    f.close()

print("Domains successfully split into custom tags.")
