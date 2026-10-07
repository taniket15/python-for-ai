import time

from dotenv import load_dotenv
from openai import OpenAI
from ticket_checker_prompt import AFTER, EXAMPLES, TICKETS, Triage

MODEL = "gpt-6-luna"

load_dotenv()
client = OpenAI()


def sort_ticket(system, text):
    messages = [
        {"role": "system", "content": system},
        *EXAMPLES,
        {"role": "user", "content": text},
    ]

    response = client.chat.completions.parse(
        model=MODEL,
        messages=messages,
        response_format=Triage,
    )

    message = response.choices[0].message

    # parsed is None when the model refuses
    return message.parsed, message.refusal, response.usage


def run(label, system):
    right, tokens_in, tokens_out = 0, 0, 0

    started = time.perf_counter()

    print(label)

    for text, expected in TICKETS:
        result, refusal, usage = sort_ticket(system, text)

        tokens_in += usage.prompt_tokens
        tokens_out += usage.completion_tokens

        ok = result is not None and result.category == expected

        right += ok

        print(
            f"  {'ok ' if ok else 'BAD'} "
            f"{expected:9} "
            + (f"{result.category:9} p{result.priority} {result.reason}" if result else f"(refused) {refusal}")
        )

    seconds = time.perf_counter() - started

    print(
        f"  accuracy {right}/{len(TICKETS)}, "
        f"{tokens_in} tokens in, "
        f"{tokens_out} out, "
        f"{seconds / len(TICKETS):.2f} seconds a ticket"
    )


run("after", AFTER)
