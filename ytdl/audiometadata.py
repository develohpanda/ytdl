"Apply audio metadata"

import logging
import eyed3
from PIL import Image

import oshelper
from customerrors import FileNotFoundError

class AudioMetadata(object):
    "Responsible for applying metadata to file"

    def __init__(self, track_file):
        self.track_file = track_file
        self.logger = logging.getLogger(__name__)

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
            self.logger.warning('No album art file present')
            return

        self.logger.info('Resizing cover art %s', album_art_file)

        resized_album_art_file = self.__resize__(album_art_file)

        self.logger.info('Embedding cover art %s', resized_album_art_file)

        audiofile = self.__load__()
        audiofile.tag.images.set(3, open(resized_album_art_file, 'rb').read(), 'image/jpeg')
        audiofile.tag.save()

    def __resize__(self, album_art_file):
        size = tuple([1000, 1000])
        dirname = oshelper.dirname(album_art_file)
        filename = oshelper.filename_no_extension(album_art_file)
        resized_album_art_file = oshelper.join_paths(dirname, filename + '-resized.png')

        image = Image.open(album_art_file)
        image.thumbnail(size, Image.ANTIALIAS)

        offset_x = max((size[0] - image.size[0]) / 2, 0)
        offset_y = max((size[1] - image.size[1]) / 2, 0)
        offset_tuple = (offset_x, offset_y)

        final_thumb = Image.new(mode='RGBA', size=size, color=(0, 0, 0, 255))
        final_thumb.paste(image, offset_tuple)
        final_thumb.save(resized_album_art_file, 'PNG')

        return resized_album_art_file

    def apply_track_info(self, info):
        "Applies the track info into the mp3 file"

        self.logger.info('Applying media tags')

        audiofile = self.__load__()

        audiofile.tag.artist = info.uploader
        audiofile.tag.album_artist = info.uploader
        audiofile.tag.album = info.full_title
        audiofile.tag.title = info.full_title
        audiofile.tag.comments.set(info.url)
        audiofile.tag.save()
