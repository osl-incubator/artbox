# ArtBox

ArtBox is a tool set for handling multimedia files.

- Documentation: https://ggpedia.games
- License: BSD-3 Clause

## Features

TBD

## Examples

For the following examples, create the a temporary folder for artbox:

```bash
$ mkdir /tmp/artbox
```

### Convert text to audio

```bash
$ echo "I love artbox!" > /tmp/artbox/text.md
$ artbox voice text-to-audio \
    --title artbox \
    --text-path /tmp/artbox/text.md \
    --output-path /tmp/artbox/voice.mp3
```

If you need to generate the audio for different language, you can use
the flag `--lang`:

```bash
$ echo "Bom dia, mundo!" > /tmp/artbox/text.md
$ artbox voice text-to-audio \
    --title artbox \
    --text-path /tmp/artbox/text.md \
    --output-path /tmp/artbox/voice.mp3 \
    --lang pt
```

### Download a youtube video

```bash
$ artbox video download-from-youtube \
    --url https://www.youtube.com/watch?v=zw47_q9wbBE \
    --output-path /tmp/artbox/
```

### Create a song based on the musical notes

```bash
# json format
echo '["E", "D#", "E", "D#", "E", "B", "D", "C", "A"]' > /tmp/artbox/notes.txt
$ artbox sound notes-to-audio \
  --input-path /tmp/artbox/notes.txt \
  --output-path /tmp/artbox/music.mp3 \
  --duration 2
```

### Remove the audio from a video

First, download the youtube video `https://www.youtube.com/watch?v=zw47_q9wbBE`
as explained before.

Next, run the following command:

```bash
$ artbox video remove-audio \
  --input-path "/tmp/artbox/The Legend of Zelda Breath of the Wild - Nintendo Switch Presentation 2017 Trailer.mp4" \
  --output-path /tmp/artbox/botw.mp4
```

### Extract the audio from a video

First, download the youtube video `https://www.youtube.com/watch?v=zw47_q9wbBE`
as explained before.

Next, run the following command:

```bash
$ artbox video extract-audio \
  --input-path "/tmp/artbox/The Legend of Zelda Breath of the Wild - Nintendo Switch Presentation 2017 Trailer.mp4" \
  --output-path /tmp/artbox/botw-audio.mp3
```

### Combine audio and video files

First, execute the previous steps:

- Download a youtube video
- Remove the audio from a video
- Extract the audio from a video

Next, run the following command:

```bash
$ artbox video combine-video-and-audio \
  --video-path /tmp/artbox/botw.mp4 \
  --audio-path /tmp/artbox/botw-audio.mp3 \
  --output-path /tmp/artbox/botw-combined.mp4
```

## Additional dependencies

If you want to use Python to play your audio files, you can install `playsound`:

```bash
$ pip wheel --use-pep517 "playsound (==1.3.0)"
```

## Troubleshoot

After installing with `poetry install`:

- Patch `pytube` (ref: https://github.com/pytube/pytube/issues/1773):
  `sed -i 's/(r"^$\\w+\\W")/(r"^\\w+\\W")/' $CONDA_PREFIX/lib/python3.*/site-packages/pytube/cipher.py`
