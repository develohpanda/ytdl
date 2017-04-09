"This is used for downloading a youtube video as mp3"

from __future__ import unicode_literals

import logging

from youtube_dl import DownloadError, YoutubeDL

import oshelper
from models import DownloadResult


class AudioDownload(object):
    "This is used for downloading a youtube video as mp3"

    def __init__(self, config):
        self.download_folder = config.download_folder
        self.downloaded_to_folder = ''
        self.logger = logging.getLogger(__name__)

    def __my_hook__(self, hook):
        if hook['status'] == 'downloading':
            folder_path = oshelper.os.path.dirname(hook['filename'])
            oshelper.try_create_lock_file(folder_path)

        elif hook['status'] == 'finished':
            self.downloaded_to_folder = oshelper.os.path.dirname(hook['filename'])
            self.logger.info('Successfully downloaded, now converting...')

    def download(self, url):
        "Downloads a url as mp3"

        self.logger.info('Downloading %s', url)

        self.downloaded_to_folder = ''
        output_template = oshelper.join_paths(self.download_folder, '%(id)s')
        output_template = oshelper.join_paths(output_template, '%(title)s.%(ext)s')
        ydl_opts = {
            'format': 'bestaudio',
            'noplaylist': True,
            'writethumbnail': True,
            'writeinfojson': True,
            'outtmpl': output_template,
            'logger': logging.getLogger(),
            'progress_hooks': [self.__my_hook__],
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.logger.info('Conversion complete')
            return DownloadResult(True, self.downloaded_to_folder)
        except DownloadError as dlerror:
            self.logger.error(dlerror)
            return DownloadResult(False, 'Download failed')
        finally:
            oshelper.try_delete_lock_file(self.downloaded_to_folder)
