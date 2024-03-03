import os
import csv
from findUrls import get_youtube_url
from download import download_as_mp3, create_playlist_folder
from getPlaylistInfo import get_playlist_info_main

def main():
    get_playlist_info_main()

    find_urls_script = 'findUrls.py'
    os.system(f'python {find_urls_script}')

    csv_file_with_urls = 'song_urls_api.csv'
    with open(csv_file_with_urls, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            youtube_url = row.get('YouTube URL')
            artist = row.get('Artist')
            title = row.get('Name')

            if youtube_url and artist and title:
                output_folder = create_playlist_folder()
                download_as_mp3(youtube_url, artist, title, output_folder)

if __name__ == "__main__":
    main()
