from yt_dlp import YoutubeDL


ytdlp = YoutubeDL({'extract_flat':'in_playlist'}) #'playlist_items': '1'

# whatisthis = ytdlp.extract_info("https://www.youtube.com/watch?v=qKL1Z9Ivns4", download=False)
whatisthis = ytdlp.extract_info("https://www.youtube.com/@KivySchool/videos", download=False)
import pdb
pdb.set_trace()
#thumbnail: 'thumbnail'
# hint: search through thumbnail height/widths and find the largest one: 
# whatisthis['entries'][0]['thumbnails'] 

# uploader: 'uploader'-> use channel because the URL is for channels
# channel: whatisthis['channel']
# title: whatisthis['entries'][0]['title']
# view_count: whatisthis['entries'][0]['view_count'] 


# https://github.com/yt-dlp/yt-dlp/issues/8621#issuecomment-1817923337
# from yt_dlp import YoutubeDL

# url = 'https://www.youtube.com/@LinusTechTips/videos'

# ydl_opts = {
#     'playlist_items': '1',
#     'extract_flat': 'in_playlist',
# }

# with YoutubeDL(ydl_opts) as ydl:
#     info = ydl.extract_info(url, download=False)

# print(info['entries'][0]['url'])