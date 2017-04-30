"process"

import datetime
import logging
import os
import sys
import time

from ytdl.downloadupload import Downloadupload
from ytdl.oshelper import absolute_files, mkdir, remove
from ytdl.ytdlconfiguration import Ytdlconfiguration


def configure_loggers(config):
    "Configure logger"

    logging.getLogger('').handlers = []

    mkdir(config.log_folder)
    logs_file_name = os.path.join(config.log_folder, str(
        datetime.date.today()) + "process.log")

    logging.basicConfig(
        filename=logs_file_name,
        level=logging.INFO,
        format='%(asctime)s %(name)-20s %(levelname)-8s %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p')

    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(name)-20s: %(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)

    sys.excepthook = handle_exception


def handle_exception(exc_type, exc_value, exc_traceback):
    "Handle uncaught exception"
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logger = logging.getLogger(__name__)
    logger.error("Uncaught exception", exc_info=(
        exc_type, exc_value, exc_traceback))


def remove_old_log_files(config):
    "Remove old log files"

    current_time = time.time()

    for file_name in absolute_files(config.log_folder):
        creation_time = os.path.getctime(file_name)
        if (current_time - creation_time) // (24 * 3600) >= 7:
            remove(file_name)
            logging.info('Removed %s', file_name)


def process():
    "process"

    config = Ytdlconfiguration()

    configure_loggers(config)

    config.load()

    if not config.is_valid():
        logger = logging.getLogger(__name__)
        logger.error("Invalid config at %s", config.config_file_path)
        return

    Downloadupload(config).download_and_upload()

    remove_old_log_files(config)


if __name__ == '__main__':
    process()
