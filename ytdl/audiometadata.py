"Apply audio metadata"

import logging

from mutagen.easyid3 import EasyID3
from mutagen.id3 import APIC, ID3, error
from mutagen.mp3 import MP3
from PIL import Image
from ytdl.customerrors import FileNotFoundError
from ytdl.oshelper import (DEFAULT_FILE_NAME, dirname, filename_no_extension,
                           join_paths)


class AudioMetadata(object):
    "Responsible for applying metadata to file"

    def __init__(self, track_file):
        self.track_file = track_file
        self.logger = logging.getLogger(__name__)

    def __load__(self):
        try:
            audiofile = MP3(self.track_file, ID3=ID3)
        except IOError as ioerror:
            raise FileNotFoundError(ioerror.filename)
        else:
            try:
                audiofile.add_tags()
            except error:
                pass
            return audiofile

    def apply_album_art(self, album_art_file):
        "Applies the album art into the mp3 file"
        if album_art_file == DEFAULT_FILE_NAME:
            self.logger.warning('No album art file present')
            return

        self.logger.info('Resizing cover art %s', album_art_file)

        resized_album_art_file = self.__resize__(album_art_file)

        self.logger.info('Embedding cover art %s', resized_album_art_file)

        audiofile = self.__load__()
        data = open(resized_album_art_file, 'rb').read()
        audiofile.tags.add(
            APIC(
                encoding=3,  # 3 is for utf-8
                mime='image/jpeg',  # image/jpeg or image/png
                type=3,  # 3 is for the cover image
                desc=u'Cover',
                data=data
            )
        )
        audiofile.save(v2_version=3)

    def __resize__(self, album_art_file):
        size = tuple([1000, 1000])
        directory_name = dirname(album_art_file)
        filename = filename_no_extension(album_art_file)
        resized_album_art_file = join_paths(
            directory_name, filename + '-resized.png')

        image = Image.open(album_art_file)
        image.thumbnail(size, Image.ANTIALIAS)

        offset_x = max((size[0] - image.size[0]) / 2, 0)
        offset_y = max((size[1] - image.size[1]) / 2, 0)
        offset_tuple = (int(offset_x), int(offset_y))

        final_thumb = Image.new(mode='RGBA', size=size, color=(0, 0, 0, 255))
        final_thumb.paste(image, offset_tuple)
        final_thumb.save(resized_album_art_file, 'PNG')

        return resized_album_art_file

    def apply_track_info(self, info):
        "Applies the track info into the mp3 file"

        self.logger.info('Applying media tags')

        audiofile = EasyID3(self.track_file)

        audiofile['artist'] = str(info.uploader)
        audiofile['albumartist'] = str(info.uploader)
        audiofile['album'] = str(info.full_title)
        audiofile['title'] = str(info.full_title)
        audiofile.save(v2_version=3)
