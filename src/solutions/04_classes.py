# Solutions for 04_classes.py
# Test them with:  uv run python src/04_classes.py --solution
import re
from dataclasses import dataclass


@dataclass
class Message:
    role: str
    content: str

    def to_dict(self) -> dict[str, str]:
        return {"role": self.role, "content": self.content}

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> "Message":
        return cls(data["role"], data["content"])


class Conversation:
    def __init__(self, system: str = ""):
        self.system = system
        self.messages = []

    def add(self, role: str, content: str) -> None:
        self.messages.append(Message(role, content))

    def last(self, n: int) -> list[Message]:
        return self.messages[-n:]

    @property
    def word_count(self) -> int:
        total = 0
        for message in self.messages:
            total += len(message.content.split())
        return total

    def to_api(self) -> list[dict[str, str]]:
        result = []
        if self.system:
            result.append({"role": "system", "content": self.system})
        for message in self.messages:
            result.append(message.to_dict())
        return result

    def __len__(self) -> int:
        return len(self.messages)


class PromptTemplate:
    def __init__(self, template: str):
        self.template = template

    @property
    def variables(self) -> list[str]:
        names = re.findall(r"\{(\w+)\}", self.template)
        return sorted(set(names))

    def format(self, **values: str) -> str:
        missing = []
        for name in self.variables:
            if name not in values:
                missing.append(name)
        if missing:
            raise ValueError(f"missing variables: {missing}")
        return self.template.format(**values)


class EchoLLM(BaseLLM):
    name = "echo"

    def generate(self, prompt: str) -> str:
        return f"echo: {prompt}"


class ShoutLLM(EchoLLM):
    name = "shout"

    def generate(self, prompt: str) -> str:
        text = super().generate(prompt)
        return text.upper() + "!"
