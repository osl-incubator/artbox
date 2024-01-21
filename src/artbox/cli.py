"""Cli functions to define the arguments and to call Makim."""
import typer

from typing_extensions import Annotated

from artbox import __version__
from artbox.sounds import Sound
from artbox.videos import Video, Youtube
from artbox.voices import Voice

app = typer.Typer(
    name="Artbox",
    help="A set of tools for handling multimedia files.",
    epilog=(
        "If you have any problem, open an issue at: "
        "https://github.com/ggpedia/artbox"
    ),
)

app_sound = typer.Typer(
    name="sound",
    help="Audio processing commands for Artbox.",
    short_help="Audio processing commands.",
)
app_video = typer.Typer(
    name="video",
    help="Video processing commands for Artbox.",
    short_help="Video processing commands.",
)
app_voice = typer.Typer(
    name="voice",
    help="Voice processing commands for Artbox.",
    short_help="Voice processing commands.",
)
app_youtube = typer.Typer(
    name="youtube",
    help="YouTube processing commands for Artbox.",
    short_help="YouTube processing commands.",
)

app.add_typer(app_sound, name="sound")
app.add_typer(app_video, name="video")
app.add_typer(app_voice, name="voice")
app.add_typer(app_youtube, name="youtube")


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        is_flag=True,
        help="Show the version and exit.",
    ),
) -> None:
    """Process commands for specific flags; otherwise, show the help menu."""
    if version:
        typer.echo(f"Version: {__version__}")
        raise typer.Exit()

    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())
        raise typer.Exit(0)


@app_voice.command("text-to-speech")
def text_to_speech(
    title: Annotated[
        str, typer.Option("--title", help="Specify the name of the audio file")
    ] = "artbox",
    text_path: Annotated[
        str,
        typer.Option("--text-path", help="Specify the path of the text file"),
    ] = "",
    output_path: Annotated[
        str,
        typer.Option(
            "--output-path", help="Specify the path to store the audio file"
        ),
    ] = "",
    engine: Annotated[
        str,
        typer.Option(
            "--engine",
            help="Choose the text-to-speech engine (Options: edge-tts, gtts)",
        ),
    ] = "edge-tts",
    lang: Annotated[
        str,
        typer.Option(
            "--lang", help="Choose the language for audio generation"
        ),
    ] = "en",
) -> None:
    """Convert text to speech."""
    args_dict = {
        "title": title,
        "text-path": text_path,
        "output-path": output_path,
        "engine": engine,
        "lang": lang,
    }

    runner = Voice(args_dict)
    runner.text_to_speech()


@app_sound.command("notes-to-audio")
def notes_to_audio(
    input_path: Annotated[
        str,
        typer.Option(
            "--input-path", help="Specify the path of the input file"
        ),
    ] = "",
    output_path: Annotated[
        str,
        typer.Option(
            "--output-path", help="Specify the path to store the audio file"
        ),
    ] = "",
    duration: Annotated[
        str,
        typer.Option("--duration", help="Specify the duration of the audio"),
    ] = "",
) -> None:
    """Convert notes to audio."""
    args_dict = {
        "input-path": input_path,
        "output-path": output_path,
        "duration": duration,
    }

    runner = Sound(args_dict)
    runner.notes_to_audio()


@app_video.command("remove-audio")
def remove_audio(
    input_path: Annotated[
        str,
        typer.Option(
            "--input-path", help="Specify the path of the input video file"
        ),
    ] = "",
    output_path: Annotated[
        str,
        typer.Option(
            "--output-path", help="Specify the path to store the video file"
        ),
    ] = "",
) -> None:
    """Remove audio from video file."""
    args_dict = {
        "input-path": input_path,
        "output-path": output_path,
    }

    runner = Video(args_dict)
    runner.remove_audio()


@app_video.command("extract-audio")
def extract_audio(
    input_path: Annotated[
        str,
        typer.Option(
            "--input-path", help="Specify the path of the input video file"
        ),
    ] = "",
    output_path: Annotated[
        str,
        typer.Option(
            "--output-path",
            help="Specify the path to store the extracted audio file",
        ),
    ] = "",
) -> None:
    """Extract audio from video file."""
    args_dict = {
        "input-path": input_path,
        "output-path": output_path,
    }

    runner = Video(args_dict)
    runner.extract_audio()


@app_video.command("combine-video-and-audio")
def combine_audio_and_video(
    video_path: Annotated[
        str,
        typer.Option(
            "--video-path", help="Specify the path of the video file"
        ),
    ] = "",
    audio_path: Annotated[
        str,
        typer.Option(
            "--audio-path", help="Specify the path of the audio file"
        ),
    ] = "",
    output_path: Annotated[
        str,
        typer.Option(
            "--output-path",
            help="Specify the path to store the combined video file",
        ),
    ] = "",
) -> None:
    """Combine audio and video files."""
    args_dict = {
        "video-path": video_path,
        "audio-path": audio_path,
        "output-path": output_path,
    }

    runner = Video(args_dict)
    runner.combine_video_and_audio()


@app_youtube.command("download")
def download_youtube_video(
    url: Annotated[
        str,
        typer.Option(
            "--url", help="Specify the URL of the YouTube video to download"
        ),
    ] = "",
    output_path: Annotated[
        str,
        typer.Option(
            "--output-path",
            help="Specify the path to store the downloaded video file",
        ),
    ] = "",
    resolution: Annotated[
        str,
        typer.Option(
            "--resolution", help="Set the quality of the downloaded video"
        ),
    ] = "",
) -> None:
    """Download youtube video."""
    args_dict = {
        "url": url,
        "output-path": output_path,
        "resolution": resolution,
    }

    runner = Youtube(args_dict)
    runner.download()
