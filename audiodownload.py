"This is used for downloading a youtube video as mp3"

from __future__ import unicode_literals
import logging
import youtube_dl

def my_hook(hook):
    "Fires when youtube_dl wants to send a notification of an event"
    if hook['status'] == 'finished':
        print 'Done downloading, now converting file ' + hook['filename']

def ytdownload(urls):
    "Downloads a given list of urls as mp3"
    ydl_opts = {
        'format': 'bestaudio',
        'noplaylist': True,
        'writethumbnail': True,
        'writeinfojson': True,
        'outtmpl': 'c:/ytdl/downloads/%(id)s/%(title)s.%(ext)s',
        'logger': logging.getLogger(),
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
