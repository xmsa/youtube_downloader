import os
from pytube import YouTube
from tqdm import tqdm
from pytube import Playlist
# from pytube.contrib.playlist import Playlist


def remove_Duplicate(list_):
    '''Remove Duplicate elements from list_ and return a new list with unique elements.
    Parameters:
        list_: list: List with duplicate elements.
    Returns:
        list: list: List with unique elements.
    '''
    list__ = []
    for i in list_:
        if i in list__:
            continue
        list__.append(i)
    return list__


def download_video_audio(url, BASE_DIR, name="temp", audio=False):
    """Download a single or multi video from youtube and save it in BASE_DIR with name as the folder name.
    Parameters:
        url: str or list: url of the video.
        BASE_DIR: str: Base directory to save the video.
        name: str: Folder name to save the video.
        audio: bool: True to download audio only.
    Returns:
        None: if download is successful.
        str: url of the video if download fails.
    """
    if isinstance(url, list):
        fail_ = []
        url_list = remove_Duplicate(url)
        for url in tqdm(url_list):
            f = download_video_audio(url, BASE_DIR, name, audio)
            if f:
                fail_.append(f)
        return fail_
    dir_path = os.path.join(BASE_DIR, name)

    os.makedirs(dir_path, exist_ok=True)
    try:
        if audio:
            YouTube(url).streams.get_audio_only().download(dir_path)
        else:
            YouTube(url).streams.get_highest_resolution().download(dir_path)
    except KeyboardInterrupt:
        return
    except Exception as ex:
        print("Error: ", ex)
        print(url)
        return url
    return None


def download_playlist(playlist_url, audio=False, BASE_DIR="."):
    """Download a playlist from youtube and save it in BASE_DIR with name as the playlist name.
    Parameters:
        playlist_url: str or list: url or list of the playlist.
        BASE_DIR: str: Base directory to save the playlist.
        audio: bool: True to download audio only.
    Returns:
        Empty list: if download is successful.
        List: url of the video if download fails.
    """
    if isinstance(playlist_url, list):
        fail_ = []
        playlist_url_list = playlist_url
        for playlist_url in tqdm(playlist_url_list):
            f = download_playlist(playlist_url, audio, BASE_DIR)
            fail_ += f
        return fail_
    play_list = Playlist(playlist_url)

    name = play_list.title
    print(name)
    dir_path = os.path.join(BASE_DIR, name)
    os.makedirs(dir_path, exist_ok=True)

    fail_ = []
    for video, url in tqdm(
            zip(play_list.videos, play_list.video_urls), total=len(play_list.videos)):
        try:
            if audio:
                video.streams.get_audio_only().download(dir_path)
            else:
                video.streams.get_highest_resolution().download(dir_path)
        except KeyboardInterrupt:
            return
        except Exception as ex:
            print("Error: ", ex)
            print(url)
            fail_.append(url)
    if len(fail_) > 0:
        print("fail:", fail_)
    print("Done ...")
    return fail_
