"""Set of tests for the videos module."""
from pathlib import Path

import pytest

from artbox.videos import Video

TMP_PATH = Path("/tmp/artbox")


@pytest.mark.fixture
def video():
    """Create a fixture for the Video object."""
    return Video()


@pytest.mark.skip
def test_combine_video_and_audio(video):
    """Test the function that combines video and audio."""
    # Example usage
    # "The Legend of Zelda Tears of the Kingdom - Official Trailer 3.mp4"
    video_path = TMP_PATH / "peachs-no-audio.mp4"
    audio_path = TMP_PATH / "smb-epic-theme.mp3"
    output_path = TMP_PATH / "peachs-with-music.mp4"
    video.combine_video_and_audio(
        str(video_path), str(audio_path), str(output_path)
    )


@pytest.mark.skip
def test_download_from_youtube(video):
    """Test the method that downloads videos from youtube."""
    # "https://www.youtube.com/watch?v=uHGShqcAHlQ"
    for url in [
        "https://youtube.com/shorts/gmutDetnBLQ",
        "https://youtube.com/watch?v=6pjbaE98ftU",
    ]:
        video.download_from_youtube(url)


@pytest.mark.skip
def test_remove_audio(video):
    """Test the function that removes audio from a video."""
    input_file = TMP_PATH / (
        "Princess Peachs Training Course in The Super Mario Bros Movie.mp4"
    )
    output_file = "peachs-no-audio.mp4"
    video.remove_audio(input_file, TMP_PATH / output_file)
