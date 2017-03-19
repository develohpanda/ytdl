"This is used for downloading a youtube video as mp3"

from __future__ import unicode_literals
import logging
import oshelper
import youtube_dl

class AudioDownload(object):
    "This is used for downloading a youtube video as mp3"

    def __init__(self, downloads_path):
        self.folders_with_lock_files = []
        if not oshelper.isdir(downloads_path):
            raise IOError('Folder {} does not exist'.format(downloads_path))

        self.downloads_path = downloads_path

    def __my_hook__(self, hook):
        "Fires when youtube_dl wants to send a notification of an event"

        if hook['status'] == 'downloading':
            folder_path = oshelper.os.path.dirname(hook['filename'])
            if oshelper.try_create_lock_file(folder_path):
                self.folders_with_lock_files.append(folder_path)

        if hook['status'] == 'finished':
            print 'Done downloading, now converting file ' + hook['filename']

    def download(self, urls):
        "Downloads a given list of urls as mp3"
        ydl_opts = {
            'format': 'bestaudio',
            'noplaylist': True,
            'writethumbnail': True,
            'writeinfojson': True,
            'outtmpl': 'c:/ytdl/downloads/%(id)s/%(title)s.%(ext)s',
            'logger': logging.getLogger(),
            'progress_hooks': [self.__my_hook__],
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }]
        }

        print 'Downloading ' + ', '.join(urls)

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download(urls)

        for folder in self.folders_with_lock_files:
            oshelper.try_delete_lock_file(folder)
