"""
ref: https://github.com/ethand91/python-youtube/blob/master/main.py
"""
from pathlib import Path

from moviepy.editor import AudioFileClip, VideoFileClip
from pytube import YouTube

from artbox.constants import AUDIOS_PATH, MEDIA_PATH, RESULTS_PATH, VIDEOS_PATH


def download(video_url: str):
    video = YouTube(video_url)
    video = video.streams.get_highest_resolution()

    try:
        video.download(str(VIDEOS_PATH))
    except:
        print("Failed to download video")

    print("video was downloaded successfully")


def combine_video_audio(
    video_path: str, audio_path: str, output_path: str
) -> None:
    """
    Combine video from an MP4 file and audio from an MP3 file to create a new MP4 file.
    The result will be clipped to the time of the shorter input (video or audio), and the audio
    will fade out smoothly over the last 5 seconds.

    Parameters
    ----------
    video_path : str
        Path to the input video file (MP4).
    audio_path : str
        Path to the input audio file (MP3).
    output_path : str
        Path to save the combined video and audio (MP4).
    """
    # Load the video (without audio) from the MP4 file
    video_clip = VideoFileClip(video_path)
    video_clip = video_clip.without_audio()

    # Load the audio from the MP3 file
    audio_clip = AudioFileClip(audio_path)

    # Determine the shorter duration of the two clips
    min_duration = min(video_clip.duration, audio_clip.duration)

    # Clip both the video and audio to the shorter duration
    video_clip = video_clip.subclip(0, min_duration)
    audio_clip = audio_clip.subclip(0, min_duration)

    # Apply a 5-second fade-out effect to the audio
    audio_clip = audio_clip.audio_fadeout(5)

    # Set the audio of the video clip
    final_clip = video_clip.set_audio(audio_clip)

    # Write the result to the output file
    final_clip.write_videofile(output_path, codec="libx264")

    # Close all clips
    video_clip.close()
    audio_clip.close()
    final_clip.close()


def remove_audio(input_file: Path, output_file: Path) -> None:
    """
    Remove the audio from an MP4 file.

    Parameters
    ----------
    input_file : Path
        Path to the input MP4 file.
    output_file : Path
        Path to the output MP4 file with audio removed.
    """

    # Load the video
    video = VideoFileClip(str(input_file))

    # Set the audio track to None
    video = video.set_audio(None)

    # Write the result to a file
    video.write_videofile(str(output_file), codec="libx264")
