"Models used in the application"

import logging
import json
from oshelper import DEFAULT_FILE_NAME

class TrackInfo(object):
    "Information about a particular track"
    def __init__(self):
        self.uploader = 'Default'
        self.full_title = 'Default'
        self.url = 'Default'
        self.is_default = True
        self.logger = logging.getLogger(__name__)

    def load(self, track_info_file):
        "Loads from a file into the object"

        if track_info_file == DEFAULT_FILE_NAME:
            self.logger.warning('No track info file present')
            return

        info = json.loads(open(track_info_file).read())

        self.uploader = info['uploader']
        self.full_title = info['fulltitle']
        self.url = info['webpage_url']
        self.is_default = False

class Payload(object):
    "The AWS Queue object payload"
    def __init__(self):
        self.title = ''
        self.url = ''

    def load(self, message):
        "Loads from the message content into the object"

        values = json.loads(message)
        self.title = values['title']
        self.url = values['link']

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

class DownloadResult(object):
    "Represents the result of downloading tracks"

    def __init__(self, success, message):
        self.success = success
        self.message = message
