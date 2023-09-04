"""Base classes for ArtBox."""
from __future__ import annotations

from abc import ABC
from pathlib import Path


class ArtBox(ABC):
    """The base class for all ArtBox classes."""

    def __init__(self, args: dict[str, str]) -> None:
        """Initialize ArtBox class."""
        self.args: dict[str, str] = args
        self.input_path = Path(self.args.get("input-path", "/tmp"))
        self.output_path = Path(self.args.get("output-path", "/tmp"))
