import requests

# Function to ping website
def ping_website(url: str) -> tuple[str, str]:
    try:
        response = requests.get(url, timeout=1)
        return url, response.status_code
    except Exception as e:
        return url, str(e)