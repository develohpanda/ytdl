"Config"

import configparser
from os.path import expanduser, exists

from oshelper import join_paths, mkdir

class Ytdlconfiguration(object):
    "Ytdl Configuration"
    def __init__(self):
        self.__home_path__ = expanduser('~')
        self._ytdl_home_path_ = join_paths(self.__home_path__, '.ytdl')
        self.config_file_path = join_paths(self._ytdl_home_path_, 'config.ini')
        self.download_folder = join_paths(self._ytdl_home_path_, 'downloads')
        self.log_folder = join_paths(self._ytdl_home_path_, 'logs')

        self.googleplay_credential_file = ''
        self.uploads_folder_path = ''
        self.mac_address_for_gplay = ''
        self.queue_url = ''
        self.uploader_name = ''

    def load(self):
        "Load from config file"
        config = configparser.ConfigParser()

        if not exists(self.config_file_path):
            configtowrite = configparser.ConfigParser()
            configtowrite['DEFAULT'] = {
                "uploadedfolderpath": "",
                "macaddressforgplay": "",
                "queueurl": "",
                "gplaycredentials": "",
                "uploadername": ""
            }

            mkdir(self._ytdl_home_path_)

            with open(self.config_file_path, 'w+') as configfile:
                configtowrite.write(configfile)

        config.read(self.config_file_path)
        self.uploads_folder_path = config['DEFAULT']['uploadedfolderpath']
        self.mac_address_for_gplay = config['DEFAULT']['macaddressforgplay']
        self.queue_url = config['DEFAULT']['queueurl']
        self.googleplay_credential_file = config['DEFAULT']['gplaycredentials']
        self.uploader_name = config['DEFAULT']['uploadername']

    def is_valid(self):
        "Is a valid config"
        valid = True
        valid = valid and len(self.mac_address_for_gplay) == 17
        valid = valid and len(self.queue_url) > 0
        valid = valid and len(self.uploader_name) > 0
        return valid
