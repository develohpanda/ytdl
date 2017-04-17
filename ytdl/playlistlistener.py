"Listens to playlist for new tracks"

import logging
from datetime import datetime

import dateutil.parser
import pytz
from googleapiclient.discovery import build

from awsqueue import Awsqueue
from models import Payload
from oshelper import file_exists, join_paths


class Playlistlistener(object):
    "Listens to playlist for new tracks"

    def __init__(self, config):
        self.ytdl_config = config
        self.youtube_thing = None
        self.logger = logging.getLogger(__name__)

    def listen_and_add_to_queue(self):
        "Add to queue"
        aws = Awsqueue(self.ytdl_config.queue_url)

        self.youtube_thing = build("youtube", "v3", developerKey=self.ytdl_config.youtube_api_key)

        request = self.youtube_thing.playlistItems().list(
            playlistId=self.ytdl_config.playlist_id,
            part="snippet",
            maxResults=self.ytdl_config.max_youtube_item_load,
            fields="nextPageToken,pageInfo,items(snippet(publishedAt,resourceId))"
        )

        video_links = []
        upload_times = []
        last_upload_time = self.__get_last_upload_time__()
        self.logger.info("Last upload time: %s", last_upload_time.isoformat())

        while request:
            response = request.execute()
            has_more = True
            
            # Print information about each video.
            for playlist_item in response["items"]:
                upload_time = dateutil.parser.parse(playlist_item["snippet"]["publishedAt"])
                upload_times.append(upload_time)

                if upload_time <= last_upload_time:
                    has_more = False
                    break

                video_id = playlist_item["snippet"]["resourceId"]["videoId"]
                video_link = self.ytdl_config.youtube_video_template + video_id
                video_links.append(video_link)

            if has_more:
                request = self.youtube_thing.playlistItems().list_next(request, response)
            else:
                request = None

        self.logger.info("Sending %d messages to queue", len(video_links))

        for link in video_links:
            aws.send_message(Payload(link))

        self.logger.info("Sent %d messages to queue", len(video_links))

        self.__save_last_upload_time__(max(upload_times))
    
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
