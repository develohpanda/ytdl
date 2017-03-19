"Apply audio metadata"

import json
import eyed3
import oshelper

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

    def apply_album_art(self, album_art_file):
        "Embeds album art into the track file"

        if album_art_file == oshelper.DEFAULT_FILE_NAME:
            return

        audiofile = self.__load__()

        audiofile.tag.images.set(3, open(album_art_file, 'rb').read(), 'image/jpeg')
        audiofile.tag.save()

    def apply_track_info(self, track_info_file):
        "Sets the appropriate tags in the mp3 file extracting from the track info file"

        if track_info_file == oshelper.DEFAULT_FILE_NAME:
            return

        audiofile = self.__load__()

        info = json.loads(open(track_info_file).read())

        audiofile.tag.artist = info['uploader']
        audiofile.tag.album_artist = info['uploader']
        audiofile.tag.album = info['fulltitle']
        audiofile.tag.title = info['fulltitle']
        audiofile.tag.year = int(info['upload_date'][:4])
        audiofile.tag.comments.set(info['webpage_url'])
        audiofile.tag.save()
