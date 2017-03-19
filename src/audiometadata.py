"Apply audio metadata"

import json
import eyed3

class AudioMetadata(object):
    "Responsible for applying metadata to file"

    def __init__(self, track_file):
        self.track_file = track_file

    def __load__(self):
        audiofile = eyed3.load(self.track_file)
        if audiofile.tag is None:
            audiofile.initTag()
        return audiofile

    def apply_album_art(self, album_art_file):
        "Embeds album art into the track file"

        album_art_file = oshelper.get_album_art_file(files)
        if album_art_file == oshelper.DEFAULT_FILE_NAME:
            return
            
        audiofile = self.__load__()

        audiofile.tag.images.set(3, open(album_art_file, 'rb').read(), 'image/jpeg')
        audiofile.tag.save()

    def apply_track_info(self, track_info_file):
        "Sets the appropriate tags in the mp3 file extracting from the track info file"



        audiofile = self.__load__()

        with open(track_info_file) as info_file:
            info = json.loads(info_file)

        audiofile.tag.artist = info['uploader']
        audiofile.tag.subtitle = info['id']
        audiofile.tag.album = info['uploader']
        audiofile.tag.albumartist = info['uploader']
        audiofile.tag.title = info['fulltitle']
        audiofile.tag.year = info['upload_date'][:4]
        audiofile.tag.comments = info['webpage_url']
        audiofile.tag.save()
