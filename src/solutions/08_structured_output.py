# Solutions for 08_structured_output.py
# Test them with:  uv run python src/08_structured_output.py --solution
from typing import Literal

from pydantic import BaseModel, Field, ValidationError


class Ticket(BaseModel):
    title: str = Field(min_length=3)
    priority: Literal["low", "medium", "high"]
    tags: list[str] = []
    estimate_hours: float | None = Field(default=None, ge=0)


def parse_ticket(data: dict) -> Ticket | None:
    try:
        return Ticket.model_validate(data)
    except ValidationError:
        return None


def parse_llm_json(text: str) -> Ticket:
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("no JSON object found in the text")
    json_text = text[start:end + 1]
    return Ticket.model_validate_json(json_text)


def extract_ticket(client, text: str) -> Ticket:
    completion = client.chat.completions.parse(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Extract a support ticket from the user's message."},
            {"role": "user", "content": text},
        ],
        response_format=Ticket,
    )
    ticket = completion.choices[0].message.parsed
    if ticket is None:
        raise RuntimeError("the model refused to answer")
    return ticket
