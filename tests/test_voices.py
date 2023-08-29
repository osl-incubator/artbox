"""Set of tests for the voices module."""
from pathlib import Path

import pytest

from artbox.voices import Voice

TMP_PATH = Path("/tmp/artbox")


@pytest.mark.skip
def test_voice_text_conversion() -> None:
    """Test the conversion from text to audio."""
    audio = Voice()
    texts_path = TMP_PATH / "texts"

    with open(texts_path / "totk.txt") as f:
        text = f.read()

    title = "The Legend of Zelda Tears of the Kingdom"
    audio.convert(title, text)
