from config import *
from transcriber import Transcriber
from videos import Videos
from makeindex import MakeIndex


def start():
    print("Menu:")
    print("1: Get list of videos")
    print("2: Transcribe videos")
    print("3: Create Index")
    print("0: Exit")
    value = input("What would you like to do?")

    if value == "1":
        Videos().get_videos_lists()
    elif value == "2":
        Transcriber.load_transcriptions()
    elif value == "3":
        MakeIndex.construct_index()
    elif value == "0":
        print("Bye Bye")
        return
    else:
        print("!!! Wrong option. Try again.")
    start()


if __name__ == '__main__':
    Log.create_logger("backend_main")
    start()
