import time, requests

def make_request_with_retry(url, retries=5, delay=1):
    for attempt in range(retries):
        resp = requests.get(url)
        if resp.status_code == 200:
            return resp.json()
        time.sleep(delay)
        delay *= 2
    return None

# def make_request_with_retry(url):
#     # Logica de retries
#     retries = 5
#     delay = 1  # Delay inicial de 1 segundo
#     for i in range(retries):
#         print(f"Tentando novamente ({i+1}/{retries})... em {url}")
#         response = requests.get(url)
#         if response.status_code == 200:
#             return response.json()
#         time.sleep(delay)
#         delay *= 2 
#     return None