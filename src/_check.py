"""Tiny test runner + fakes for the exercises. You don't need to edit this file."""
import copy
import sys
from pathlib import Path
from types import SimpleNamespace


def eq(actual, expected):
    if actual != expected:
        raise AssertionError(f"expected {expected!r}, got {actual!r}")


def raises(exc_type, fn, *args, **kwargs):
    try:
        fn(*args, **kwargs)
    except exc_type:
        return
    raise AssertionError(f"expected {exc_type.__name__} to be raised")


def load_solution(namespace: dict) -> None:
    """Replace your answers with the ones in src/solutions/<same file name>."""
    exercise = Path(namespace["__file__"])
    solution = exercise.parent / "solutions" / exercise.name
    print(f"Testing the official solution: src/solutions/{exercise.name}\n")
    exec(solution.read_text(encoding="utf-8"), namespace)


def run(namespace: dict) -> None:
    if "--solution" in sys.argv:
        load_solution(namespace)
    tests = [fn for name, fn in namespace.items() if name.startswith("test_") and callable(fn)]
    passed = 0
    for test in tests:
        label = test.__name__.removeprefix("test_")
        try:
            test()
        except NotImplementedError:
            print(f"⬜ {label}: not started")
        except Exception as e:
            print(f"❌ {label}: {type(e).__name__}: {e}")
        else:
            passed += 1
            print(f"✅ {label}")
    print(f"\n{passed}/{len(tests)} passed")
    if tests and passed == len(tests):
        print("🎉 All done! Move on to the next file.")


class FakeOpenAI:
    """Pretends to be `openai.OpenAI()` so tests run offline and cost nothing.

    reply: a string, or a function(kwargs) -> string
    parsed: dict used to build `message.parsed` for `chat.completions.parse(...)`
    """

    def __init__(self, reply="Hello!", finish_reason="stop", parsed=None):
        self.reply = reply
        self.finish_reason = finish_reason
        self.parsed = parsed
        self.calls: list[dict] = []
        self.chat = SimpleNamespace(completions=SimpleNamespace(create=self._create, parse=self._parse))

    def _response(self, content, parsed=None):
        message = SimpleNamespace(role="assistant", content=content, parsed=parsed, refusal=None)
        return SimpleNamespace(
            choices=[SimpleNamespace(index=0, message=message, finish_reason=self.finish_reason)],
            usage=SimpleNamespace(prompt_tokens=10, completion_tokens=5, total_tokens=15),
        )

    def _create(self, **kwargs):
        self.calls.append(copy.deepcopy(kwargs))
        text = self.reply(kwargs) if callable(self.reply) else self.reply
        return self._response(text)

    def _parse(self, **kwargs):
        self.calls.append({**copy.deepcopy({k: v for k, v in kwargs.items() if k != "response_format"}),
                           "response_format": kwargs.get("response_format")})
        model_cls = kwargs["response_format"]
        return self._response(None, parsed=model_cls.model_validate(self.parsed))
