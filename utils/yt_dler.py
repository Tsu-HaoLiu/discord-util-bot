import yt_dlp

from .utils import remove_special_characters

file_format = {
    'mp4': {
        'format': 'bestvideo*+bestaudio/best',
    },
    'mp3': {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    },
}

def get_title(url):
    ydl_opts = {
        'extract_info': True,
        'skip_download': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)

    # Extract the video title
    video_title = info_dict['title']
    video_title = remove_special_characters(video_title)[:150]

    return video_title


def download_video(url, fmt='mp4', ffmpeg_location=None) -> str:

    file_title = get_title(url)
    # there is a bug with mp4 and mp3 files. mp3 auto apply the .mp3 file format
    # while mp4 do not. We will need to fix it manually (might be fixed in later yt-dl updates)
    custom_format = ""
    if fmt == "mp4":
        custom_format = ".mp4"

    ydl_opts = {
        'outtmpl': f'./{file_title}{custom_format}',
        'merge_output_format': f'{fmt}',
        **file_format[fmt],
        'ffmpeg_location': ffmpeg_location,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(url)

    return f'{file_title}.{fmt}'
