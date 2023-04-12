import os

import pandas as pd
import whisper
from pytube import YouTube

from config import *


class Transcriber:
    def __init__(self, video_url, video_title):
        """
        Object to download a video from YouTube, convert to mp3 and transcribe its content
        :param video_url: Video's YouTube URL
        :param video_title: Video's title
        """
        self.transcription = ''
        self.video_url = video_url
        self.video_title = video_title
        video_title_name = "".join(x for x in video_title if x.isalnum())
        self.audio_file = os.path.join(audios_path, f"{video_title_name}.mp3")
        self.transcription_file = os.path.join(transcriptions_path, f"{video_title_name}.txt")
        self.whisper_model = whisper.load_model(model_size)

    def download_mp3(self):
        """
        Downloads mp3 file in case there is no transcription file or audio file
        """
        # In case there is already a transcription file it is not necessary to download the audio file
        if os.path.exists(self.transcription_file):
            Log.log(f"Skipping download. {self.video_title}.txt already exists.")
            return

        # In case there is already an audio file it is not necessary to download again
        if os.path.exists(self.audio_file):
            Log.log(f"Skipping download. {self.video_title}.mp3 already exists.")
            return

        try:
            # Streaming video from YouTube
            Log.log(f"Streaming video for {self.video_title}...")
            yt = YouTube(self.video_url)
            video = yt.streams.filter(only_audio=True).first()

            # Downloading audio from the YouTube stream
            Log.log(f"Downloading audio for {self.video_title}...")
            out_file = video.download(output_path=audios_path)

            # Renaming to the expected audio file name
            os.rename(out_file, self.audio_file)
            Log.log(f"Successfully downloaded {self.video_title}.mp3")
        except Exception as e:
            Log.log(f"Error downloading audio for {self.video_title}: {e}", level='exception')

    def transcribe_audio(self):
        """
        Transcribe from the audio file in case it exists
        """
        # Checking if the transcription file already exists
        if os.path.exists(self.transcription_file):
            Log.log(f"Skipping transcription. {self.video_title}.txt already exists.")

        # Checking if the audio file exists
        elif not os.path.exists(self.audio_file):
            Log.log(f"Skipping transcription. {self.video_title}.mp3 doesn't exists.")

        # Transcribing
        else:
            result = self.whisper_model.transcribe(self.audio_file)
            self.transcription = result["text"]
            Log.log(f"Successfully transcribed {self.video_title}.")

    def save_transcription(self, delete_audio=True):
        """
        Save the transcription in a file
        :param delete_audio: If True deletes the audio file after the transcription
        """
        if self.transcription != '':
            yt = YouTube(self.video_url)
            with open(self.transcription_file, "w", encoding="utf-8") as f:
                f.write(f"Video Author: {yt.author}\n")
                f.write(f"Video Title: {self.video_title}\n")
                f.write(f"Video URL: {self.video_url}\n")
                f.write(f"Video Description: {yt.description}\n")
                f.write("Transcription:\n")
                f.write(self.transcription)
            Log.log(f"Transcription has been successfully saved for {self.video_title}.")

            # Deletes the audio file
            if delete_audio and os.path.exists(self.transcription_file) and os.path.exists(self.audio_file):
                os.remove(self.audio_file)

    @staticmethod
    def load_transcriptions():
        """
        Transcribes all videos
        """

        videos_files = os.listdir(videos_list_path)
        videos_db = pd.DataFrame()
        for file in videos_files:
            file = os.path.join(videos_list_path, file)
            videos = pd.read_csv(file)
            videos_db = pd.concat([videos_db, videos], ignore_index=True)

        # Process each video
        for index, video in videos_db.iterrows():
            transcriber = Transcriber(video["Video URL"], video["Video Title"])
            transcriber.download_mp3()
            transcriber.transcribe_audio()
            transcriber.save_transcription()
