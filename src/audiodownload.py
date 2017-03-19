"This is used for downloading a youtube video as mp3"

from __future__ import unicode_literals
import logging
import oshelper
import youtube_dl

class DownloadResult(object):
    "Represents the result of downloading tracks"

    def __init__(self, success, message):
        self.success = success
        self.message = message

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

    def download(self, url):
        "Downloads a url as mp3"
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
                'preferredquality': '320',
            }]
        }

        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            return DownloadResult(True, self.downloaded_to_folder)
        except  youtube_dl.DownloadError as dlerror:
            return DownloadResult(False, dlerror.message)
        finally:
            oshelper.try_delete_lock_file(self.downloaded_to_folder)
