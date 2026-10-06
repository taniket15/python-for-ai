# Solutions for 07_chatbot_memory.py
# Test them with:  uv run python src/07_chatbot_memory.py --solution


def trim_history(messages: list[dict], max_messages: int) -> list[dict]:
    window = messages[-max_messages:]  # slicing makes a new list
    while window and window[0]["role"] != "user":
        window = window[1:]
    return window


class ChatBot:
    def __init__(self, llm, system: str = "", max_messages: int = 20):
        self.llm = llm
        self.system = system
        self.max_messages = max_messages
        self.history: list[dict] = []

    def send(self, text: str) -> str:
        self.history.append({"role": "user", "content": text})

        messages = []
        if self.system:
            messages.append({"role": "system", "content": self.system})
        messages += trim_history(self.history, self.max_messages)

        reply = self.llm(messages)
        self.history.append({"role": "assistant", "content": reply})
        return reply

    def reset(self) -> None:
        self.history = []


def openai_llm(client):
    def llm(messages: list[dict]) -> str:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            max_completion_tokens=1024,
        )
        return response.choices[0].message.content or ""

    return llm
