from user_agents import parse
import random

DESKTOP_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version} Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{version} Safari/605.1.15"
]

MOBILE_AGENTS = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{version} Mobile/15E148 Safari/604.1"
]

def get_random_agent(device="desktop"):
    if device == "mobile":
        template = random.choice(MOBILE_AGENTS)
    else:
        template = random.choice(DESKTOP_AGENTS)
    
    # Generate random version numbers
    if "{version}" in template:
        version = f"{random.randint(100, 125)}.0.{random.randint(1000, 9999)}.{random.randint(1, 200)}"
        return template.format(version=version)
    return template

def parse_user_agent(ua_string):
    return parse(ua_string)