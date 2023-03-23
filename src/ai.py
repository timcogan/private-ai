import subprocess

from config import Config, get_config
from typing import Final, Iterator


PROMPT: Final[str] = ">"


class AI_Pipe:
    p: subprocess.Popen

    def __init__(self, config: Config) -> None:
        cmd = [config.ai_cli_path, "-m", config.ai_model_path]
        print("Starting AI process with command: " + " ".join(cmd))
        self.p = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        self.get_response()

    def read(self) -> str:
        assert self.p.stdout, "`stdout` is None. The pipe did not open properly."
        return self.p.stdout.read(1).decode()

    def write(self, s: bytes) -> None:
        assert self.p.stdin, "`stdin` is None. The pipe did not open properly."
        self.p.stdin.write(s)
        self.p.stdin.write(b"\r\n")
        self.p.stdin.flush()

    def get_response(self, message: str = "") -> str:
        if message:
            self.write(message.encode())
        response_chunks = list(self.read_until_prompt())
        response = "".join(response_chunks).strip()

        # These codes control the color of the text when printed in a terminal
        # but they will just clutter the response
        for ansi_escape in ["\x1b[1m", "\x1b[32m", "\x1b[0m"]:
            response = response.replace(ansi_escape, "")

        return response

    def read_until_prompt(self) -> Iterator[str]:
        while (latest := self.read()) != PROMPT:
            print(latest, end="")
            yield latest


def main() -> None:
    ai_pipe = AI_Pipe(get_config())
    while True:
        text = input(PROMPT + " ")
        response = ai_pipe.get_response(text)
        print(f"AI response: `{response}`")


if __name__ == "__main__":
    main()
