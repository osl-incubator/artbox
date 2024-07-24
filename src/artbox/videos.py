"""
Set of tools for video handling.

ref: https://github.com/ethand91/python-youtube/blob/master/main.py
"""

from __future__ import annotations

from abc import abstractmethod

import ffmpeg

from moviepy.editor import (
    AudioFileClip,
    CompositeAudioClip,
    ImageClip,
    VideoFileClip,
)
from pytubefix import YouTube as PyYouTube

from artbox.base import ArtBox


class DownloadBase(ArtBox):
    """Set of tools for handing videos."""

    @abstractmethod
    def download(self):
        """Download a video."""
        ...


def _convert_srt_to_plain_text(srt_text: str) -> str:
    """
    Convert an SRT file to plain text by removing timestamps and formatting.

    Parameters
    ----------
    srt_file_path (str): Path to the SRT file.

    Returns
    -------
    str: The extracted plain text from the SRT file.
    """
    plain_text = []
    # Skip lines that are part of SRT formatting (timestamps, etc.)
    for line in srt_text.split("\n"):
        if line.strip() and not line.strip().isdigit() and "-->" not in line:
            plain_text.append(line.strip())

    return "\n".join(plain_text)


class Youtube(DownloadBase):
    """Set of tools for handing videos."""

    def download(self):
        """Download a youtube video."""
        resolution = self.args.get("resolution", "")
        video_url = self.args.get("url", "")

        if not video_url:
            raise Exception("Argument `url` not given.")

        video = PyYouTube(video_url)

        # Filter the stream by resolution if provided,
        # else get the highest resolution
        if resolution:
            video_stream = video.streams.filter(
                res=resolution, file_extension="mp4"
            ).first()
            if video_stream is None:
                raise Exception(
                    f"No video stream found with resolution {resolution}."
                )
        else:
            video_stream = video.streams.get_highest_resolution()

        try:
            video_stream.download(str(self.output_path))
            print("Video was downloaded successfully")
        except Exception as e:
            print(f"Failed to download video: {e}")

    def download_captions(self):
        """Download the English closed captions of a YouTube video."""
        video_url = self.args.get("url", "")
        lang = self.args.get("lang", "en")
        format = self.args.get("format", "text")

        yt = PyYouTube(video_url)
        caption = yt.captions.get_by_language_code(f"a.{lang}")

        if not caption:
            print(f"No captions found for language {lang}.")
            return

        # Save the captions to a file
        cc = caption.generate_srt_captions()
        with open(str(self.output_path), "w") as f:
            if format == "text":
                cc = _convert_srt_to_plain_text(cc)
            f.write(cc)
        print("Captions downloaded successfully.")


class Video(ArtBox):
    """Set of tools for handing videos."""

    def combine_video_and_audio(self) -> None:
        """Combine audio and video files."""
        video_path = self.args.get("video-path", "")
        audio_paths: list[str] = self.args.get("audio-paths", "").split(",")
        output_path = str(self.output_path)

        # Load the video file
        video_clip = VideoFileClip(video_path)

        # Load audio files
        audio_clips = [AudioFileClip(audio_path) for audio_path in audio_paths]

        # Overlay all audio clips on top of each other
        combined_audio = CompositeAudioClip(audio_clips)

        # Set the audio of the video clip to the combined audio
        final_clip = video_clip.set_audio(combined_audio)

        # Export the final video
        final_clip.write_videofile(
            output_path, codec="libx264", audio_codec="aac"
        )

        # Close all clips
        video_clip.close()
        final_clip.close()

        for audio_clip in audio_clips:
            audio_clip.close()

    def crop(self) -> None:
        """
        Crop a video to the specified time range.

        Notes
        -----
        - video_path: Path to the input video file.
        - start_time: Start time in seconds.
        - end_time: End time in seconds.
        - output_path: Path to save the cropped video file.
        """
        video_path = self.input_path
        start_time = float(self.args.get("start-time", "0"))
        end_time = float(self.args.get("end-time", "0"))
        output_path = self.output_path
        fade_duration = 1

        # Load the video file
        video_clip = VideoFileClip(str(video_path))

        # If end_time is 0 or not provided, set it to the duration of the video
        if end_time == 0:
            end_time = video_clip.duration

        # Crop the video to the specified time range
        cropped_clip = video_clip.subclip(start_time, end_time)

        # Apply fade-in effect if start_time > 0
        if start_time > 0:
            cropped_clip = cropped_clip.fadein(fade_duration)

        # Apply fade-out effect
        cropped_clip = cropped_clip.fadeout(fade_duration)

        # Export the cropped video with fade effects to a new file
        cropped_clip.write_videofile(str(output_path), codec="libx264")

    def extract_audio(self) -> None:
        """Extract audio from an MP4 file."""
        video_path = str(self.input_path)
        output_path = str(self.output_path)

        video_clip = VideoFileClip(video_path)
        audio_clip = video_clip.audio
        audio_clip.write_audiofile(output_path)
        audio_clip.close()
        video_clip.reader.close()

        print(f"Audio has been extracted. Output saved at '{output_path}'.")

    def get_metadata(self) -> None:
        """
        Extract metadata from an MP4 file using moviepy.

        Returns
        -------
        Metadata of the MP4 file.
        """
        file_path = str(self.input_path)

        try:
            probe = ffmpeg.probe(file_path)
            general_metadata = probe.get("format", {})
            streams_metadata = probe.get("streams", [])

            detailed_metadata = {
                "format": general_metadata.get("format_name"),
                "duration": general_metadata.get("duration"),
                "size": general_metadata.get("size"),
                "bit_rate": general_metadata.get("bit_rate"),
                "tags": general_metadata.get("tags", {}),
                "streams": [],
            }

            for stream in streams_metadata:
                stream_info = {
                    "index": stream.get("index"),
                    "type": stream.get("codec_type"),
                    "codec": stream.get("codec_name"),
                    "profile": stream.get("profile"),
                    "resolution": (
                        f"{stream.get('width')}x{stream.get('height')}"
                        if stream.get("codec_type") == "video"
                        else None
                    ),
                    "bit_rate": stream.get("bit_rate"),
                    "sample_rate": stream.get("sample_rate")
                    if stream.get("codec_type") == "audio"
                    else None,
                    "channels": stream.get("channels")
                    if stream.get("codec_type") == "audio"
                    else None,
                    "tags": stream.get("tags", {}),
                }
                detailed_metadata["streams"].append(stream_info)

        except Exception as e:
            print(f"An error occurred: {e}")
            return

        with open(self.output_path, "w") as f:
            f.write(str(detailed_metadata))
        print(detailed_metadata)

    def remove_audio(self) -> None:
        """Remove the audio from an MP4 file."""
        # Load the video
        video = VideoFileClip(str(self.input_path))

        # Set the audio track to None
        video = video.set_audio(None)

        # Write the result to a file
        video.write_videofile(str(self.output_path), codec="libx264")

    def image_to_video(self) -> None:
        """Convert a static image to a video with a given duration."""
        image_path = str(self.input_path)
        output_path = str(self.output_path)
        duration = float(self.args.get("duration", "1"))
        fps = 24

        # Load the image
        clip = ImageClip(image_path, duration=duration)

        # Set the frame rate
        clip = clip.set_fps(fps)

        # Write the video file
        clip.write_videofile(output_path, codec="libx264")
