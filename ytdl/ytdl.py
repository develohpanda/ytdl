"Ytdl"

from __future__ import unicode_literals

import datetime
import logging
import oshelper
from audiodownload import AudioDownload
from awsqueue import Awsqueue
from customerrors import AuthError, DirectoryNotFoundError
from gmupload import GoolgeMusicUploader
from models import Payload


class Ytdl(object):
    "Youtube downloader"
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.downloads_path = 'c:\\users\\opend\\ytdl\\downloads'
        self.uploaded_path = 'c:\\users\\opend\\ytdl\\uploaded'

        self.credential_file = '..\\gmusicapi-musicmanager.cred'
        self.mac_address = '09:32:24:12:CD:AA'
        self.queue_url = 'https://sqs.us-east-1.amazonaws.com/342179033824/to-download'

    def __download_tracks__(self):
        "Downloads any tracks to the download folder"

        messages = Awsqueue(self.queue_url).get_messages()

        if len(messages) == 0:
            self.logger.info('No messages loaded')
            return False

        self.logger.info('Loaded %d messages', len(messages))
        for message in messages:
            payload = Payload()
            payload.load(message.body)

            download_result = AudioDownload(self.downloads_path).download(payload.url)

            if download_result.success:
                message.delete()
                self.logger.info('Message deleted from queue (%s)', download_result.message)
            else:
                self.logger.info(download_result.message)

        return True

    def __upload_tracks__(self):
        "Uploads any tracks in the downloaded folder"

        track_dirs = oshelper.absolute_dirs(self.downloads_path)
        if len(track_dirs) == 0:
            self.logger.info('No tracks to upload')
            return

        gmu = GoolgeMusicUploader(self.credential_file, self.mac_address)

        try:
            self.logger.info('Authenticating with Google Play Music')
            gmu.login()
            self.logger.info('Authenticated')
        except AuthError as autherror:
            self.logger.error(autherror)
            return

        self.logger.info('%d tracks to upload', len(track_dirs))
        for track_dir in track_dirs:
            try:
                upload_result = gmu.upload(track_dir)
            except AuthError as auth_error:
                self.logger.error(auth_error)
            except DirectoryNotFoundError as dir_not_found:
                self.logger.error(dir_not_found)
            else:
                if upload_result.success:
                    self.__successful_upload_tasks__(
                        upload_result.track_file,
                        upload_result.track_dir)
                else:
                    message = '[{}] - {} - {}'.format(
                        upload_result.track_name,
                        upload_result.message,
                        upload_result.track_dir)
                    self.logger.warning(message)
        gmu.logout()

    def __successful_upload_tasks__(self, track_file, track_dir):
        oshelper.copy(track_file, self.uploaded_path)
        oshelper.remove(track_dir)
        self.logger.info(
            'Track directory removed, track file copied to %s',
            self.uploaded_path)

    def run(self):
        "Main run method"

        self.logger.info('Starting up')

        while self.__download_tracks__():
            pass

        self.__upload_tracks__()
        self.logger.info('Shutting down')
