import os
import signal
import subprocess
import sys

from config import Config, get_config
from pathlib import Path
from typing import Final


def download_model(model_destination: Path, model_url: Path) -> None:
    for p in list(model_destination.parents)[:2]:
        p.mkdir(exist_ok=True)
    wd = os.getcwd()
    os.chdir(str(model_destination.parent))
    cmd = ["curl", "-L", "-O", model_url]
    subprocess.run(cmd)
    os.chdir(wd)


def get_model_path(config: Config) -> str:
    model_folder = Path(config.ai_cli_path).parent / "models" / config.ai_model_size
    model_url = Path(
        f"https://huggingface.co/Pi3141/alpaca-{config.ai_model_size}-ggml/resolve/main/ggml-model-q4_0.bin"
    )
    model_path = model_folder / model_url.name

    if not model_path.exists():
        download_model(model_path, model_url)

    return str(model_path)


class AI_Pipe:
    p: subprocess.Popen
    max_len_output: int = -1

    def __init__(self, config: Config) -> None:
        cmd = [config.ai_cli_path, "-m", get_model_path(config)]
        print("Starting AI process with command: " + " ".join(cmd))
        self.p = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        # Read/print all of the startup text before configuring max_len_output
        self.read_until_prompt()
        self.max_len_output = config.max_len_output

    def read(self) -> bytes:
        assert self.p.stdout, "`stdout` is None. The pipe did not open properly."
        return self.p.stdout.read(1)

    def write(self, s: bytes) -> None:
        assert self.p.stdin, "`stdin` is None. The pipe did not open properly."
        self.p.stdin.write(s)
        self.p.stdin.write(b"\r\n")
        self.p.stdin.flush()

    def cancel_output(self) -> None:
        assert self.p.stdin, "`stdin` is None. The pipe did not open properly."
        self.p.send_signal(signal.SIGINT)  # Tell the AI to stop generating output

    def get_response(self, message: str) -> str:
        self.write(message.encode())
        response = self.read_until_prompt().decode().strip()

        # These codes control the color of the text when printed in a terminal
        # but they will just clutter the response
        for ansi_escape in ["\x1b[1m", "\x1b[32m", "\x1b[0m"]:
            response = response.replace(ansi_escape, "")

        return response

    def read_until_prompt(self, prompt: bytes = b"\n> ") -> bytes:
        response = b""
        buffer = b"".join(self.read() for _ in range(len(prompt)))

        while buffer != prompt:
            response += buffer[:1]
            buffer = buffer[1:] + self.read()

            # Sometimes the AI will repeat itself forever
            # "This is a poem about... This is a poem about... This is a..."
            output_is_too_long = False if self.max_len_output < 0 else len(response) > self.max_len_output

            if check_squirrely_behavior(buffer) or output_is_too_long:
                self.cancel_output()
                while buffer != prompt:  # Clear buffer so we don't cancel output multiple times
                    buffer = buffer[1:] + self.read()
            try:
                print(response[-1:].decode(), end="")
            except UnicodeDecodeError:
                print("□", end="")
            sys.stdout.flush()

        return response


def check_squirrely_behavior(b: bytes) -> bool:
    """
    The AI will start printing outputs like:
        ### Instruction:
        Generate a response to...
        ### Response:
        My favorite book is...
    We want to identify and ignore these kinds of output.
    Variations:
        ## Instruction:
        # ## Instruction:
    """
    output_is_squirrely = b.count(b"#") >= 2
    if output_is_squirrely:
        print(f"WARNING: AI output `{b}`")
    return output_is_squirrely


def main() -> None:
    ai_pipe = AI_Pipe(get_config())
    while True:
        text = input("> ")
        response = ai_pipe.get_response(text)
        print(f"\nAI response: `{response}`")


if __name__ == "__main__":
    main()
