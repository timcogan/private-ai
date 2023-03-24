import sys
import time

from ai import AI_Pipe
from config import get_config
from message import get_messages, send_message
from typing import Final


ERROR_MESSAGE: Final[str] = "I'm sorry, but I don't know you."


def main() -> None:
    config = get_config()
    ai_pipe = AI_Pipe(config)
    while True:
        for message in get_messages(config):
            print(message)
            if message.sender not in config.number_whitelist:
                print(ERROR_MESSAGE)
                send_message(config, ERROR_MESSAGE, message.sender)
            elif message.body:
                response = ai_pipe.get_response(message.body)
                print(repr(response))
                send_message(config, response, message.sender)

        time.sleep(5)  # We don't want to poll the Signal API too fast
        print(".", end="")  # Just show that our process is alive
        sys.stdout.flush()


if __name__ == "__main__":
    main()
