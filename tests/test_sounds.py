import pytest

from artbox.sounds import Sound


@pytest.mark.skip
def test_extract():
    # Example usage
    videos_path = VIDEOS_PATH / "Super Mario Theme  EPIC VERSION.mp4"
    output_path = MEDIA_PATH / "sounds" / "smb-epic-theme.mp3"
    extract_audio(str(videos_path), str(output_path))


@pytest.mark.skip
def test_extract_notes_from_mp3():
    # Example usage
    mp3_path = MEDIA_PATH / "sounds" / "tok-audio.mp3"
    output_notes = MEDIA_PATH / "notes" / "tok-audio.txt"
    notes = extract_notes_from_mp3(str(mp3_path), str(output_notes))
    print("Detected notes:", notes)


@pytest.mark.skip
def test_generate_melody():
    notes_path = MEDIA_PATH / "notes" / "tok-audio.txt"
    generate_melody(notes_path, total_duration=3.54 * 60)


@pytest.mark.skip
def test_convert_to_8bit_audio():
    # Example usage
    videos_path = (
        MEDIA_PATH
        / "videos"
        / "The Legend of Zelda Tears of the Kingdom – Official Trailer 3.mp4"
    )
    output_path = MEDIA_PATH / "sounds" / "tok8bits.mp3"
    convert_to_8bit_audio(str(videos_path), str(output_path))
