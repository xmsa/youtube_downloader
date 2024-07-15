import os
from pytube import YouTube
from pydub import AudioSegment
from pytube import Playlist
# from pytube.contrib.playlist import Playlist
from pytube.innertube import _default_clients
_default_clients["ANDROID_MUSIC"] = _default_clients["ANDROID_CREATOR"]


def run_inside_jupyter():
    try:
        get_ipython = __import__("IPython").get_ipython
        if 'IPKernelApp' not in get_ipython().config:
            return False
    except:
        return False
    return True


if run_inside_jupyter():
    from tqdm.notebook import tqdm
else:
    from tqdm import tqdm


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


def select_resolution(streams, resolution):
    if resolution == "best":
        return streams.filter(progressive=False, file_extension='mp4').order_by(
            'resolution').desc().first()
    elif resolution == "low":
        return streams.filter(file_extension='mp4').order_by(
            'resolution').asc().first()
    elif resolution == "auto":
        return streams.get_highest_resolution()
    else:
        all_resolution = ["1080p", "720p", "480p", "360p", "240p"]
        index = all_resolution.index(resolution)
        all_resolution = all_resolution[index:]
        for resolution in all_resolution:
            s = streams.filter(res=resolution)
            if len(s):
                return s.order_by('resolution').desc().first()


def download_video_audio(url, BASE_DIR, quality="480p", name="temp", audio=False):
    """Download a single or multi video from youtube and save it in BASE_DIR with name as the folder name.
    Parameters:
        url: str or list: url of the video.
        BASE_DIR: str: Base directory to save the video.
        name: str: Folder name to save the video.
        audio: bool: True to download audio only.
        quality: str: Resolution of the video. Default is 480p. auto, best, low, 1080p, 720p, 480p, 360p, 240p.
    Returns:
        None: if download is successful.
        str: url of the video if download fails.
    """
    if isinstance(url, list):
        fail_ = []
        url_list = remove_Duplicate(url)
        for url in tqdm(url_list):
            f = download_video_audio(
                url=url, BASE_DIR=BASE_DIR, quality=quality, name=name, audio=audio)
            if f:
                fail_.append(f)
        return fail_
    dir_path = os.path.join(BASE_DIR, name)

    os.makedirs(dir_path, exist_ok=True)
    try:
        streams = YouTube(url).streams
        if audio:
            streams = streams.filter(
                only_audio=True).order_by('abr').desc().first()
        else:
            streams = select_resolution(streams=streams, resolution=quality)

        streams.download(dir_path)
    except KeyboardInterrupt:
        return
    except Exception as ex:
        print("Error: ", ex)
        print(url)
        return url
    return None


def download_playlist(playlist_url, audio=False, quality="480p", BASE_DIR="."):
    """Download a playlist from youtube and save it in BASE_DIR with name as the playlist name.
    Parameters:
        playlist_url: str or list: url or list of the playlist.
        BASE_DIR: str: Base directory to save the playlist.
        audio: bool: True to download audio only.
        quality: str: Resolution of the video. Default is 480p. auto, best, low, 1080p, 720p, 480p, 360p, 240p.
    Returns:
        Empty list: if download is successful.
        List: url of the video if download fails.
    """
    if isinstance(playlist_url, list):
        fail_ = []
        playlist_url_list = playlist_url
        for playlist_url in tqdm(playlist_url_list):
            f = download_playlist(playlist_url=playlist_url,
                                  audio=audio, quality=quality, BASE_DIR=BASE_DIR)
            fail_ += f
        return fail_
    play_list = Playlist(playlist_url)
    url = list(map(str, play_list.video_urls))
    name = play_list.title
    print(play_list.title)
    fail_ = download_video_audio(
        url=url, BASE_DIR=BASE_DIR, quality=quality, name=name, audio=audio)
    if len(fail_) > 0:
        print("fail:", fail_)

    print("Done ...")
    return fail_


def convert_to_mp3(input_, output_dir=None):
    '''
    Convert a Audio or Video to mp3 format.
    Parameters:
        input_: str: Path of the video.
        output_dir: str: Path to save the mp3 file.
    Returns:
        None: if conversion is successful.
        str: input_ if conversion fails.
    '''

    if output_dir is None:
        if os.path.isfile(input_):
            dir_path = os.path.dirname(input_)
        else:
            if input_.endswith("/"):
                input_ = input_[:-1]
            dir_path = input_
        dir_path_ = os.path.dirname(dir_path)

        output_dir = os.path.join(dir_path_, "mp3")

    if os.path.isdir(input_):
        fail = []
        for i in os.listdir(input_):
            f = convert_to_mp3(os.path.join(input_, i), output_dir=output_dir)
            fail.append(f)
    else:
        try:

            path, filename = os.path.split(input_)
            file_name, file_extension = os.path.splitext(filename)
            dir_path = os.path.dirname(input_)

            output_file = os.path.join(output_dir, file_name + '.mp3')

            audio = AudioSegment.from_file(input_)
            audio.export(output_file, format="mp3")
        except:
            return input_
