"Main"

import os
import datetime
import logging
from ytdl import Ytdl

def main():
    "Main"
    logging.getLogger('').handlers = []

    #oshelper.mkdir(oshelper.dirname(logs_file_path))
    logging.basicConfig(
        filename=os.path.join(
            'c:\\users\\opend\\ytdl\\logs',
            str(datetime.date.today()) + ".log"),
        level=logging.DEBUG,
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

if __name__ == '__main__':
    main()
