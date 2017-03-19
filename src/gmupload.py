"This is used for uploading downloaded track to google play music"

import oshelper
from customerrors import AuthError, DirectoryNotFoundError
from audiometadata import AudioMetadata
from gmusicapi import Musicmanager

class UploadResult(object):
    "Represents the result of uploading tracks"

    def __init__(self, success, track_dir, message):
        self.success = success
        self.track_dir = track_dir
        self.message = message

class GoolgeMusicUploader(object):
    "Google music upload class"

    def __init__(self, track_dir):
        if not oshelper.isdir(track_dir):
            raise DirectoryNotFoundError(track_dir)

        self.track_dir = track_dir

    def __upload_file__(self, track_file):
        credential_file = '..\\gmusicapi-musicmanager.cred'
        manager = Musicmanager()
        if not manager.login(credential_file, '09:32:24:12:CD:AA', 'ytdl-bot'):
            raise AuthError(
                'Could not authenticate music manager using {}'.format(credential_file))

        upload_result = manager.upload(track_file)

        if upload_result[0] != {}:
            return UploadResult(True, self.track_dir, upload_result[0])

        elif upload_result[1] != {}:
            return UploadResult(True, self.track_dir, upload_result[1])

        elif upload_result[2] != {}:
            reason = list(upload_result[2].viewitems())[0]
            return UploadResult(
                False,
                self.track_dir,
                'Couldn\'t upload {} because {}'.format(reason[0], reason[1]))

    def upload(self):
        "Does the upload."

        files = oshelper.absolute_files(self.track_dir)

        locked = oshelper.lock_file_exists(self.track_dir)
        if locked:
            return UploadResult(False, self.track_dir, 'Lock file exists')

        track_file = oshelper.get_track_file(files)
        if track_file == oshelper.DEFAULT_FILE_NAME:
            return UploadResult(False, self.track_dir, 'MP3 Track file not found')

        audio_metadata = AudioMetadata(track_file)
        audio_metadata.apply_album_art(oshelper.get_album_art_file(files))
        audio_metadata.apply_track_info(oshelper.get_track_info_file(files))

        return self.__upload_file__(track_file)
