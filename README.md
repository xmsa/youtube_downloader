# youtube_downloader
Download movies from YouTube with this script


1. **install pytube**
```
python -m pip install pytube
```
2. import download_playlist and  download_video_audio from youtube_downloader
```
from youtube_downloader import download_video_audio, download_playlist
```
3. use this Code 
3.1 **for Download Playlist**
```
playlist_url = [] # list of Urls or string of url
BASE_DIR = "."                                                   # set Base Directory
download_playlist(playlist_url,audio=False, BASE_DIR=BASE_DIR)   # for Video Downloader
download_playlist(playlist_url,audio=True, BASE_DIR=BASE_DIR)    # for Audio Downloader
```
3.2 **for Download Video_Audio**

```
Video_or_audio_url = []                                                   # list of Urls or string of url
BASE_DIR = "."                                                            # set Base Directory
name = "directory_name"                                                   # set Directory name
download_video_audio(Video_or_audio_url,audio=False, BASE_DIR=BASE_DIR)   # for Video Downloader
download_video_audio(Video_or_audio_url,audio=True, BASE_DIR=BASE_DIR)    # for Audio Downloader
```

