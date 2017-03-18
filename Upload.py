"This is used for uploading downloaded track to google play music"

from gmusicapi import Musicmanager

def upload():
    "Does the upload."

    manager = Musicmanager()
    manager.login(
        '..\\gmusicapi-musicmanager.cred'
        , '09:32:24:12:CD:AA'
        , 'ytdl-bot')

    upload_result = manager.upload(
        "E:\\Music\\Good Riddance, Heathens (feat. twent.mp3"
        , True
        , True)

    if upload_result[0] != {}:
        print "Uploaded " + upload_result[0]
    elif upload_result[1] != {}:
        print "Uploaded and matched " + upload_result[1]
    elif upload_result[2] != {}:
        reason = list(upload_result[2].viewitems())[0]
        print "Couldn't upload " + reason[0] + " because " + reason[1]

if __name__ is '__main__':
    upload()
