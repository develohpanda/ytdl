"Main"

import json
import os
import oshelper
import audiodownload
import gmupload
import boto3

def __get_messages__():
    "Checks in queue and downloads tracks to a local folder"

    sqs = boto3.resource('sqs')
    queue = sqs.Queue('https://sqs.us-east-1.amazonaws.com/342179033824/to-download')
    return queue.receive_messages(
        MaxNumberOfMessages=10,
        VisibilityTimeout=43200
    )

def __download_tracks__():
    "Downloads any tracks to the download folder"

    messages = __get_messages__()

    if len(messages) == 0:
        print 'No new tracks in queue for download'
        return

    print 'Downloading {} tracks'.format(len(messages))
    for message in messages:
        payload = json.loads(message.body)
        try:
            audiodownload.download([payload['link']])
        except:
            print 'Failed to download [{},{}]'.format(payload['title'], payload['link'])
        else:
            message.delete()


def __upload_tracks__():
    "Uploads any tracks in the downloaded folder"

    downloads_path = 'c:/ytdl/downloads'
    if not os.path.isdir(downloads_path):
        return

    trackdirs = oshelper.absolute_dirs(downloads_path)
    if len(trackdirs) == 0:
        return

    for trackdir in trackdirs:
        try:
            success = gmupload.upload(trackdir)
            if success:
                os.rmdir(trackdir)
        except:
            print 'Failed to upload {}'.format(trackdir)

def run():
    "Main run method"
    __download_tracks__()
    __upload_tracks__()
