import json
import logging
import time

from dotenv import load_dotenv
from openai import OpenAI
from ticket_checker_prompt import AFTER, EXAMPLES, TICKETS, Triage

MODEL = "gpt-6-luna"

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)-7s %(message)s", datefmt="%H:%M:%S")
log = logging.getLogger("ticket_checker")

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
    log.debug("raw response: %s", response.model_dump_json(indent=2))

    # parsed is None when the model refuses
    return message.parsed, message.refusal


def run(label, system):
    right = 0
    started = time.perf_counter()

    log.info("run %r: model=%s, %d tickets", label, MODEL, len(TICKETS))

    for i, (text, expected) in enumerate(TICKETS, 1):
        result, refusal = sort_ticket(system, text)

        ok = result is not None and result.category == expected
        right += ok

        log.log(
            logging.INFO if ok else logging.WARNING,
            "[%d/%d] %s  expected=%s  ticket=%r\n%s",
            i,
            len(TICKETS),
            "OK " if ok else "BAD",
            expected,
            text,
            json.dumps(result.model_dump(), indent=2) if result else f"refused: {refusal}",
        )

    seconds = time.perf_counter() - started

    log.info(
        "run %r done: accuracy %d/%d, %.2fs per ticket",
        label,
        right,
        len(TICKETS),
        seconds / len(TICKETS),
    )


run("after", AFTER)
