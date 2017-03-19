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

def __upload_tracks__(downloads_path, uploaded_path, credential_file):
    "Uploads any tracks in the downloaded folder"

    track_dirs = oshelper.absolute_dirs(downloads_path)
    if len(track_dirs) == 0:
        return

    print 'Uploading {} tracks'.format(len(track_dirs))

    for track_dir in track_dirs:
        try:
            upload_result = GoolgeMusicUploader(credential_file, track_dir).upload()
        except AuthError as auth_error:
            print auth_error.message
        except DirectoryNotFoundError as dir_not_found:
            print "{} - {}".format(dir_not_found.message, dir_not_found.path)
        else:
            if upload_result.success:
                oshelper.copy_dir_tree(upload_result.track_dir, uploaded_path)
                print 'Uploaded [{}] to gmusic and copied to {}'.format(
                    upload_result.track_name,
                    uploaded_path)
            else:
                #TODO Log to raygun
                print '[{}] - {} - {}'.format(
                    upload_result.track_name,
                    upload_result.message,
                    upload_result.track_dir)

def run():
    "Main run method"
    #TODO Add config file and load data from config file
    home_path = 'c:\\users\\opend\\ytdl'
    downloads_folder = 'downloads'
    uploaded_folder = 'uploaded'
    credential_file = '..\\gmusicapi-musicmanager.cred'

    downloads_path = oshelper.join_paths(home_path, downloads_folder)
    uploaded_path = oshelper.join_paths(home_path, uploaded_folder)

    while __download_tracks__(downloads_path):
        pass

    __upload_tracks__(downloads_path, uploaded_path, credential_file)

run()
