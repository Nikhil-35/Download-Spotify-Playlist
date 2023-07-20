import os
import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from googleapiclient.discovery import build
from pytube import YouTube

client_credentials_manager = SpotifyClientCredentials(client_id= "YOUR_ID", client_secret="YOUR_SECRET")
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

playlist_link = sys.argv[1]
playlist_URI = playlist_link.split("/")[-1].split("?")[0]

track_names = [x["track"]["name"] for x in spotify.playlist_tracks(playlist_URI)["items"]]
artists_names = [x["track"]["artists"][0]["name"] for x in spotify.playlist_tracks(playlist_URI)["items"]]

# names and artists name of the songs in playlist
res_list = [track_names[i] + " " +artists_names[i] for i in range(len(track_names))]
res_list = [i for i in res_list if i !=' ']
# print(res_list)

fin_size = len(res_list)

youtube_api_key = "YOUR_YOUTUBE_API_KEY"
youtube = build('youtube','v3',developerKey=youtube_api_key)

#youtube video links of the songs
vid_urls = []

for i in range(fin_size):
    request = youtube.search().list(
        part = 'snippet',
        maxResults = 1,
        q = res_list[i]
    )   
    response = request.execute()
    vid_urls.append("https://www.youtube.com/watch?v="+response["items"][0]['id']['videoId'])
    # print("https://www.youtube.com/watch?v="+response["items"][0]['id']['videoId'])


for link in vid_urls:
    yt = YouTube(link)
    video = yt.streams.filter(only_audio=True).first()
    download_file = video.download(output_path='./playlist')  #files uploaded to playlist folder in same directory

    base, ext = os.path.splitext(download_file)
    new_file = base + '.mp3'
    os.rename(download_file, new_file)


