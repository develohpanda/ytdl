"This is used for downloading a youtube video as mp3"

from __future__ import unicode_literals
import youtube_dl

class MyLogger(object):
    "Logger passthrough that only prints errors"
    def debug(self, msg):
        "Passthrough"
        pass

    def warning(self, msg):
        "Passthrough"
        pass

    def error(self, msg):
        """Print errors"""
        print msg

def my_hook(hook):
    "Fires when youtube_dl wants to send a notification of an event"
    if hook['status'] == 'finished':
        print 'Done downloading, now converting...'

def ytdownload(urls):
    "Downloads a given list of urls as mp3"
    ydl_opts = {
        'format': 'bestaudio',
        'noplaylist': True,
        'writethumbnail': True,
        'writeinfojson': True,
        'outtmpl': '../downloads/%(id)s/%(title)s.%(ext)s',
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    }

    print 'Downloading ' + ', '.join(urls)

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(urls)

ytdownload(['https://www.youtube.com/watch?v=ouycfHgjky4'])
