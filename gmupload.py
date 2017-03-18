"This is used for uploading downloaded track to google play music"

import oshelper
from gmusicapi import Musicmanager

DEFAULT_FILE_NAME = ''

def __get_track_file__(files):
    return next((f for f in files if f.endswith('.mp3')), DEFAULT_FILE_NAME)

def __upload_file__(track_file):
    manager = Musicmanager()
    manager.login(
        '..\\gmusicapi-musicmanager.cred'
        , '09:32:24:12:CD:AA'
        , 'ytdl-bot')

    upload_result = manager.upload(track_file, True, True)

    if upload_result[0] != {}:
        print "Uploaded " + upload_result[0]
        return upload_result[0]

    elif upload_result[1] != {}:
        print "Uploaded and matched " + upload_result[1]
        return upload_result[1]

    elif upload_result[2] != {}:
        reason = list(upload_result[2].viewitems())[0]
        print "Couldn't upload " + reason[0] + " because " + reason[1]
        return ''

def upload(trackdir):
    "Does the upload and returns the track id if successfully uploaded."

    files = oshelper.absolute_files(trackdir)

    track_file = __get_track_file__(files)
    if track_file == DEFAULT_FILE_NAME:
        return

    uploaded_track_id = __upload_file__(track_file)
