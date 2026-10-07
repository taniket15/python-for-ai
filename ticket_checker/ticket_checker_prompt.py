from typing import Literal

from pydantic import BaseModel, Field


# The API enforces this schema, so the field order matters:
# the model writes its reason before it picks a category.
class Triage(BaseModel):
    reason: str = Field(description="One short sentence on what the customer's main complaint is")
    category: Literal["billing", "shipping", "other"]
    priority: int = Field(ge=1, le=5, description="1 (can wait) to 5 (urgent)")

BEFORE = """You sort customer support tickets for an online shop.

Categories:
- billing: payments, charges, refunds
- shipping: parcels, delivery, damaged boxes
- other: anything else"""

AFTER = """You sort customer support tickets for an online shop.

Categories:
- billing: payments, charges, refunds, and any fee a customer is asked to pay, even at the door
- shipping: where a parcel is, late or lost deliveries, damaged boxes
- other: account changes, cancelling an order, anything else

When a ticket contains multiple issues, classify according to the customer's primary complaint.

Use these rules:
- A complaint about a payment, charge, refund, or fee is billing.
- A complaint about the location, delay, loss, or physical damage of a parcel is shipping.
- A request to change an account or cancel an order is other.
- A requested resolution does not change the category of the underlying complaint.

Examples:
- "My package never arrived and I want a refund" → shipping
- "My package was damaged and I want my money back" → shipping
- "I was charged for an order that never arrived" → billing"""

EXAMPLES = [
    {"role": "user", "content": "You took money from my card two times"},
    {"role": "assistant", "content": '{"reason": "The customer was charged twice.", "category": "billing", "priority": 4}'},
    {"role": "user", "content": "Where is my delivery? It is a week late"},
    {"role": "assistant", "content": '{"reason": "The delivery is late.", "category": "shipping", "priority": 3}'},
    {"role": "user", "content": "Can I change the email on my account?"},
    {"role": "assistant", "content": '{"reason": "The customer wants to change account details.", "category": "other", "priority": 2}'},
]

TICKETS = [
    ("I was charged twice for one order", "billing"),
    ("My parcel has not arrived", "shipping"),
    ("Can I get a refund for the blue mug?", "billing"),
    ("How do I change my password?", "other"),
    ("The parcel arrived but the box was crushed", "shipping"),
    ("The courier asked me to pay a delivery fee at the door", "billing"),
    ("I want to cancel my order before it ships", "other"),
]

TICKETS1 = [
    # -------------------------
    # Billing edge cases
    # -------------------------

    ("Why did you charge me twice?", "billing"),
    ("I see two identical transactions on my card", "billing"),
    ("The amount on my statement is wrong", "billing"),
    ("You charged me for something I never bought", "billing"),
    ("I want my money back for this order", "billing"),
    ("Can you reverse this payment?", "billing"),
    ("Why is there an extra charge on my bill?", "billing"),
    ("The delivery guy wants me to pay 200 rupees at the door", "billing"),
    ("The courier says I need to pay a fee before he gives me the package", "billing"),
    ("Why am I being asked for cash when my order is already paid?", "billing"),

    # Deliberately contains shipping words but is billing
    ("I was charged a delivery fee", "billing"),
    ("They charged me for shipping even though shipping was supposed to be free", "billing"),
    ("The courier charged my card twice", "billing"),

    # -------------------------
    # Shipping edge cases
    # -------------------------

    ("Where is my package?", "shipping"),
    ("My order still hasn't arrived", "shipping"),
    ("It's been 10 days and I still don't have my parcel", "shipping"),
    ("Can you tell me where my package is?", "shipping"),
    ("The tracking hasn't moved for three days", "shipping"),
    ("My package says delivered but I don't have it", "shipping"),
    ("The box arrived completely destroyed", "shipping"),
    ("The delivery came but everything inside was damaged", "shipping"),
    ("When will this thing actually get here?", "shipping"),

    # Deliberately contains billing/order words but is shipping
    ("I paid for my order last week but it still hasn't arrived", "shipping"),
    ("I ordered this ages ago, where is it?", "shipping"),
    ("The order was shipped but seems to be stuck somewhere", "shipping"),

    # -------------------------
    # Other edge cases
    # -------------------------

    ("I forgot my password", "other"),
    ("How do I update my email address?", "other"),
    ("Can I change my name on my account?", "other"),
    ("I don't want this order anymore", "other"),
    ("Please cancel my order", "other"),
    ("Can you stop my order before it leaves the warehouse?", "other"),
    ("I changed my mind about buying this", "other"),

    # Deliberately contains shipping words but is other
    ("Can I cancel this before it ships?", "other"),
    ("I want to cancel the order that is about to be shipped", "other"),
    ("Don't ship my order, I want to cancel it", "other"),

    # -------------------------
    # Weird / natural customer language
    # -------------------------

    ("uhhh why did my card get hit twice lol", "billing"),
    ("bro where's my package", "shipping"),
    ("pls refund this thing", "billing"),
    ("wtf why is there another charge", "billing"),
    ("package?? hello??", "shipping"),
    ("I don't need it anymore just cancel it", "other"),
    ("can u tell me where my stuff is", "shipping"),
    ("money gone. twice.", "billing"),
    ("box came looking like it got run over", "shipping"),

    # -------------------------
    # Typos / poor grammar
    # -------------------------

    ("i was chaged two times", "billing"),
    ("my parcal is missing", "shipping"),
    ("wheres my delivry", "shipping"),
    ("i want refnd", "billing"),
    ("plz cancle my oder", "other"),
    ("why u charge me extra", "billing"),

    # -------------------------
    # Mixed-intent / tricky cases
    # -------------------------

    ("My package hasn't arrived and I want a refund", "shipping"),
    ("The courier damaged my box and now I want my money back", "shipping"),
    ("I was charged for an order that never arrived", "billing"),
    ("My order hasn't shipped yet, can I cancel it?", "other"),
    ("I paid for the order but want to cancel it before delivery", "other"),

    # -------------------------
    # Very short / underspecified
    # -------------------------

    ("Refund?", "billing"),
    ("Cancel", "other"),
    ("Where's my order?", "shipping"),
    ("Extra charge", "billing"),
    ("Broken box", "shipping"),
    ("Password", "other"),
]
