"This is used for downloading a youtube video as mp3"

from __future__ import unicode_literals
import logging
import oshelper
import youtube_dl

class DownloadResult(object):
    "Represents the result of downloading tracks"

    def __init__(self, successful_urls, failed_urls):
        self.successful_urls = successful_urls
        self.failed_urls = failed_urls

class AudioDownload(object):
    "This is used for downloading a youtube video as mp3"

    def __init__(self, downloads_path):
        self.folders_with_lock_files = []
        self.failed_urls = []
        self.successful_urls = []

        self.downloads_path = downloads_path

    def __my_hook__(self, hook):
        if hook['status'] == 'error':
            self.failed_urls.append(u'url')

        elif hook['status'] == 'downloading':
            folder_path = oshelper.os.path.dirname(hook['filename'])
            if oshelper.try_create_lock_file(folder_path):
                self.folders_with_lock_files.append(folder_path)

        elif hook['status'] == 'finished':
            self.successful_urls.append(u'url')

    def download(self, urls):
        "Downloads a given list of urls as mp3"
        output_template = oshelper.os.path.join(self.downloads_path, '/%(id)s/%(title)s.%(ext)s')
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

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download(urls)
        for folder in self.folders_with_lock_files:
            oshelper.try_delete_lock_file(folder)

        return DownloadResult(self.successful_urls, self.failed_urls)
