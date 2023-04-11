import json
import os

import whisper
from pytube import YouTube

from log import Log


class Transcriber:
    def __init__(self, video_id, video_title, video_description, audios_path, transcriptions_path, model_size="base"):
        """
        Object to download a video from YouTube, convert to mp3 and transcribe its content
        :param video_id: Video's YouTube ID
        :param video_title: Video's title
        :param video_description: Video's description
        :param audios_path: Path to save audio files
        :param transcriptions_path: Path to save transcription files
        """
        self.video_id = video_id
        self.video_title = video_title
        video_title_name = "".join(x for x in video_title if x.isalnum())
        self.video_description = video_description
        self.audios_path = audios_path
        self.audio_file = os.path.join(self.audios_path, f"{video_title_name}.mp3")
        self.transcription = ''
        self.transcriptions_path = transcriptions_path
        self.transcription_file = os.path.join(self.transcriptions_path, f"{video_title_name}.txt")
        self.check_paths_existence()
        self.whisper_model = whisper.load_model(model_size)

    def check_paths_existence(self):
        """
        Check and Create necessary folders to save the files.
        """
        # Create audios folder in case it does not exist
        if not os.path.exists(self.audios_path):
            os.makedirs(self.audios_path)

        # Create transcriptions folder in case it does not exist
        if not os.path.exists(self.transcriptions_path):
            os.makedirs(self.transcriptions_path)

    def download_mp3(self):
        """
        Downloads mp3 file in case there is no transcription file or audio file
        """
        # In case there is already a transcription file it is not necessary to download the audio file
        if os.path.exists(self.transcription_file):
            Log.log(f"{self.video_title}.txt already exists. Skipping download.")
            return

        # In case there is already an audio file it is not necessary to download again
        if os.path.exists(self.audio_file):
            Log.log(f"{self.video_title}.mp3 already exists. Skipping download.")
            return

        try:
            # Streaming video from YouTube
            Log.log(f"Streaming video for {self.video_title}...")
            yt = YouTube(f"https://www.youtube.com/watch?v={self.video_id}")
            video = yt.streams.filter(only_audio=True).first()

            # Downloading audio from the YouTube stream
            Log.log(f"Downloading audio for {self.video_title}...")
            out_file = video.download(output_path=self.audios_path)

            # Renaming to the expected audio file name
            os.rename(out_file, self.audio_file)
            Log.log(f"{self.video_title}.mp3 has been successfully downloaded.")
        except Exception as e:
            Log.log(f"Error downloading audio for {self.video_title}: {e}", level='exception')

    def transcribe_audio(self):
        """
        Transcribe from the audio file in case it exists
        """
        # Checking if the transcription file already exists
        if os.path.exists(self.transcription_file):
            Log.log(f"{self.video_title}.txt already exists. Skipping transcription.")

        # Checking if the audio file exists
        elif not os.path.exists(self.audios_path):
            Log.log(f"{self.video_title}.mp3 doesn't exists. Skipping transcription.")

        # Transcribing
        else:
            result = self.whisper_model.transcribe(self.audio_file)
            self.transcription = result["text"]
            Log.log(f"{self.video_title} has been successfully transcribed.")

    def save_transcription(self, delete_audio=True):
        """
        Save the transcription in a file
        :param delete_audio: If True deletes the audio file after the transcription
        """
        if self.transcription != '':
            with open(self.transcription_file, "w") as f:
                f.write(f"Video Title: {self.video_title}\n")
                f.write(f"Video Description: {self.video_description}\n")
                f.write("Transcription:\n")
                f.write(self.transcription)
            Log.log(f"{self.video_title} transcription has been successfully saved.")

            # Deletes the audio file
            if delete_audio and os.path.exists(self.transcription_file) and os.path.exists(self.audio_file):
                os.remove(self.audio_file)

    @staticmethod
    def load_transcriptions(videos_file, audios_path, transcriptions_path):
        """
        Transcribes all videos in the videos_file
        :param videos_file: Path to the videos file
        :param audios_path: Path to save audio files
        :param transcriptions_path: Path to save transcription files
        """
        # Load videos list from file
        with open(videos_file, "r") as f:
            videos_list = json.load(f)

        # Process each video
        for video in videos_list:
            transcriber = Transcriber(video["id"], video["title"], video["description"],
                                      audios_path, transcriptions_path)
            transcriber.download_mp3()
            transcriber.transcribe_audio()
            transcriber.save_transcription()
