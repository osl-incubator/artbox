"""
Utilities for handling audio.

ref: https://thepythoncode.com/article/convert-text-to-speech-in-python
"""

import re
from pathlib import Path

import gtts


def slugify(s):
    s = s.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_-]+", "-", s)
    s = re.sub(r"^-+|-+$", "", s)
    return s


MEDIA_PATH = Path(__file__).parent.parent.parent / "media"


class Audio:
    def convert(self, title: str, text: str) -> None:
        """Convert text to audio."""
        output_path = MEDIA_PATH / "audios"
        slug = slugify(title)
        tts = gtts.gTTS(text)
        tts.save(str(output_path / f"{slug}.mp3"))
