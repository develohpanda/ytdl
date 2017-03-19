"Apply audio metadata"

import json
import eyed3

def apply_album_art(track_file, album_art_file):
    "Embeds album art into the track file"
    audiofile = eyed3.load(track_file)
    if audiofile.tag is None:
        audiofile.initTag()

    audiofile.tag.images.set(3, open(album_art_file, 'rb').read(), 'image/jpeg')
    audiofile.tag.save()

def apply_track_info(track_file, track_info_file):
    "Sets the appropriate tags in the mp3 file extracting from the track info file"
    audiofile = eyed3.load(track_file)
    if audiofile.tag is None:
        audiofile.initTag()

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
