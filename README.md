# youtube_downloader
Download movies from YouTube with this script


1. **install pytube**
```
python -m pip install pytube
```
2. You create the `YouTube_Downloader` class element
```
yd = YouTube_Downloader(verbose=True)
```
3. use this Code
```
yd.download_by_txt_file(path='./text.txt')
yd.download_by_txt_file(path='./txtfolder')
```
**or**
```
yd.download_by_url(youtube_url='https://youtube.com/')
```
You can use the following two methods to use download_by_txt_file
1. Put all the links in one file and send its location to this function
2. save the links in separate files and send the folder address to this function

To use download_by_url, you must set URL = URL
