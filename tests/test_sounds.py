"""Set of tests for the sounds module."""
from pathlib import Path

import pytest

from artbox.sounds import Sound

TMP_PATH = Path("/tmp/artbox")


@pytest.mark.fixture
def sound():
    """Create a fixture for the Sound object."""
    return Sound()


@pytest.mark.skip
def test_extract(sound):
    """Test the extraction audio from a video."""
    videos_path = TMP_PATH / "Super Mario Theme  EPIC VERSION.mp4"
    output_path = TMP_PATH / "sounds" / "smb-epic-theme.mp3"
    sound.extract_audio(str(videos_path), str(output_path))


@pytest.mark.skip
def test_extract_notes_from_mp3(sound):
    """Test the extraction of notes from mp3 file."""
    mp3_path = TMP_PATH / "sounds" / "tok-audio.mp3"
    output_notes = TMP_PATH / "notes" / "tok-audio.txt"
    notes = sound.extract_notes_from_mp3(str(mp3_path), str(output_notes))
    print("Detected notes:", notes)


@pytest.mark.skip
def test_generate_melody(sound):
    """Test the melody generation from notes."""
    notes_path = TMP_PATH / "notes" / "tok-audio.txt"
    sound.generate_melody(notes_path, total_duration=3.54 * 60)


@pytest.mark.skip
def test_convert_to_8bit_audio(sound):
    """Test the audio conversion to 8bits style."""
    videos_path = (
        TMP_PATH
        / "videos"
        / "The Legend of Zelda Tears of the Kingdom - Official Trailer 3.mp4"
    )
    output_path = TMP_PATH / "sounds" / "tok8bits.mp3"
    sound.convert_to_8bit_audio(str(videos_path), str(output_path))
