"This is used for uploading downloaded track to google play music"

import oshelper
from customerrors import AuthError, DirectoryNotFoundError
from audiometadata import AudioMetadata, TrackInfo
from gmusicapi import Musicmanager

class UploadResult(object):
    "Represents the result of uploading tracks"

    def __init__(self, track_dir, track_file, track_name):
        self.success = False
        self.track_dir = track_dir
        self.track_file = track_file
        self.track_name = track_name
        self.message = ''

    def set_success(self, message):
        "Sets success properties on the result object"
        self.message = message
        self.success = True

    def set_failure(self, message):
        "Sets failure properties on the result object"
        self.message = message
        self.success = False

class GoolgeMusicUploader(object):
    "Google music upload class"

    def __init__(self, credential_file, track_dir):
        if not oshelper.isdir(track_dir):
            raise DirectoryNotFoundError(track_dir)

        self.track_dir = track_dir
        self.credential_file = credential_file

    def __upload_file__(self, track_file, result):
        manager = Musicmanager(False)
        if not manager.login(self.credential_file, '09:32:24:12:CD:AA', 'ytdl-bot'):
            raise AuthError(
                'Could not authenticate music manager using {}'.format(self.credential_file))

        upload_result = manager.upload(track_file)

        if upload_result[0] != {}:
            result.set_success(upload_result[0])

        elif upload_result[1] != {}:
            result.set_success(upload_result[1])

        elif upload_result[2] != {}:
            reason = list(upload_result[2].viewitems())[0]
            result.set_failure('Couldn\'t upload {} because {}'.format(reason[0], reason[1]))

    def upload(self):
        "Does the upload."

        files = oshelper.absolute_files(self.track_dir)

        info = TrackInfo(oshelper.get_track_info_file(files))
        info.load()

        print 'Uploading {}'.format(info.full_title)

        track_file = oshelper.get_track_file(files)
        result = UploadResult(self.track_dir, track_file, info.full_title)

        if track_file == oshelper.DEFAULT_FILE_NAME:
            result.set_failure('MP3 Track file not found')
            return result

        locked = oshelper.lock_file_exists(self.track_dir)
        if locked:
            result.set_failure('Lock file exists')
            return result

        audio_metadata = AudioMetadata(track_file)
        audio_metadata.apply_track_info(info)
        audio_metadata.apply_album_art(oshelper.get_album_art_file(files))

        self.__upload_file__(track_file, result)
        return result
