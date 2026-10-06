"""
08 — Structured Output (Pydantic)
=================================

THEORY (read first)
-------------------
1. LLMs return TEXT, but apps need DATA. Structured output means making the model return
   JSON that matches a schema, then VALIDATING it.
2. Pydantic is Python's Zod. You declare a class with typed fields, and it validates
   (and converts) data at RUNTIME:
       class User(BaseModel):            const User = z.object({
           name: str                         name: z.string(),
           age: int                          age: z.number().int(),
                                         })
       User.model_validate(data)      ≈  User.parse(data)
       User.model_validate_json(s)    ≈  User.parse(JSON.parse(s))
       user.model_dump()              ->  dict          user.model_dump_json() -> str
       User.model_json_schema()       ->  the JSON Schema that gets sent to the LLM
       pydantic.ValidationError       ≈  ZodError    (e.errors() lists every problem)
3. Field(...) adds constraints and docs:  Field(min_length=3), Field(ge=0, le=10),
   Field(description="...")  (descriptions end up in the schema and help the LLM!)
4. Types:  Literal["low", "high"]  = TS union of string literals "low" | "high"
           X | None = None         = an optional field (TS  x?: X | null)
           list[str] = []          = SAFE in Pydantic (each instance gets its own copy),
                                     unlike the function-default gotcha from file 03
5. Pydantic is "lax" by default and coerces where it's safe: "2.5" -> 2.5 for a float
   field. Use `strict=True` to disable that.
6. OpenAI structured outputs: pass the Pydantic CLASS as `response_format`:
       completion = client.chat.completions.parse(
           model=MODEL, messages=[...], response_format=Ticket)
       ticket = completion.choices[0].message.parsed     # a validated Ticket instance
   The SDK turns the class into a JSON schema, and the model is constrained to it.
   If the model declines, message.refusal is set and parsed is None.
7. Models without native support often wrap JSON in ```json fences or add chatter
   around it, so you extract the JSON, then validate it (Q3).
8. Pydantic also powers FastAPI request and response bodies (file 11).

Run tests:  uv run python src/08_structured_output.py
Live:       uv run python src/08_structured_output.py --live   (needs OPENAI_API_KEY)
"""
import os
import sys
from typing import Literal

from pydantic import BaseModel, Field, ValidationError

from _check import FakeOpenAI, eq, raises, run

MODEL = os.getenv("OPENAI_MODEL", "gpt-5.4-nano")


# Q1 ─────────────────────────────────────────────────────────────────────────────
# Define a support-ticket model with these fields:
#   title:           str, at least 3 characters             -> Field(min_length=3)
#   priority:        one of "low", "medium", "high"         -> Literal[...]
#   tags:            list of str, defaults to an empty list
#   estimate_hours:  float or None, default None, must be >= 0 when given
class Ticket(BaseModel):
    pass  # TODO: replace with your fields


# Q2 ─────────────────────────────────────────────────────────────────────────────
# Validate a dict into a Ticket. Return None if it's invalid (catch ValidationError).
def parse_ticket(data: dict) -> Ticket | None:
    raise NotImplementedError  # TODO


# Q3 ─────────────────────────────────────────────────────────────────────────────
# LLMs often answer like:   'Sure! ```json\n{"title": ...}\n```'
# Extract the JSON object (from the first "{" to the last "}") and validate it with
# Ticket.model_validate_json. Raise ValueError if there is no "{...}" in the text.
# (Invalid ticket data raises ValidationError, which is a subclass of ValueError.)
#
# Hint: text.find("{") and text.rfind("}") return -1 when not found. Slice between them.
def parse_llm_json(text: str) -> Ticket:
    raise NotImplementedError  # TODO


# Q4 ─────────────────────────────────────────────────────────────────────────────
# Ask the model to extract a Ticket from a customer's message:
#   client.chat.completions.parse(
#       model=MODEL,
#       messages=[{"role": "system", "content": "Extract a support ticket from the user's message."},
#                 {"role": "user", "content": text}],
#       response_format=Ticket,
#   )
# Return choices[0].message.parsed. If it's None (the model refused), raise RuntimeError.
def extract_ticket(client, text: str) -> Ticket:
    raise NotImplementedError  # TODO


# ── Tests (don't edit) ──────────────────────────────────────────────────────────
def test_q1_ticket_model():
    t = Ticket(title="Fix login", priority="high")
    eq(t.tags, [])
    eq(t.estimate_hours, None)
    raises(ValidationError, Ticket, title="Fix login", priority="urgent")
    raises(ValidationError, Ticket, title="ab", priority="low")
    raises(ValidationError, Ticket, title="Fix", priority="low", estimate_hours=-1)
    eq(Ticket(title="Fix", priority="low", estimate_hours="2.5").estimate_hours, 2.5)  # lax coercion
    eq(t.model_dump(), {"title": "Fix login", "priority": "high", "tags": [], "estimate_hours": None})


def test_q2_parse_ticket():
    eq(parse_ticket({"title": "Add SSO", "priority": "medium", "tags": ["auth"]}).tags, ["auth"])
    eq(parse_ticket({"title": "Add SSO"}), None)  # priority missing


def test_q3_parse_llm_json():
    eq(parse_llm_json('{"title": "Dark mode", "priority": "low"}').title, "Dark mode")
    fenced = 'Sure! Here it is:\n```json\n{"title": "Dark mode", "priority": "low"}\n```\nAnything else?'
    eq(parse_llm_json(fenced).priority, "low")
    raises(ValueError, parse_llm_json, "Sorry, I can't help with that.")
    raises(ValidationError, parse_llm_json, '{"title": "Dark mode", "priority": "ASAP"}')


def test_q4_extract_ticket():
    fake = FakeOpenAI(parsed={"title": "Login broken", "priority": "high", "tags": ["auth"]})
    ticket = extract_ticket(fake, "I can't log in since this morning!!")
    assert isinstance(ticket, Ticket), "return the parsed Ticket"
    eq(ticket.title, "Login broken")
    eq(fake.calls[0]["response_format"], Ticket)
    eq(fake.calls[0]["messages"][-1]["content"], "I can't log in since this morning!!")


def live_demo():
    from openai import OpenAI

    ticket = extract_ticket(OpenAI(), "Hi, the export-to-PDF button crashes the app on Safari. "
                                      "Pretty annoying, we need it for Friday's report.")
    print(ticket.model_dump_json(indent=2))


if __name__ == "__main__":
    if "--live" in sys.argv:
        live_demo()
    else:
        run(globals())
