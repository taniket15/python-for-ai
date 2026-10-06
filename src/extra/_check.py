"""Tiny test runner for the warm-up exercises. You don't need to edit this file."""
import sys
from pathlib import Path


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
    """Replace your answers with the ones in src/extra/solutions/<same file name>."""
    exercise = Path(namespace["__file__"])
    solution = exercise.parent / "solutions" / exercise.name
    print(f"Testing the official solution: src/extra/solutions/{exercise.name}\n")
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
