"Responsible for sending a notification"

import logging

import http.client


class Iftttnotify(object):
    "Sends notification through IFTTT"

    def __init__(self, ytdl_config):
        self.logger = logging.getLogger(__name__)
        self.ytdl_config = ytdl_config

    def send(self, value1="", value2="", value3=""):
        "Sends value1, value2 and value3"

        conn = http.client.HTTPSConnection("maker.ifttt.com")

        payload = "{{ \"value1\" : \"{}\", \"value2\" : \"{}\", \"value3\" : \"{}\",}}".format(
            value1, value2, value3)

        headers = {
            'content-type': "application/json"
        }

        conn.request("POST", "/trigger/{}/with/key/{}".format(
            self.ytdl_config.notification_trigger_name,
            self.ytdl_config.notification_trigger_key),
            payload,
            headers)

        conn.getresponse()
