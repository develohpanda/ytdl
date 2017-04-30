"This is used for uploading downloaded track to google play music"

import logging

from gmusicapi import Musicmanager, clients
from audiometadata import AudioMetadata
from customerrors import AuthError, DirectoryNotFoundError
from models import TrackInfo, UploadResult
from oshelper import (DEFAULT_FILE_NAME, absolute_files,
                      get_album_art_file, get_track_file,
                      get_track_info_file, isdir, lock_file_exists)


class GoolgeMusicUploader(object):
    "Google music upload class"

    def __init__(self, config):
        self.credential_file = ''

        if len(config.googleplay_credential_file) > 0:
            self.credential_file = config.googleplay_credential_file
        else:
            self.credential_file = clients.OAUTH_FILEPATH

        self.mac_address = config.mac_address_for_gplay
        self.manager = Musicmanager(False)
        self.logger = logging.getLogger(__name__)

    def login(self):
        "Logs in"

        if not self.manager.login(self.credential_file, self.mac_address):
            raise AuthError(
                'Could not authenticate music manager using {}'.format(
                    self.credential_file))

    def logout(self):
        "Logs out"
        if self.manager.is_authenticated:
            success = self.manager.logout()
            if success:
                self.logger.info('Logged out of Google Play Music')
            else:
                self.logger.warning('Failed to log out of Google Play Music')

    def upload(self, track_dir):
        "Does the upload."

        if not self.manager.is_authenticated:
            raise AuthError(
                "Music Manager not authenticated. Call 'login' first.")

        if not isdir(track_dir):
            raise DirectoryNotFoundError(track_dir)

        files = absolute_files(track_dir)

        info = TrackInfo()
        info.load(get_track_info_file(files))

        track_file = get_track_file(files)

        result = UploadResult(track_dir, track_file, info.full_title)

        if track_file == DEFAULT_FILE_NAME:
            result.set_failure('MP3 Track file not found')
            return result

        locked = lock_file_exists(track_dir)
        if locked:
            result.set_failure('Lock file exists')
            return result

        metadata = AudioMetadata(track_file)
        metadata.apply_album_art(get_album_art_file(files))
        metadata.apply_track_info(info)

        success, message = self.__upload_file__(track_file)
        if success:
            result.set_success(message)
        else:
            result.set_failure(message)
        return result

    def __upload_file__(self, track_file):
        self.logger.info('Uploading %s', track_file)
        upload_result = self.manager.upload(track_file)

        if upload_result[0] != {}:
            return True, upload_result[0]

        elif upload_result[1] != {}:
            return True, upload_result[2]

        elif upload_result[2] != {}:
            reason = list(upload_result[2].items())[0]
            return False, 'Couldn\'t upload {} because {}'.format(reason[0],
                                                                  reason[1])
