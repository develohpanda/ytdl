Works on Raspberry Pi Debbie with the default python 3.4.2

Will only download tracks added to playlist since the first time the listen method ran

### Setup aws credentials
``` bash
sudo pip3 install awscli
aws configure
```
### Install ffmpeg ([instructions](https://sebastian.korotkiewicz.eu/2016/09/30/ffmpeg-on-raspbian-raspberry-pi/))
``` bash
sudo apt-get install -y libav-tools
```

### Install this repository
``` bash
pip3 install git+https://github.com/develohpanda/ytdl --process-dependency-links
```

### Setup Gmusic Credentials in Python
``` python
import gmusicapi
gmusicapi.clients.Musicmanager.perform_oauth(False)
```

### Execute the module
``` bash
python3 -m ytdl.listen # this will listen and add to aws queue
python3 -m ytdl.process # this get messages from queue, download tracks, and upload to GPlay
```

### Run as a cronjob
The listening step will run every 2 minutes, the processing step will run every 15 minutes
``` bash
*/2 * * * * python3 -m ytdl.listen
*/15 * * * * python3 -m ytdl.process
```