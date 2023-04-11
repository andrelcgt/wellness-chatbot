import fnmatch
import logging
import os
import re

from config import log_path


class Log:
    _logger = None

    @classmethod
    def create_logger(cls, name='std'):
        """
        Creates logger file if it is not created already
        @param name: name of the file
        """
        if cls._logger is None:
            handlers = [logging.FileHandler(cls._get_file_name(name), 'w', 'utf-8')]
            for handler in logging.root.handlers[:]:
                logging.root.removeHandler(handler)
            logging.basicConfig(handlers=handlers, format='%(asctime)s %(message)s')
            cls._logger = logging.getLogger()
            cls._logger.setLevel(logging.INFO)
            cls.log('==================== start ====================')

    @classmethod
    def log(cls, msg, level='info', print_msg=True):
        """
        Log the msg
        @param msg: Message
        @param level: level of message importance. debug, info, warning, error, exception, critical
        @param print_msg: True to print the message, False to not print the message
        """
        cls.create_logger()

        # log the msg
        getattr(cls._logger, level)(msg)

        # print the msg
        if print_msg:
            print(msg)

    @staticmethod
    def _get_file_name(file_name):
        """
        Gets the file name to be used. If the same name already exists returns that name with a counter
        @param file_name: name of the file
        @return: name of the file with the counter
        """
        extension = '.log'
        files = fnmatch.filter(os.listdir(log_path), file_name + '*')

        if len(files) == 0:
            count = 1
        else:
            for i, file in enumerate(files, start=0):
                files[i] = int(re.search(file_name + '(.+?)' + extension, file).group(1))
            count = max(files) + 1
        return f'{log_path}/{file_name}{count}{extension}'
