"Apply audio metadata"

import eyed3

def apply_album_art(track_file, album_art_file):
    "Embeds album art into the track file"
    audiofile = eyed3.load(track_file)
    if audiofile.tag is None:
        audiofile.initTag()

    audiofile.tag.images.set(3, open(album_art_file, 'rb').read(), 'image/jpeg')
    audiofile.tag.save()

