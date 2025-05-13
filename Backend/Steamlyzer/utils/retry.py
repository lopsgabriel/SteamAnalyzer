import time, requests

def make_request_with_retry(url, retries=5, delay=1):
    for attempt in range(retries):
        resp = requests.get(url)
        if resp.status_code == 200:
            return resp.json()
        time.sleep(delay)
        delay *= 2
    return None

