"""
04 — Classes
============

THEORY (read first)
-------------------
1. The constructor is `__init__(self, ...)`. `self` is `this`, but every method must take
   it EXPLICITLY as its first parameter. There's no `new`: you write Foo(1), not new Foo(1).
2. Attributes are created by assigning in __init__ (self.x = x). You don't have to declare
   fields first, unless you use @dataclass (see 8).
3. Nothing is truly private. By convention, `_name` means "internal, don't touch", and
   `__name` triggers name-mangling. (TS has `private` / `#private`.)
4. @property turns a method into a computed attribute (TS `get total()`). Access it
   without parentheses: obj.total
5. @classmethod receives the class (`cls`) instead of an instance. Use it for alternative
   constructors like Message.from_dict(d). @staticmethod gets neither (TS `static`).
6. "Dunder" (double-underscore) methods hook into the language:
       __repr__  debug text (what print/REPL shows)     __str__  str(obj)
       __len__   len(obj)                               __eq__   obj == other
       __iter__  for x in obj                           __getitem__  obj[i]
       __call__  obj()   (an instance you can call like a function)
7. Inheritance: `class Child(Parent):`, then super().__init__(...) or super().method().
   Duck typing: Python cares whether an object HAS the method, not about its declared
   type. To describe an interface, use typing.Protocol (the TS `interface` equivalent)
   or abc.ABC with @abstractmethod.
8. @dataclass generates __init__, __repr__ and __eq__ from annotated fields. Use it for
   plain data holders (like a TS interface plus a constructor). For a mutable default,
   write `field(default_factory=list)`.

TS / JS  ->  Python
-------------------
    class A { constructor(public x: number) {} }    @dataclass
                                                    class A:
                                                        x: int
    this.x                                          self.x
    new A(1)                                        A(1)
    get total() { ... }                             @property
                                                    def total(self): ...
    static fromJSON(d) { ... }                      @classmethod
                                                    def from_dict(cls, d): ...
    class B extends A                               class B(A):
    super.greet()                                   super().greet()
    interface LLM { generate(p: string): string }   class LLM(Protocol):
                                                        def generate(self, p: str) -> str: ...
    toString()                                      __str__  (and __repr__ for debugging)

WHY THIS MATTERS FOR AI
-----------------------
SDKs are class-based (OpenAI(), client.chat.completions...). You'll model messages,
conversations, prompt templates and swappable model backends as classes. Pydantic
models (file 08) are classes too.

Run:  uv run python src/04_classes.py
"""
import re
from dataclasses import dataclass

from _check import eq, raises, run


# Q1 ─────────────────────────────────────────────────────────────────────────────
# A dataclass for a chat message. The fields are done; implement the two methods.
#   Message("user", "hi").to_dict()                       -> {"role": "user", "content": "hi"}
#   Message.from_dict({"role": "user", "content": "hi"})  -> Message(role="user", content="hi")
@dataclass
class Message:
    role: str
    content: str

    def to_dict(self) -> dict[str, str]:
        raise NotImplementedError  # TODO

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> "Message":
        raise NotImplementedError  # TODO: return cls(...)


# Q2 ─────────────────────────────────────────────────────────────────────────────
# A Conversation holds a system prompt and a list of Message objects.
#   c = Conversation("Be nice")
#   c.add("user", "hi there"); c.add("assistant", "hello")
#   len(c)         -> 2
#   c.last(1)      -> [Message("assistant", "hello")]
#   c.word_count   -> 3          (a @property: total words in all message contents)
#   c.to_api()     -> [{"role": "system", "content": "Be nice"},
#                      {"role": "user", "content": "hi there"},
#                      {"role": "assistant", "content": "hello"}]
#                     (leave out the system message if the system prompt is "")
class Conversation:
    def __init__(self, system: str = ""):
        raise NotImplementedError  # TODO: store `system` and an empty list of messages

    def add(self, role: str, content: str) -> None:
        raise NotImplementedError  # TODO

    def last(self, n: int) -> list[Message]:
        raise NotImplementedError  # TODO

    @property
    def word_count(self) -> int:
        raise NotImplementedError  # TODO

    def to_api(self) -> list[dict[str, str]]:
        raise NotImplementedError  # TODO

    def __len__(self) -> int:
        raise NotImplementedError  # TODO


# Q3 ─────────────────────────────────────────────────────────────────────────────
# A reusable prompt template.
#   t = PromptTemplate("Translate {text} to {language}. Again: {text}")
#   t.variables                          -> ["language", "text"]  (@property, sorted, unique)
#   t.format(text="hi", language="Hindi")  -> "Translate hi to Hindi. Again: hi"
#   t.format(text="hi")                  -> raises ValueError (missing: language)
#
# Hint: re.findall(r"\{(\w+)\}", self.template) finds the names; set() removes duplicates.
class PromptTemplate:
    def __init__(self, template: str):
        self.template = template

    @property
    def variables(self) -> list[str]:
        raise NotImplementedError  # TODO

    def format(self, **values: str) -> str:
        raise NotImplementedError  # TODO


# Q4 ─────────────────────────────────────────────────────────────────────────────
# Inheritance and polymorphism: swappable "model" backends. BaseLLM is done.
#   EchoLLM:   name = "echo";   generate(prompt) returns f"echo: {prompt}"
#   ShoutLLM:  inherits from EchoLLM; name = "shout"; generate() calls the parent's
#              generate via super() and returns it UPPERCASED with "!" on the end:
#              ShoutLLM().generate("hi") -> "ECHO: HI!"
class BaseLLM:
    name = "base"  # a class attribute, shared by all instances (like TS `static`-ish)

    def generate(self, prompt: str) -> str:
        raise NotImplementedError("subclasses must implement generate()")

    def __repr__(self) -> str:
        return f"<{type(self).__name__} name={self.name!r}>"


class EchoLLM(BaseLLM):
    pass  # TODO


class ShoutLLM(EchoLLM):
    pass  # TODO


# ── Tests (don't edit) ──────────────────────────────────────────────────────────
def test_q1_message():
    eq(Message("user", "hi").to_dict(), {"role": "user", "content": "hi"})
    eq(Message.from_dict({"role": "assistant", "content": "yo"}), Message("assistant", "yo"))


def test_q2_conversation():
    c = Conversation("Be nice")
    c.add("user", "hi there")
    c.add("assistant", "hello")
    eq(len(c), 2)
    eq(c.last(1), [Message("assistant", "hello")])
    eq(c.word_count, 3)
    eq(c.to_api(), [
        {"role": "system", "content": "Be nice"},
        {"role": "user", "content": "hi there"},
        {"role": "assistant", "content": "hello"},
    ])
    empty = Conversation()
    eq(empty.to_api(), [])
    eq(len(empty), 0)


def test_q3_prompt_template():
    t = PromptTemplate("Translate {text} to {language}. Again: {text}")
    eq(t.variables, ["language", "text"])
    eq(t.format(text="hi", language="Hindi"), "Translate hi to Hindi. Again: hi")
    raises(ValueError, t.format, text="hi")


def test_q4_inheritance():
    eq(EchoLLM().generate("hi"), "echo: hi")
    eq(ShoutLLM().generate("hi"), "ECHO: HI!")
    eq(repr(ShoutLLM()), "<ShoutLLM name='shout'>")
    assert isinstance(ShoutLLM(), BaseLLM)
    eq([m.generate("x") for m in (EchoLLM(), ShoutLLM())], ["echo: x", "ECHO: X!"])


if __name__ == "__main__":
    run(globals())
