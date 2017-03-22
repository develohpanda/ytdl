"This is used for downloading a youtube video as mp3"

import logging

from youtube_dl import YoutubeDL, DownloadError

import oshelper
from models import DownloadResult

class AudioDownload(object):
    "This is used for downloading a youtube video as mp3"

    def __init__(self, downloads_path):
        self.downloads_path = downloads_path
        self.downloaded_to_folder = ''

    def __my_hook__(self, hook):
        if hook['status'] == 'downloading':
            folder_path = oshelper.os.path.dirname(hook['filename'])
            oshelper.try_create_lock_file(folder_path)

        elif hook['status'] == 'finished':
            self.downloaded_to_folder = oshelper.os.path.dirname(hook['filename'])
            logging.info('Successfully downloaded, now converting...')

    def download(self, url):
        "Downloads a url as mp3"

        logging.info('Downloading %s', url)

        self.downloaded_to_folder = ''
        output_template = oshelper.join_paths(self.downloads_path, '%(id)s\\%(title)s.%(ext)s')
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
            logging.info('Conversion complete')
            return DownloadResult(True, self.downloaded_to_folder)
        except DownloadError as dlerror:
            logging.error(dlerror)
            return DownloadResult(False, 'Download failed')
        finally:
            oshelper.try_delete_lock_file(self.downloaded_to_folder)
