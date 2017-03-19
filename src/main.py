"Main"

import json
import os
import oshelper
import audiodownload
import gmupload
import boto3

def __get_messages__():
    "Checks in queue and downloads tracks to a local folder"

    try:
        sqs = boto3.resource('sqs')
        queue = sqs.Queue('https://sqs.us-east-1.amazonaws.com/342179033824/to-download')
        return queue.receive_messages(MaxNumberOfMessages=10)
    except boto3.exceptions.Boto3Error as awserror:
        #TODO LOG
        print awserror.message
        return []

def __download_tracks__(downloads_path):
    "Downloads any tracks to the download folder"

    messages = __get_messages__()

    if len(messages) == 0:
        print 'No new tracks in queue for download'
        return False

    print 'Downloading {} tracks'.format(len(messages))

    for message in messages:
        payload = json.loads(message.body)
        url = payload['link']

        download_result = audiodownload.AudioDownload(downloads_path).download([url])

        if url in download_result.successful_urls:
            message.delete()

        if url in download_result.failed_urls:
            #TODO LOG
            print 'Failed to download {}'.format(url)
    return True

def __upload_tracks__(downloads_path):
    "Uploads any tracks in the downloaded folder"

    track_dirs = oshelper.absolute_dirs(downloads_path)
    if len(track_dirs) == 0:
        return

    for track_dir in track_dirs:
        upload_result = gmupload.upload(track_dir)
        if upload_result.success:
            os.rmdir(upload_result.track_dir)
        else:
            #TODO LOG
            print '{} - {}'.format(upload_result.message, upload_result.track_dir)

def run():
    "Main run method"
    downloads_path = 'c:/ytdl/downloads'

    while __download_tracks__(downloads_path):
        pass

    __upload_tracks__(downloads_path)
