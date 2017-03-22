"Apply audio metadata"

import logging
import eyed3

import oshelper
from customerrors import FileNotFoundError

class AudioMetadata(object):
    "Responsible for applying metadata to file"

    def __init__(self, track_file):
        self.track_file = track_file

    def __load__(self):
        try:
            audiofile = eyed3.load(self.track_file)
        except IOError as ioerror:
            raise FileNotFoundError(ioerror.filename)
        else:
            if audiofile.tag is None:
                audiofile.initTag()
            return audiofile

    def apply_album_art(self, album_art_file):
        "Applies the album art into the mp3 file"
        if album_art_file == oshelper.DEFAULT_FILE_NAME:
            logging.warning('No album art file present')
            return

        logging.warning('Embedding cover art %s', album_art_file)

        audiofile = self.__load__()
        audiofile.tag.images.set(3, open(album_art_file, 'rb').read(), 'image/jpeg')
        audiofile.tag.save()

    def apply_track_info(self, info):
        "Applies the track info into the mp3 file"

        logging.warning('Applying media tags')

        audiofile = self.__load__()

        audiofile.tag.artist = info.uploader
        audiofile.tag.album_artist = info.uploader
        audiofile.tag.album = info.full_title
        audiofile.tag.title = info.full_title
        audiofile.tag.date = info.upload_year
        audiofile.tag.comments.set(info.url)
        audiofile.tag.save()
