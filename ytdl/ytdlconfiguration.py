"Config"

import configparser
from os.path import expanduser, exists

from oshelper import join_paths, mkdir

class Ytdlconfiguration(object):
    "Ytdl Configuration"
    def __init__(self):
        self.__home_path__ = expanduser('~')
        self._ytdl_home_path_ = join_paths(self.__home_path__, '.ytdl')
        self.listener_time_file_path = join_paths(self._ytdl_home_path_, 'listener-timestamp.txt')
        self.config_file_path = join_paths(self._ytdl_home_path_, 'config.ini')
        self.download_folder = join_paths(self._ytdl_home_path_, 'downloads')
        self.log_folder = join_paths(self._ytdl_home_path_, 'logs')
        self.yt_time_format = '%Y-%m-%dT%H:%M:%S.%fZ'

        self.googleplay_credential_file = ''
        self.uploads_folder_path = ''
        self.mac_address_for_gplay = ''
        self.queue_url = ''
        self.uploader_name = ''
        self.playlist_id = ''
        self.max_youtube_item_load = 5
        self.youtube_api_key = ''
        self.youtube_video_template = ''

    def load(self):
        "Load from config file"
        config = configparser.ConfigParser()

        if not exists(self.config_file_path):
            configtowrite = configparser.ConfigParser()
            configtowrite['DEFAULT'] = {
                "uploads_folder_path": "",
                "mac_address_for_gplay": "",
                "queue_url": "",
                "googleplay_credential_file": "",
                "uploader_name": "",
                "playlist_id":"",
                "max_youtube_item_load": "",
                "youtube_api_key": "",
                "youtube_video_template": ""
            }

            mkdir(self._ytdl_home_path_)

            with open(self.config_file_path, 'w+') as configfile:
                configtowrite.write(configfile)

        config.read(self.config_file_path)

        self.uploads_folder_path = config['DEFAULT']['uploads_folder_path']
        self.mac_address_for_gplay = config['DEFAULT']['mac_address_for_gplay']
        self.queue_url = config['DEFAULT']['queue_url']
        self.googleplay_credential_file = config['DEFAULT']['googleplay_credential_file']
        self.uploader_name = config['DEFAULT']['uploader_name']
        self.playlist_id = config['DEFAULT']['playlist_id']
        self.max_youtube_item_load = int(config['DEFAULT']['max_youtube_item_load'])
        self.youtube_api_key = config['DEFAULT']['youtube_api_key']
        self.youtube_video_template = config['DEFAULT']['youtube_video_template']

    def is_valid(self):
        "Is a valid config"
        valid = True
        valid = valid and len(self.mac_address_for_gplay) == 17
        valid = valid and len(self.queue_url) > 0
        valid = valid and len(self.uploader_name) > 0
        valid = valid and len(self.youtube_api_key) > 0
        valid = valid and len(self.playlist_id) > 0
        valid = valid and len(self.youtube_video_template) > 0
        return valid
