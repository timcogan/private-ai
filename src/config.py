import json

from pathlib import Path
from typing import Final, List, NamedTuple


CONFIG_FILE_PATH: Final[Path] = Path("config.json")


class Config(NamedTuple):
    ai_number: str
    number_whitelist: List[str]
    # TODO The following should probably be Path objects instead of strings
    ai_cli_path: str = "tools/alpaca.cpp/chat"
    ai_model_size: str = "7B"
    signal_cli_path: str = "tools/signal-cli/signal-cli-0.11.7/bin/signal-cli"

    @classmethod
    def from_file(cls, path: Path) -> "Config":
        with open(path) as f:
            dictionary = json.load(f)
            return cls(**dictionary)

    def save(self, path: Path) -> None:
        dictionary = self._asdict()
        with open(path, "w") as f:
            json.dump(dictionary, f, indent=4)


def get_config() -> Config:
    if CONFIG_FILE_PATH.is_file():
        config = Config.from_file(CONFIG_FILE_PATH)
    else:
        # TODO The user input should be verified
        whitelist_number = input(
            "What is your personal phone number that you will use to message the AI? (E.g., +1XXXYYYZZZZ) "
        )
        ai_number = input("What is the number that the AI will be messaging with? (E.g., +1XXXYYYZZZZ) ")
        config = Config(ai_number, [whitelist_number])
        config.save(CONFIG_FILE_PATH)

    return config


def main() -> None:
    config = get_config()
    print(config)


if __name__ == "__main__":
    main()
