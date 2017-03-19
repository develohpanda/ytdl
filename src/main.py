"Main"

import json
import oshelper
from customerrors import AuthError, DirectoryNotFoundError
from audiodownload import AudioDownload
from gmupload import GoolgeMusicUploader
import boto3

def __get_messages__():
    "Checks in queue and downloads tracks to a local folder"

    try:
        sqs = boto3.resource('sqs')
        queue = sqs.Queue('https://sqs.us-east-1.amazonaws.com/342179033824/to-download')
        return queue.receive_messages(MaxNumberOfMessages=10, VisibilityTimeout=300)

    except boto3.exceptions.Boto3Error as awserror:
        #TODO Log to raygun
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

        download_result = AudioDownload(downloads_path).download(url)

        if download_result.success:
            message.delete()
        else:
            #TODO Log to raygun
            print 'Failed to download {}'.format(url)

    return True

def __upload_tracks__(downloads_path):
    "Uploads any tracks in the downloaded folder"

    track_dirs = oshelper.absolute_dirs(downloads_path)
    if len(track_dirs) == 0:
        return

    for track_dir in track_dirs:
        try:
            upload_result = GoolgeMusicUploader(track_dir).upload()
        except AuthError as auth_error:
            print auth_error.message
        except DirectoryNotFoundError as dir_not_found:
            print "{} - {}".format(dir_not_found.message, dir_not_found.path)
        else:
            if upload_result.success:
                pass
                #oshelper.remove(upload_result.track_dir)
            else:
                #TODO Log to raygun
                print '{} - {}'.format(upload_result.message, upload_result.track_dir)

def run():
    "Main run method"
    #TODO Add config file and load data from config file
    home_path = 'c:\\users\\opend'
    downloads_path = 'ytdl\\downloads'
    full_path = oshelper.join_paths(home_path, downloads_path)

    while __download_tracks__(full_path):
        pass

    __upload_tracks__(full_path)

run()
