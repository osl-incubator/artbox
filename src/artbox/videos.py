"""
Set of tools for video handling.

ref: https://github.com/ethand91/python-youtube/blob/master/main.py
"""
from abc import abstractmethod

from moviepy.editor import AudioFileClip, VideoFileClip
from pytube import YouTube

from artbox.base import ArtBox


class DownloadBase(ArtBox):
    """Set of tools for handing videos."""

    @abstractmethod
    def download(self):
        """Download a video."""
        ...


class Youtube(DownloadBase):
    """Set of tools for handing videos."""

    def download(self):
        """Download a youtube video."""
        resolution = self.args.get("resolution", "")
        video_url = self.args.get("url", "")

        if not video_url:
            raise Exception("Argument `url` not given.")

        video = YouTube(video_url)

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


class Video(ArtBox):
    """Set of tools for handing videos."""

    def combine_video_and_audio(self) -> None:
        """
        Combine video and audio files to create a new MP4 file.

        The result will be clipped to the time of the shorter input
        (video or audio), and the audio will fade out smoothly over the last
        5 seconds.
        """
        video_path = self.args.get("video-path", "")
        audio_path = self.args.get("audio-path", "")
        output_path = str(self.output_path)

        if not video_path:
            raise Exception("Argument `video-path` not given.")

        if not audio_path:
            raise Exception("Argument `audio-path` not given.")

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

    def remove_audio(self) -> None:
        """Remove the audio from an MP4 file."""
        # Load the video
        video = VideoFileClip(str(self.input_path))

        # Set the audio track to None
        video = video.set_audio(None)

        # Write the result to a file
        video.write_videofile(str(self.output_path), codec="libx264")
