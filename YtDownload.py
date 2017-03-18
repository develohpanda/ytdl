"This is used for downloading a youtube video as mp3"

from __future__ import unicode_literals
import youtube_dl

class MyLogger(object):
    "Logger passthrough that only prints errors"
    def debug(self, msg):
        """Passthrough"""
        pass

    def warning(self, msg):
        """Passthrough"""
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
        'sleep_interval': 5,
        'max_sleep_interval': 10,
        'logger': MyLogger(),
        'progress_hooks': [my_hook]
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(urls)

if __name__ is '__main__':
    ytdownload('https://www.youtube.com/watch?v=EsefK-eyiPo')
