import os, asyncio

STEAM_API_KEY = os.getenv("STEAM_API_KEY", "")
HEADERS = {"Accept-Language": "en-US,en;q=0.9"}
SEMAPHORE = asyncio.Semaphore(5)