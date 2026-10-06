"""
06 — Error Handling
===================

THEORY (read first)
-------------------
1. try / except / else / finally
       try:
           risky()
       except ValueError as e:      # catch a SPECIFIC type
           ...
       except (KeyError, TypeError):
           ...
       else:                        # runs only if NO exception happened
           ...
       finally:                     # always runs (cleanup)
           ...
2. You can have several typed `except` clauses. In TS you get one `catch (e: unknown)`
   and have to `instanceof`-check inside it.
3. Never use a bare `except:`. It even swallows Ctrl+C. Catch specific exceptions;
   save `except Exception` for top-level boundaries (a request handler, a CLI main).
4. raise ValueError("msg")      ≈ throw new Error("msg")
   `raise` on its own           ≈ re-throw the current exception
   raise MyError("x") from e    ≈ new Error("x", { cause: e })   (sets e.__cause__)
5. Custom exceptions: `class MyError(Exception): ...`. Build a hierarchy so callers can
   catch something broad (LLMError) or narrow (RateLimited).
6. Common built-ins: ValueError (bad value), TypeError (wrong type), KeyError (missing
   dict key), IndexError, FileNotFoundError, TimeoutError, json.JSONDecodeError
   (a subclass of ValueError).
7. EAFP, "Easier to Ask Forgiveness than Permission": Python style is usually to TRY
   and catch, rather than check everything first.
8. AI-specific: API calls fail ALL the time. You get rate limits (429), overloaded
   servers (5xx) and timeouts, and those are worth RETRYING with exponential backoff.
   Don't retry a 400, because that's a bug in your request. The OpenAI SDK raises
   openai.RateLimitError, openai.APITimeoutError, openai.APIConnectionError and
   openai.APIStatusError (with .status_code), and it already retries twice by default
   (max_retries=2). LLM output is unreliable too, so parsing it needs error handling.

TS / JS  ->  Python
-------------------
    try {} catch (e) {} finally {}       try: ... except X as e: ... finally: ...
    if (e instanceof HttpError) {}       except HttpError as e:
    throw new Error("x")                 raise ValueError("x")
    throw e                              raise
    new Error("x", { cause: e })         raise MyError("x") from e
    class MyErr extends Error {}         class MyErr(Exception): pass

Run:  uv run python src/06_errors.py
"""
import json
import time

from _check import eq, raises, run


# Q1 ─────────────────────────────────────────────────────────────────────────────
# Parse JSON text. If it's invalid, return `default` instead of crashing.
#
#   safe_json_loads('{"a": 1}')            -> {"a": 1}
#   safe_json_loads("not json", default={}) -> {}
def safe_json_loads(text: str, default=None):
    raise NotImplementedError  # TODO


# Q2 ─────────────────────────────────────────────────────────────────────────────
# A custom exception hierarchy. LLMError is done. Make RateLimited:
#   - store `retry_after` as an attribute
#   - have the message "rate limited, retry after {retry_after}s"
#     (pass it to super().__init__(message))
class LLMError(Exception):
    """Base class for every error our LLM code raises."""


class RateLimited(LLMError):
    def __init__(self, retry_after: float):
        raise NotImplementedError  # TODO


# Q3 ─────────────────────────────────────────────────────────────────────────────
# Retry with exponential backoff. Call fn() up to `max_attempts` times.
#   - If it raises one of the `retry_on` exceptions and attempts are left:
#     sleep(2 ** attempt) and try again (attempt counts from 0, so waits are 1, 2, 4...)
#   - On the LAST attempt, let the exception propagate (re-raise it).
#   - Any OTHER exception propagates immediately, with no retry.
#   - Return fn()'s result as soon as it succeeds.
#
# `sleep` is a parameter so tests don't actually wait (dependency injection).
# Hint: `except retry_on:` works with a tuple of exception classes.
def with_retry(fn, max_attempts: int = 3, retry_on=(RateLimited, TimeoutError), sleep=time.sleep):
    raise NotImplementedError  # TODO


# Q4 ─────────────────────────────────────────────────────────────────────────────
# Read a required setting from a config dict. If the key is missing, raise
# ConfigError("missing setting: <key>") FROM the original KeyError (use `from`).
class ConfigError(Exception):
    pass


def get_setting(config: dict, key: str):
    raise NotImplementedError  # TODO


# ── Tests (don't edit) ──────────────────────────────────────────────────────────
def test_q1_safe_json_loads():
    eq(safe_json_loads('{"a": 1}'), {"a": 1})
    eq(safe_json_loads("not json"), None)
    eq(safe_json_loads("not json", default={}), {})


def test_q2_rate_limited():
    e = RateLimited(5)
    eq(e.retry_after, 5)
    eq(str(e), "rate limited, retry after 5s")
    assert isinstance(e, LLMError), "RateLimited should be a kind of LLMError"
    try:
        raise RateLimited(1)
    except LLMError:
        pass  # catching the base class works


def test_q3_with_retry():
    waits, attempts = [], []

    def flaky():
        attempts.append(1)
        if len(attempts) < 3:
            raise TimeoutError("slow")
        return "ok"

    eq(with_retry(flaky, sleep=waits.append), "ok")
    eq(waits, [1, 2])

    waits.clear()

    def always_limited():
        raise RateLimited(1)

    raises(RateLimited, with_retry, always_limited, max_attempts=3, sleep=waits.append)
    eq(waits, [1, 2])

    calls = []

    def bad_request():
        calls.append(1)
        raise ValueError("bad prompt")

    raises(ValueError, with_retry, bad_request, sleep=waits.append)
    eq(len(calls), 1)


def test_q4_get_setting():
    eq(get_setting({"model": "x"}, "model"), "x")
    try:
        get_setting({}, "api_key")
    except ConfigError as e:
        eq(str(e), "missing setting: api_key")
        assert isinstance(e.__cause__, KeyError), "use `raise ... from e`"
    else:
        raise AssertionError("expected ConfigError")


if __name__ == "__main__":
    run(globals())
