"Ytdl"

from __future__ import unicode_literals

import json
import logging

from ytdl.audiodownload import AudioDownload
from ytdl.awsqueue import Awsqueue
from ytdl.customerrors import AuthError, DirectoryNotFoundError
from ytdl.gmupload import GoolgeMusicUploader
from ytdl.models import Payload
from ytdl.notify import Iftttnotify
from ytdl.oshelper import absolute_dirs, copy, isdir, remove


class Downloadupload(object):
    "Youtube downloader"

    def __init__(self, ytdl_config):
        self.logger = logging.getLogger(__name__)
        self.ytdl_config = ytdl_config

    def __download_tracks__(self):
        "Downloads any tracks to the download folder"

        messages = Awsqueue(self.ytdl_config.queue_url).get_messages()

        if len(messages) == 0:
            self.logger.info('No messages loaded')
            return False

        self.logger.info('Loaded %d messages', len(messages))
        for message in messages:
            values = json.loads(message.body)
            payload = Payload(values['url'])

            download_result = AudioDownload(
                self.ytdl_config).download(payload.url)

            if download_result.success:
                message.delete()
                self.logger.info(
                    'Message deleted from queue (%s)', download_result.message)
            else:
                self.logger.info(download_result.message)

        return True

    def __upload_tracks__(self):
        "Uploads any tracks in the downloaded folder"

        track_dirs = absolute_dirs(self.ytdl_config.download_folder)
        if len(track_dirs) == 0:
            self.logger.info('No tracks to upload')
            return

        gmu = GoolgeMusicUploader(self.ytdl_config)

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
                    Iftttnotify(self.ytdl_config).send(
                        "Uploaded: {}".format(upload_result.track_name))
                else:
                    message = '[{}] - {} - {}'.format(
                        upload_result.track_name,
                        upload_result.message,
                        upload_result.track_dir)
                    self.logger.warning(message)
                    if "ALREADY_EXISTS" in upload_result.message:
                        self.__failed_upload_tasks__(upload_result.track_dir)
                        Iftttnotify(self.ytdl_config).send(
                            "Track already exists: {}".format(
                                upload_result.track_name)
                        )

        gmu.logout()

    def __successful_upload_tasks__(self, track_file, track_dir):
        if isdir(self.ytdl_config.uploads_folder_path):
            copy(track_file, self.ytdl_config.uploads_folder_path)
            self.logger.info('Track file copied to %s',
                             self.ytdl_config.uploads_folder_path)

        remove(track_dir)
        self.logger.info('Track directory as %s removed', track_dir)

    def __failed_upload_tasks__(self, track_file, track_dir):
        remove(track_dir)
        self.logger.info('Track directory as %s removed', track_dir)

    def download_and_upload(self):
        "Main run method"

        self.logger.info('Starting up')

        while self.__download_tracks__():
            pass

        self.__upload_tracks__()
        self.logger.info('Shutting down')
