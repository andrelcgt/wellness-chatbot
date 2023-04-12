import os
import shutil

from yt_videos_list import ListCreator

from config import *


class Videos:
    channel_id = 'UCxHTM1FYxeC4F7xDsBVltGg'

    def __init__(self, driver='chrome'):
        """
        Object to create a list of video files from YouTube
        :param driver: Driver to use to scrape YouTube
        """
        self.driver = driver

    def get_videos_lists(self):
        """
        Gets video list files from YouTube
        """
        Log.log("Getting videos list ...")

        # Create csv and log file for each YouTube channel in channels_file
        lc = ListCreator(driver=self.driver, txt=False, md=False, headless=True,
                         all_video_data_in_memory=True, video_data_returned=True)
        lc.create_list_from(path_to_channel_urls_file=channels_file)

        # Move csv and log files to correct folder
        self._move_files('.log', log_path)
        self._move_files('.csv', videos_list_path)
        Log.log("Videos list has been successfully saved.")

    @staticmethod
    def _move_files(ext, destination_path):
        """
        Move files from ext extension to destination_path
        :param ext: extension of the files
        :param destination_path: Path to move the files
        """
        source_path = './'
        source_files = os.listdir(source_path)
        for file in source_files:
            if file.endswith(ext):
                shutil.move(os.path.join(source_path, file), os.path.join(destination_path, file))
