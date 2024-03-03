import os
import csv
import yt_dlp
from datetime import datetime

def download_as_mp3(youtube_url, artist, title, output_folder):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_folder, f'{title} - {artist}.mp3'),
        'ffmpeg_location': '/opt/homebrew/bin/ffmpeg',  # Replace with the actual path to ffmpeg
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([youtube_url])
        except Exception as e:
            print(f"Error downloading '{youtube_url}': {e}")

def create_playlist_folder():
    downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
    playlist_folder_name = 'playlist'
    playlist_folder = os.path.join(downloads_folder, playlist_folder_name)

    if not os.path.exists(playlist_folder):
        os.makedirs(playlist_folder)

    return playlist_folder

if __name__ == "__main__":
    csv_file = 'song_urls.csv'  # Replace with the path to your CSV file
    output_folder = create_playlist_folder()

    with open(csv_file, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            youtube_url = row.get('YouTube URL')
            artist = row.get('Artist')
            title = row.get('Name')
            
            if youtube_url and artist and title:
                download_as_mp3(youtube_url, artist, title, output_folder)
