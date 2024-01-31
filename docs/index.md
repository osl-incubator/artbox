# ArtBox

ArtBox is a tool set for handling multimedia files.

- Documentation: https://ggpedia.games
- License: BSD-3 Clause

## Features

TBD

# Setup

ArtBox uses some dependencies that maybe would not work well in your machine. In
order to have everything well installed, create a conda/mamba environment and
install `artbox` there.

```bash
$ mamba create --name artbox "python>=3.8.1,<3.12" pygobject pip
$ conda activate artbox
$ pip install artbox
```

## Examples

For the following examples, create the a temporary folder for artbox:

```bash
$ mkdir /tmp/artbox
```

### Convert text to audio

By default, the `artbox voice` uses
[`edge-tts`](https://pypi.org/project/edge-tts/) engine, but if you can also
specify [`gtts`](https://github.com/pndurette/gTTS) with the flag
`--engine gtts`.

```bash
$ echo "Are you ready to join Link and Zelda in fighting off this unprecedented threat to Hyrule?" > /tmp/artbox/text.md
$ artbox voice text-to-speech \
    --title artbox \
    --text-path /tmp/artbox/text.md \
    --output-path /tmp/artbox/voice.mp3 \
    --engine edge-tts
```

If you need to generate the audio for different language, you can use the flag
`--lang`:

```bash
$ echo "Bom dia, mundo!" > /tmp/artbox/text.md
$ artbox voice text-to-speech \
    --title artbox \
    --text-path /tmp/artbox/text.md \
    --output-path /tmp/artbox/voice.mp3 \
    --lang pt
```

If you are using `edge-tts` engine (the default one), you can also specify the
locale for that language, for example:

```bash
$ echo "Are you ready to join Link and Zelda in fighting off this unprecedented threat to Hyrule?" > /tmp/artbox/text.md
$ artbox voice text-to-speech \
    --title artbox \
    --text-path /tmp/artbox/text.md \
    --output-path /tmp/artbox/voice.mp3 \
    --engine edge-tts \
    --lang en-IN
```

### Download a youtube video

If you want to download videos from the youtube, you can use the following
command:

```bash
$ artbox youtube download \
    --url https://www.youtube.com/watch?v=zw47_q9wbBE \
    --output-path /tmp/artbox/
```

The command above downloads using a random resolution. If you want a specific
resolution, use the flat `--resolution`:

```bash
$ artbox youtube download \
    --url https://www.youtube.com/watch?v=zw47_q9wbBE \
    --output-path /tmp/artbox/ \
    --resolution 360p
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
