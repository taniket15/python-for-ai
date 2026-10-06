"""
10 — Calling APIs with `requests`
=================================

THEORY (read first)
-------------------
1. `requests` is the classic HTTP client. It's SYNCHRONOUS (blocks until the response
   arrives), so think axios without promises. For async there's `httpx`
   (httpx.AsyncClient), which is what the OpenAI SDK uses internally.
2. requests.get(url, params={...}, headers={...}, timeout=10)
   requests.post(url, json={...}, timeout=10)  # json= serializes AND sets Content-Type
   (data= sends form-encoded data instead.)
3. ⚠️ requests has NO default timeout. A hung server hangs your program forever, so
   always pass timeout=.
4. Like fetch, a 404 or 500 does NOT raise by default. Call response.raise_for_status()
   to turn 4xx/5xx into a requests.HTTPError. (axios throws; fetch and requests don't.)
5. response.status_code, response.json() (parses the body, synchronously), response.text,
   response.headers (a case-insensitive dict).
6. requests.Session() reuses connections and shared headers (like an axios instance).
7. Exceptions: requests.RequestException is the base class of HTTPError, Timeout and
   ConnectionError. Catch the base when "any network problem" should be handled the same.
8. When an official SDK exists (openai), prefer it: it handles auth, retries, types and
   streaming. Use raw HTTP for services without an SDK, webhooks, or pulling data for RAG.

TS / JS  ->  Python
-------------------
    await fetch(`${url}?${new URLSearchParams(p)}`)      requests.get(url, params=p, timeout=10)
    await fetch(url, { method: "POST",                   requests.post(url, json=data,
      body: JSON.stringify(data), headers })                 headers=headers, timeout=10)
    if (!res.ok) throw new Error(...)                    res.raise_for_status()
    await res.json()                                     res.json()
    res.status                                           res.status_code
    axios.create({ headers })                            s = requests.Session(); s.headers.update(h)

TESTING TRICK: the functions below take `http=requests` as a parameter. In real use you
don't pass it, so the real module is used. The tests pass a fake object with a .get()
method (duck typing again), so no network is needed.

Run tests:  uv run python src/10_requests.py
Live:       uv run python src/10_requests.py --live   (calls a free test API)
"""
import sys

import requests

from _check import eq, raises, run

BASE_URL = "https://jsonplaceholder.typicode.com"  # a free fake REST API for practice


# Q1 ─────────────────────────────────────────────────────────────────────────────
# Build the headers for an authenticated JSON API:
#   {"Authorization": "Bearer <api_key>", "Content-Type": "application/json"}
# Raise ValueError if api_key is empty or None.
def build_headers(api_key: str | None) -> dict[str, str]:
    raise NotImplementedError  # TODO


# Q2 ─────────────────────────────────────────────────────────────────────────────
# GET `url` with the given query params and timeout=10, raise on HTTP errors,
# and return the parsed JSON body.
#   res = http.get(url, params=params, timeout=10)
def fetch_json(url: str, params: dict | None = None, http=requests):
    raise NotImplementedError  # TODO


# Q3 ─────────────────────────────────────────────────────────────────────────────
# Using fetch_json, GET f"{BASE_URL}/posts" with params {"userId": user_id}.
# The API returns a list of dicts like {"id": 1, "userId": 1, "title": "...", "body": "..."}.
# Return just the titles. (Remember to pass `http` along!)
def get_post_titles(user_id: int, http=requests) -> list[str]:
    raise NotImplementedError  # TODO


# Q4 ─────────────────────────────────────────────────────────────────────────────
# Like fetch_json, but return None on ANY requests error (connection, timeout, 4xx/5xx).
# Hint: reuse fetch_json and catch requests.RequestException.
def safe_fetch(url: str, http=requests):
    raise NotImplementedError  # TODO


# ── Fakes + Tests (don't edit) ──────────────────────────────────────────────────
class FakeResponse:
    def __init__(self, data, status_code=200):
        self._data = data
        self.status_code = status_code

    def json(self):
        return self._data

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"{self.status_code} error")


class FakeHTTP:
    def __init__(self, data=None, status_code=200, error=None):
        self.data, self.status_code, self.error = data, status_code, error
        self.calls = []

    def get(self, url, **kwargs):
        self.calls.append((url, kwargs))
        if self.error:
            raise self.error
        return FakeResponse(self.data, self.status_code)


def test_q1_build_headers():
    eq(build_headers("abc"), {"Authorization": "Bearer abc", "Content-Type": "application/json"})
    raises(ValueError, build_headers, "")
    raises(ValueError, build_headers, None)


def test_q2_fetch_json():
    fake = FakeHTTP(data={"ok": True})
    eq(fetch_json("https://x.test/a", params={"q": "ai"}, http=fake), {"ok": True})
    url, kwargs = fake.calls[0]
    eq(url, "https://x.test/a")
    eq(kwargs.get("params"), {"q": "ai"})
    eq(kwargs.get("timeout"), 10)
    raises(requests.HTTPError, fetch_json, "https://x.test/a", http=FakeHTTP(status_code=500))


def test_q3_get_post_titles():
    fake = FakeHTTP(data=[{"id": 1, "userId": 1, "title": "first"}, {"id": 2, "userId": 1, "title": "second"}])
    eq(get_post_titles(1, http=fake), ["first", "second"])
    url, kwargs = fake.calls[0]
    eq(url, f"{BASE_URL}/posts")
    eq(kwargs.get("params"), {"userId": 1})


def test_q4_safe_fetch():
    eq(safe_fetch("https://x.test", http=FakeHTTP(data=[1, 2])), [1, 2])
    eq(safe_fetch("https://x.test", http=FakeHTTP(status_code=404)), None)
    eq(safe_fetch("https://x.test", http=FakeHTTP(error=requests.ConnectionError("down"))), None)
    eq(safe_fetch("https://x.test", http=FakeHTTP(error=requests.Timeout("slow"))), None)


if __name__ == "__main__":
    if "--live" in sys.argv:
        for title in get_post_titles(1)[:3]:
            print("-", title)
    else:
        run(globals())
