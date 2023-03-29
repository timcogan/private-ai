from config import get_config
from pathlib import Path


def test_get_config(monkeypatch, tmpdir):
    config_file_path = Path(tmpdir) / "config.json"
    monkeypatch.setattr("builtins.input", lambda _: "Test")
    config_with_user_input = get_config(config_file_path)
    config_read_from_file = get_config(config_file_path)
    assert config_with_user_input == config_read_from_file
