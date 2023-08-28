import pytest


@pytest.mark.skip
def test_audio() -> None:
    audio = Audio()
    texts_path = MEDIA_PATH / "texts"

    with open(texts_path / "totk.txt") as f:
        text = f.read()

    title = "The Legend of Zelda Tears of the Kingdom"
    audio.convert(title, text)
