import json
import os

from googleapiclient.discovery import build

from log import Log


class Videos:
    channel_id = 'UCxHTM1FYxeC4F7xDsBVltGg'

    def __init__(self, videos_file):
        """
        Object to create a list of video files from YouTube
        :param videos_file: Path to the videos file
        """
        # Access to YouTube
        self.youtube = build('youtube', 'v3', developerKey=os.environ['YOUTUBE-KEY-FILE'])
        self.videos_file = videos_file

    def get_videos_list(self, channel_id):
        """
        Gets the list of videos from the channel_id
        :param channel_id: ID of the YouTube channel
        """
        Log.log(f"Getting videos list for channel_id:{channel_id}...")

        request = self.youtube.search().list(
            part='snippet',
            channelId=channel_id,
            type='video',
            videoDuration='long',
            maxResults=500
        )
        response = request.execute()

        # Parse the response
        videos = []
        for item in response['items']:
            video_id = item['id']['videoId']
            video_title = item['snippet']['title']
            video_description = item['snippet']['description']
            videos.append({'id': video_id,
                           'title': video_title,
                           'description': video_description})

        # Write the video data to a text file
        with open(self.videos_file, 'w') as f:
            json.dump(videos, f, indent=2)

        Log.log(f"{self.channel_id} videos list has been successfully saved.")

    @staticmethod
    def load_videos(videos_file):
        """
        Loads video files from YouTube
        :param videos_file: Path to the videos file
        """
        videos_list = Videos(videos_file)
        videos_list.get_videos_list(Videos.channel_id)
