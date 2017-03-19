"This is used for uploading downloaded track to google play music"

import oshelper
import audiometadata
from gmusicapi import Musicmanager

def __upload_file__(track_file):
    manager = Musicmanager()
    manager.login(
        '..\\gmusicapi-musicmanager.cred'
        , '09:32:24:12:CD:AA'
        , 'ytdl-bot')

    upload_result = manager.upload(track_file)

    if upload_result[0] != {}:
        print "Uploaded " + upload_result[0]
        return True

    elif upload_result[1] != {}:
        print "Uploaded and matched " + upload_result[1]
        return True

    elif upload_result[2] != {}:
        reason = list(upload_result[2].viewitems())[0]
        print "Couldn't upload " + reason[0] + " because " + reason[1]
        return False

def upload(trackdir):
    "Does the upload and returns the track id if successfully uploaded."

    files = oshelper.absolute_files(trackdir)

    locked = oshelper.lock_file_exists(files)
    if locked:
        return False

    track_file = oshelper.get_track_file(files)
    if track_file == oshelper.DEFAULT_FILE_NAME:
        return False

    album_art_file = oshelper.get_album_art_file(files)
    if album_art_file != oshelper.DEFAULT_FILE_NAME:
        audiometadata.apply_album_art(track_file, album_art_file)

    track_info_file = oshelper.get_track_info_file(files)
    if track_info_file != oshelper.DEFAULT_FILE_NAME:
        audiometadata.apply_track_info(track_file, track_info_file)

    return __upload_file__(track_file)
