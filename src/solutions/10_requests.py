# Solutions for 10_requests.py
# Test them with:  uv run python src/10_requests.py --solution
import requests


def build_headers(api_key: str | None) -> dict[str, str]:
    if not api_key:
        raise ValueError("an API key is required")
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


def fetch_json(url: str, params: dict | None = None, http=requests):
    response = http.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def get_post_titles(user_id: int, http=requests) -> list[str]:
    posts = fetch_json(f"{BASE_URL}/posts", params={"userId": user_id}, http=http)
    titles = []
    for post in posts:
        titles.append(post["title"])
    return titles


def safe_fetch(url: str, http=requests):
    try:
        return fetch_json(url, http=http)
    except requests.RequestException:
        return None
