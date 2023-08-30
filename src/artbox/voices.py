"""
Utilities for handling audio voices.

ref: https://thepythoncode.com/article/convert-text-to-speech-in-python
"""
import asyncio
import random

from abc import ABC, abstractmethod

import edge_tts
import gtts

from edge_tts import VoicesManager

from artbox.base import ArtBox


class VoiceEngineBase(ArtBox, ABC):
    """Set of methods for handing audio voices."""

    @abstractmethod
    def text_to_speech(self) -> None:
        """Convert text to audio voice."""
        ...


class Voice(VoiceEngineBase):
    """Voice class will run commands according to the selected engine."""

    def __init__(self, *args, **kwargs) -> None:
        """Initialize Voice class."""
        super().__init__(*args, **kwargs)
        engine = self.args.get("engine", "edge-tts")

        if engine == "edge-tts":
            self.engine = VoiceEngineMSEdgeTTS(*args, **kwargs)
        elif engine == "gtts":
            self.engine = VoiceEngineGTTS(*args, **kwargs)
        else:
            raise Exception(f"Engine {engine} not found.")

    def text_to_speech(self) -> None:
        """Convert text to audio voice."""
        return self.engine.text_to_speech()


class VoiceEngineGTTS(VoiceEngineBase):
    """Google-Text-To-Speech engine."""

    def text_to_speech(self) -> None:
        """Convert text to audio voice."""
        title: str = self.args.get("title", "")
        text_path: str = self.args.get("text-path", "")
        lang: str = self.args.get("lang", "en")

        if not title:
            raise Exception("Argument `title` not given")

        if not text_path:
            raise Exception("Argument `text_path` not given")

        with open(text_path, "r") as f:
            text = f.read()

        tts = gtts.gTTS(text, lang=lang, slow=False)
        tts.save(str(self.output_path))


class VoiceEngineMSEdgeTTS(VoiceEngineBase):
    """Microsoft Edge Text-To-Speech engine."""

    async def async_text_to_speech(self) -> None:
        """Convert text to audio voice in async mode."""
        title: str = self.args.get("title", "")
        text_path: str = self.args.get("text-path", "")
        lang: str = self.args.get("lang", "en")

        if not title:
            raise Exception("Argument `title` not given")

        if not text_path:
            raise Exception("Argument `text_path` not given")

        with open(text_path, "r") as f:
            text = f.read()

        params = {"Locale": lang} if "-" in lang else {"Language": lang}
        voices = await VoicesManager.create()
        voice_options = voices.find(Gender="Female", **params)

        communicate = edge_tts.Communicate(
            text=text,
            voice=random.choice(voice_options)["Name"],
            rate="+5%",
            volume="+0%",
        )
        with open(self.output_path, "wb") as file:
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    file.write(chunk["data"])
                elif chunk["type"] == "WordBoundary":
                    print(f"WordBoundary: {chunk}")

    def text_to_speech(self) -> None:
        """Convert text to audio voice."""
        loop = asyncio.get_event_loop_policy().get_event_loop()
        try:
            loop.run_until_complete(self.async_text_to_speech())
        finally:
            loop.close()
