import re, requests
from Steamlyzer.utils.constants import STEAM_API_KEY
from Steamlyzer.utils.retry import make_request_with_retry

def resolve_vanity_url(custom_url: str) -> str | None:
    url = (f"https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/"
           f"?key={STEAM_API_KEY}&vanityurl={custom_url}")
    data = make_request_with_retry(url)
    if data and data.get("response", {}).get("success", 0) == 1: #A utilização do .get() evita que o programa quebre com erro
        return data["response"]["steamid"]
    return None

def verify_steamid_or_vanity_url(raw: str) -> str | None:
    if not isinstance(raw, str):
        return None
    # steamcommunity.com/profiles/ID64
    if m := re.search(r"steamcommunity\.com/profiles/(\d+)", raw):
        return m.group(1)
    # steamcommunity.com/id/custom
    if m := re.search(r"steamcommunity\.com/id/([\w-]+)", raw):
        return resolve_vanity_url(m.group(1))
    # id64 direto
    if re.fullmatch(r"\d{17}", raw):
        return raw
    # só vanity
    if re.fullmatch(r"[\w-]+", raw):
        return resolve_vanity_url(raw)
    return None