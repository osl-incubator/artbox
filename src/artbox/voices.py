"""
Utilities for handling audio voices.

ref: https://thepythoncode.com/article/convert-text-to-speech-in-python
"""

import re

from pathlib import Path

import gtts

from artbox.base import ArtBox


def slugify(s):
    s = s.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_-]+", "-", s)
    s = re.sub(r"^-+|-+$", "", s)
    return s


class Voice(ArtBox):
    """Set of methods for handing audio voices."""

    def text_to_audio(self) -> None:
        """Convert text to audio voice."""
        title: str = self.args.get("title", "")
        text_path: str = self.args.get("text-path", "")

        if not title:
            raise Exception("Argument `title` not given")

        if not text_path:
            raise Exception("Argument `text_path` not given")

        with open(text_path, "r") as f:
            text = f.read()

        tts = gtts.gTTS(text, lang="en", slow=False)
        tts.save(str(self.output_path))
