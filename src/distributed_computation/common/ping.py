import requests


# Function to ping website
def ping_website(url: str) -> tuple[str, str]:
    try:
        response = requests.get(url[0], timeout=1)
        # is_display = random.randint(0, 1000)
        # if is_display >= 0:
        #     print(f'{datetime.datetime.now().isoformat()} : \t\t {url[0]} \t returned \t {response.status_code}')
        return url[0], response.status_code
    except Exception as e:
        return url[0], str(e)