"Main"

import datetime
import time
import logging
import os

import oshelper
from ytdl import Ytdl


def main():
    "Main"
    logging.getLogger('').handlers = []
    logs_file_path = 'c:\\users\\opend\\ytdl\\logs'
    oshelper.mkdir(logs_file_path)
    logs_file_name = os.path.join(logs_file_path, str(datetime.date.today()) + ".log")

    logging.basicConfig(
        filename=logs_file_name,
        level=logging.INFO,
        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p')

    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)

    Ytdl().run()

    current_time = time.time()

    for file_name in os.listdir(logs_file_path):
        creation_time = os.path.getctime(file_name)
        if (current_time - creation_time) // (24 * 3600) >= 7:
            os.unlink(file_name)
            logging.info('Removed %s', file_name)

if __name__ == '__main__':
    main()
