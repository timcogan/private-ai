import json

from pathlib import Path
from typing import Final, List, NamedTuple


CONFIG_FILE_PATH: Final[Path] = Path("config.json")


class Config(NamedTuple):
    ai_number: str = ""
    number_whitelist: List[str] = []
    # TODO The following should probably be Path objects instead of strings
    ai_cli_path: str = "tools/alpaca.cpp/chat"
    ai_model_size: str = "7B"
    signal_cli_path: str = "tools/signal-cli/signal-cli-0.11.7/bin/signal-cli"
    max_len_output: int = 512

    @classmethod
    def from_file(cls, path: Path) -> "Config":
        with open(path) as f:
            config_dictionary = cls()._asdict()
            # Use the config.json file to override Config defaults
            for k, v in json.load(f).items():
                config_dictionary[k] = v
            return cls(**config_dictionary)

    def save(self, path: Path) -> None:
        dictionary = self._asdict()
        with open(path, "w") as f:
            json.dump(dictionary, f, indent=4)


def get_config(config_file_path: Path = CONFIG_FILE_PATH) -> Config:
    if config_file_path.is_file():
        config = Config.from_file(config_file_path)
    else:
        # TODO The user input should be verified
        whitelist_number = input(
            "What is your personal phone number that you will use to message the AI? (E.g., +1XXXYYYZZZZ) "
        )
        ai_number = input("What is the number that the AI will be messaging with? (E.g., +1XXXYYYZZZZ) ")
        config = Config(ai_number=ai_number, number_whitelist=[whitelist_number])
        config.save(config_file_path)

    return config


def main() -> None:
    config = get_config()
    print(config)


if __name__ == "__main__":
    main()
