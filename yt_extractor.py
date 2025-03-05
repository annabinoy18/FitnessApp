import yt_dlp
from yt_dlp.utils import DownloadError

def get_info(url):
    ydl_opts = {}
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            result = ydl.extract_info(url, download=False)
        except DownloadError:
            return None
        
    if "entries" in result:  # Playlist or multiple videos
        video = result["entries"][0]
    else:
        video = result  # Single video
    
    infos = ['id', 'title', 'channel', 'view_count', 'like_count',
             'channel_id', 'duration', 'categories', 'tags']
    
    def key_name(key):
        return "video_id" if key == "id" else key
    
    return {key_name(key): video.get(key, None) for key in infos}


