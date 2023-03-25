import re
import subprocess

from config import Config, get_config
from typing import Final, Iterator, List, NamedTuple


SENDER_TEMPLATE: Final[str] = r"(?P<sender>\S+) \(device:"
NEWLINE_TEMPLATE: Final[str] = r".+\n"
BODY_TEMPLATE: Final[str] = r"Body: (?P<body>.*)"

MESSAGE_PATTERN: Final[re.Pattern] = re.compile(SENDER_TEMPLATE + NEWLINE_TEMPLATE * 4 + BODY_TEMPLATE)
RECEIPT_PATTERN: Final[re.Pattern] = re.compile(SENDER_TEMPLATE + NEWLINE_TEMPLATE * 3 + "Received a receipt message")


class Message(NamedTuple):
    sender: str
    body: str


"""
Regular message text looks like this:

Envelope from: “SENDER NAME” +1XXXYYYZZZZ (device: X) to +1XXXYYYZZZZ
Timestamp: XXXXXXXXXXXXX (YYYY-MM-DDTHH:MM:SS.SSSZ)
Server timestamps: received: XXXXXXXXXXXXX (YYYY-MM-DDTHH:MM:SS.SSSZ) delivered: XXXXXXXXXXXXX (YYYY-MM-DDTHH:MM:SS.SSSZ)
Sent by unidentified/sealed sender
Message timestamp: XXXXXXXXXXXXX (YYYY-MM-DDTHH:MM:SS.SSSZ)
Body: MESSAGE_BODY
With profile key

A receipt message looks like this:

Envelope from: “SENDER NAME” +1XXXYYYZZZZ (device: X) to +1XXXYYYZZZZ
Timestamp: XXXXXXXXXXXXX (YYYY-MM-DDTHH:MM:SS.SSSZ)
Server timestamps: received: XXXXXXXXXXXXX (YYYY-MM-DDTHH:MM:SS.SSSZ) delivered: XXXXXXXXXXXXX (YYYY-MM-DDTHH:MM:SS.SSSZ)
Sent by unidentified/sealed sender
Received a receipt message
  When: XXXXXXXXXXXXX (YYYY-MM-DDTHH:MM:SS.SSSZ)
  Is delivery receipt
  Timestamps:
  - XXXXXXXXXXXXX (YYYY-MM-DDTHH:MM:SS.SSSZ)
"""


def get_messages(config: Config) -> List[Message]:
    cmd = [config.signal_cli_path, "-a", config.ai_number, "receive"]
    completed_process = subprocess.run(cmd, stdout=subprocess.PIPE)
    messages_text = str(completed_process.stdout.decode())
    messages = list(parse_messages(messages_text))
    if messages_text != "" and messages == []:
        print(f"WARNING: Signal message parsing is broken.\nReceived:\n{messages_text}")
    return messages


def parse_messages(text: str) -> Iterator[Message]:
    # This line is present for some senders, but we don't care about it
    # and we want all messages to come across in the same format
    text = text.replace("Sent by unidentified/sealed sender\n", "")

    for match in MESSAGE_PATTERN.findall(text):
        message = Message(*match)
        yield message
        if message.body == "":
            print("WARNING: Unexpected empty message body.")

    for match in RECEIPT_PATTERN.findall(text):
        yield Message(sender=match, body="")


def send_message(config: Config, body: str, address: str) -> None:
    cmd = [config.signal_cli_path, "-a", config.ai_number, "send", "-m", body, address]
    subprocess.run(cmd, stdout=subprocess.PIPE)


def main() -> None:
    config = get_config()

    for number in config.number_whitelist:
        send_message(config, "This is a test.", number)

    for message in get_messages(config):
        print(message)


if __name__ == "__main__":
    main()
