# Solutions for 06_errors.py
# Test them with:  uv run python src/06_errors.py --solution
import json
import time


def safe_json_loads(text: str, default=None):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return default


class RateLimited(LLMError):
    def __init__(self, retry_after: float):
        super().__init__(f"rate limited, retry after {retry_after}s")
        self.retry_after = retry_after


def with_retry(fn, max_attempts: int = 3, retry_on=(RateLimited, TimeoutError), sleep=time.sleep):
    for attempt in range(max_attempts):
        try:
            return fn()
        except retry_on:
            is_last_attempt = attempt == max_attempts - 1
            if is_last_attempt:
                raise  # give up: re-raise the same error
            sleep(2 ** attempt)  # wait 1s, 2s, 4s, ...


def get_setting(config: dict, key: str):
    try:
        return config[key]
    except KeyError as e:
        raise ConfigError(f"missing setting: {key}") from e
