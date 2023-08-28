import pytest

from artbox.videos import Video


@pytest.mark.skip
def test_combine_video_audio():
    # Example usage
    # "The Legend of Zelda Tears of the Kingdom – Official Trailer 3.mp4"
    video_path = RESULTS_PATH / "peachs-no-audio.mp4"
    audio_path = SOUNDS_PATH / "smb-epic-theme.mp3"
    output_path = RESULTS_PATH / "peachs-with-music.mp4"
    combine_video_audio(str(video_path), str(audio_path), str(output_path))


@pytest.mark.skip
def test_download():
    # "https://www.youtube.com/watch?v=uHGShqcAHlQ"
    for url in [
        "https://youtube.com/shorts/gmutDetnBLQ",
        "https://youtube.com/watch?v=6pjbaE98ftU",
    ]:
        download(url)


@pytest.mark.skip
def test_remove_audio():
    input_file = VIDEOS_PATH / (
        "Princess Peachs Training Course in The Super Mario Bros Movie.mp4"
    )
    output_file = "peachs-no-audio.mp4"
    remove_audio(input_file, RESULTS_PATH / output_file)
