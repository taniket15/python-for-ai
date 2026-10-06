# Solutions for 05_call_llm.py
# Test them with:  uv run python src/05_call_llm.py --solution


def build_request(prompt: str, system: str | None = None, max_tokens: int = 1024) -> dict:
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    return {
        "model": MODEL,
        "max_completion_tokens": max_tokens,
        "messages": messages,
    }


def extract_text(response) -> str:
    content = response.choices[0].message.content
    if content is None:
        return ""
    return content


def ask(client, prompt: str, system: str | None = None) -> str:
    request = build_request(prompt, system)
    response = client.chat.completions.create(**request)
    if response.choices[0].finish_reason == "length":
        raise RuntimeError("the answer was cut off (hit max tokens)")
    return extract_text(response)


def estimate_cost(usage, input_price: float, output_price: float) -> float:
    input_cost = usage.prompt_tokens * input_price / 1_000_000
    output_cost = usage.completion_tokens * output_price / 1_000_000
    return input_cost + output_cost
