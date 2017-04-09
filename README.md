### Setup aws credentials
``` bash
sudo pip install awscli
aws configure
```
### Install ffmpeg ([instructions](https://sebastian.korotkiewicz.eu/2016/09/30/ffmpeg-on-raspbian-raspberry-pi/))

### Install this repository
``` bash
pip install git+https://github.com/develohpanda/ytdl --process-dependency-links
```

### Setup Gmusic Credentials in Python
``` python
import gmusicapi
gmusicapi.clients.Musicmanager.perform_oauth(False)
```

### Execute the module
``` bash
python -m ytdl.main
```


