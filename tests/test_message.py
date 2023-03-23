from message import Message, parse_messages
from typing import Final, List


EXAMPLE_RECEIPT: Final[
    str
] = """
Envelope from: “Joe Bob” +19876543210 (device: X) to +1XXXYYYZZZZ
Timestamp: XXXXXXXXXXXXX (YYYY-MM-DDTHH:MM:SS.SSSZ)
Server timestamps: received: XXXXXXXXXXXXX (YYYY-MM-DDTHH:MM:SS.SSSZ) delivered: XXXXXXXXXXXXX (YYYY-MM-DDTHH:MM:SS.SSSZ)
Sent by unidentified/sealed sender
Message timestamp: XXXXXXXXXXXXX (YYYY-MM-DDTHH:MM:SS.SSSZ)
Body: This is a test
With profile key

Envelope from: “Jane Doe” +12223334444 (device: X) to +1XXXYYYZZZZ
Timestamp: XXXXXXXXXXXXX (YYYY-MM-DDTHH:MM:SS.SSSZ)
Server timestamps: received: XXXXXXXXXXXXX (YYYY-MM-DDTHH:MM:SS.SSSZ) delivered: XXXXXXXXXXXXX (YYYY-MM-DDTHH:MM:SS.SSSZ)
Sent by unidentified/sealed sender
Received a receipt message
  When: XXXXXXXXXXXXX (YYYY-MM-DDTHH:MM:SS.SSSZ)
  Is delivery receipt
  Timestamps:
  - XXXXXXXXXXXXX (YYYY-MM-DDTHH:MM:SS.SSSZ)

Envelope from: “Slim Jim” +430123456789 (device: X) to +1XXXYYYZZZZ
Timestamp: XXXXXXXXXXXXX (YYYY-MM-DDTHH:MM:SS.SSSZ)
Server timestamps: received: XXXXXXXXXXXXX (YYYY-MM-DDTHH:MM:SS.SSSZ) delivered: XXXXXXXXXXXXX (YYYY-MM-DDTHH:MM:SS.SSSZ)
Sent by unidentified/sealed sender
Message timestamp: XXXXXXXXXXXXX (YYYY-MM-DDTHH:MM:SS.SSSZ)
Body: Should I pick up a pizza?
With profile key
"""

EXPECTED_MESSAGES: Final[List[Message]] = [
    Message("+19876543210", "This is a test"),
    Message("+430123456789", "Should I pick up a pizza?"),
    Message("+12223334444", ""),
]


def test_parse_messages() -> None:
    for i, message in enumerate(parse_messages(EXAMPLE_RECEIPT)):
        assert message.sender == EXPECTED_MESSAGES[i].sender
        assert message.body == EXPECTED_MESSAGES[i].body
