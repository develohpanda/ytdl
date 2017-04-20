"Listens to playlist for new tracks"

import logging
from datetime import datetime

import http.client
from googleapiclient.discovery import build
from ytdl.awsqueue import Awsqueue
from ytdl.models import Payload
from ytdl.oshelper import file_exists

import dateutil.parser
import pytz


class Youtubeentity(object):
    "Youtube entity object"

    def __init__(self, title, link, upload_time):
        self.title = title
        self.link = link
        self.upload_time = upload_time


class Playlistlistener(object):
    "Listens to playlist for new tracks"

    def __init__(self, config):
        self.ytdl_config = config
        self.youtube_thing = None
        self.logger = logging.getLogger(__name__)

    def listen_and_add_to_queue(self):
        "Add to queue"
        aws = Awsqueue(self.ytdl_config.queue_url)

        self.youtube_thing = build(
            "youtube", "v3", developerKey=self.ytdl_config.youtube_api_key)

        request = self.youtube_thing.playlistItems().list(
            playlistId=self.ytdl_config.playlist_id,
            part="snippet",
            maxResults=self.ytdl_config.max_youtube_item_load,
            fields="nextPageToken,pageInfo,items(snippet(publishedAt,title,resourceId))"
        )

        entities = []
        last_upload_time = self.__get_last_upload_time__()
        self.logger.info("Last upload time: %s", last_upload_time.isoformat())

        while request:
            response = request.execute()
            has_more = True

            # Print information about each video.
            for playlist_item in response["items"]:
                title = playlist_item["snippet"]["title"]
                upload_time = dateutil.parser.parse(
                    playlist_item["snippet"]["publishedAt"])
                video_id = playlist_item["snippet"]["resourceId"]["videoId"]
                video_link = self.ytdl_config.youtube_video_template + video_id

                entity = Youtubeentity(title, video_link, upload_time)

                if entity.upload_time <= last_upload_time:
                    has_more = False
                    break

                entities.append(entity)

            if has_more:
                request = self.youtube_thing.playlistItems().list_next(request, response)
            else:
                request = None

        self.logger.info("Sending %d messages to queue", len(entities))

        for entity in entities:
            aws.send_message(Payload(entity.link))
            self.__send_notification__(entity.title)

        self.logger.info("Sent %d messages to queue", len(entities))

        if len(entities) > 0:
            self.__save_last_upload_time__(
                max(entity.upload_time for entity in entities))

    def __send_notification__(self, title):
        conn = http.client.HTTPSConnection("maker.ifttt.com")

        payload = "{{ \"value1\" : \"Uploaded: {}\"}}".format(title)

        headers = {
            'content-type': "application/json"
        }

        conn.request("POST",
                     "/trigger/{}/with/key/{}"
                     .format(self.ytdl_config.notification_trigger_name,
                             self.ytdl_config.notification_trigger_key),
                     payload, headers)

        conn.getresponse()

    def __get_last_upload_time__(self):
        if file_exists(self.ytdl_config.listener_time_file_path):
            with open(self.ytdl_config.listener_time_file_path, 'r') as f:
                contents = f.read()
                return dateutil.parser.parse(contents)
        else:
            min_date = datetime.min
            min_date = min_date.replace(tzinfo=pytz.UTC)
            return min_date

    def __save_last_upload_time__(self, last_upload_time):
        with open(self.ytdl_config.listener_time_file_path, 'w') as f:
            f.write(last_upload_time.isoformat())
