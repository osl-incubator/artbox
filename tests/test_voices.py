"""Set of tests for the voices module."""
from pathlib import Path

import pytest

from artbox.voices import Voice

TMP_PATH = Path("/tmp/artbox")


@pytest.mark.parametrize("engine", ["gtts", "edge-tts"])
def test_convert_text_to_speech(engine) -> None:
    """Test the conversion from text to audio."""
    text_path = TMP_PATH / f"totk-{engine}.txt"
    params = {
        "title": "totk",
        "text-path": str(text_path),
        "output-path": str(TMP_PATH / f"voice-{engine}.mp3"),
        "engine": engine,
    }

    with open(text_path, "w") as f:
        f.write(
            "Are you ready to join Link and Zelda in fighting "
            "off this unprecedented threat to Hyrule?"
        )

    voice = Voice(params)
    voice.text_to_speech()
