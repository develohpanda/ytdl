"Listens to playlist for new tracks"

from googleapiclient.discovery import build
from models import Payload
from awsqueue import Awsqueue

class Playlistlistener(object):
    "Listens to playlist for new tracks"

    def __init__(self, config):
        self.ytdl_config = config
        self.youtube_thing = None

    def listen_and_add_to_queue(self):
        "Add to queue"
        aws = Awsqueue(self.ytdl_config.queue_url)

        self.youtube_thing = build("youtube", "v3", developerKey=self.apikey)

        request = self.youtube_thing.playlistItems().list(
            playlistId=self.ytdl_config.playlist_id,
            part="snippet",
            maxResults=self.ytdl_config.max_youtube_item_load,
            fields="nextPageToken,pageInfo,items(snippet(publishedAt,resourceId))"
        )

        video_links = []

        while request:
            response = request.execute()

            # Print information about each video.
            for playlist_item in response["items"]:
                video_id = playlist_item["snippet"]["resourceId"]["videoId"]
                video_link = str.format(self.ytdl_config.youtube_video_template, video_id)
                video_links.append(video_link)

            request = self.youtube_thing.playlistItems().list_next(request, response)

        for link in video_links:
            aws.send_message(Payload(link))
