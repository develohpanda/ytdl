"Apply audio metadata"

import json
import eyed3
import oshelper
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error

class TrackInfo(object):
    "Information about a particular track"
    def __init__(self, track_info_file):
        self.track_info_file = track_info_file
        self.uploader = ''
        self.full_title = ''
        self.upload_year = 0
        self.url = ''
        self.is_default = True

    def load(self):
        "Loads from a file into the object"

        if self.track_info_file == oshelper.DEFAULT_FILE_NAME:
            return

        info = json.loads(open(self.track_info_file).read())

        self.uploader = info['uploader']
        self.full_title = info['fulltitle']
        self.upload_year = int(info['upload_date'][:4])
        self.url = info['webpage_url']
        self.is_default = False

class AudioMetadata(object):
    "Responsible for applying metadata to file"

    def __init__(self, track_file):
        self.track_file = track_file

    def __load__(self):
        try:
            audiofile = eyed3.load(self.track_file)
        except IOError as ioerror:
            print 'File doesn\'t exist: ' + ioerror.filename
            raise
        else:
            if audiofile.tag is None:
                audiofile.initTag()
            return audiofile

    # def apply_album_art(self, album_art_file):
    #     "Embeds album art into the track file"

    #     if album_art_file == oshelper.DEFAULT_FILE_NAME:
    #         return

    #     audiofile = self.__load__()

    #     audiofile.tag.images.set(3, open(album_art_file, 'rb').read(), 'image/jpeg')
    #     audiofile.tag.save()

    def apply_album_art(self, album_art_file):
        "Embeds album art into the track file"

        if album_art_file == oshelper.DEFAULT_FILE_NAME:
            return

        audio = ID3(self.track_file, v2_version=3)
        audio.save(v2_version=3)

        audio = MP3(self.track_file)
        audio.tags.add(
            APIC(
                encoding=3, # 3 is for utf-8
                mime='image/jpeg', # image/jpeg or image/png
                type=3, # 3 is for the cover image
                desc=u'Cover',
                data=open(album_art_file, 'rb').read()
            ))
        audio.save(v2_version=3)

    def apply_track_info(self, info):
        "Sets the appropriate tags in the mp3 file extracting from the track info file"

        if info.is_default:
            return

        audiofile = self.__load__()

        audiofile.tag.artist = info.uploader
        audiofile.tag.album_artist = info.uploader
        audiofile.tag.album = info.full_title
        audiofile.tag.title = info.full_title
        audiofile.tag.date = info.upload_year
        audiofile.tag.comments.set(info.url)
        audiofile.tag.save()

        return info
