"Main"

import os
import datetime
import logging
from ytdl import Ytdl

def main():
    "Main"
    #oshelper.mkdir(oshelper.dirname(logs_file_path))
    logging.basicConfig(
        filename=os.path.join(
            'c:\\users\\opend\\ytdl\\logs',
            str(datetime.date.today()) + ".log"),
        level=logging.DEBUG,
        format='%(asctime)s %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p')

    logging.debug("test")

    Ytdl().run()

if __name__ == '__main__':
    main()
