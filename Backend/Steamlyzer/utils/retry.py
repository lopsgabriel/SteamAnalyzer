import time, requests

def make_request_with_retry(url, retries=5, delay=1):
    """Faz uma requisição GET e tenta novamente se a resposta for diferente de 200."""
    for attempt in range(retries):
        resp = requests.get(url)
        if resp.status_code == 200:
            return resp.json()
        time.sleep(delay)
        delay *= 2
    return None

