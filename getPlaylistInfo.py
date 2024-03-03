import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.exceptions import SpotifyException
import csv

def connect_to_spotify():
    spotipy_client_id = os.environ.get('SPOTIPY_CLIENT_ID') or False
    spotipy_client_secret = os.environ.get('SPOTIPY_CLIENT_SECRET') or False

    if not spotipy_client_id or not spotipy_client_secret:
        print("Please set SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET")
        print("exiting...")
        exit(1)
        
    auth_manager = SpotifyClientCredentials(client_id=spotipy_client_id, client_secret=spotipy_client_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    return sp

def get_playlist_info(sp, playlist_code):
    
    try:
        playlist_dict = sp.playlist(playlist_code)
        no_of_songs = playlist_dict["tracks"]["total"]
    except SpotifyException as e:
        print(f"Error accessing playlist information: {e}")
        print("exiting...")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        print("exiting...")
        exit(1)
    
    album_list = []
    song_list = []
    release_date_list = []
    artists_list = []

    tracks = playlist_dict["tracks"]
    items = tracks["items"]
    offset = 0
    i = 0

    while i < no_of_songs:
        song = items[i - offset]["track"]["name"]
        album = items[i - offset]["track"]["album"]["name"]
        release_date = items[i - offset]["track"]["album"]["release_date"]
        artists = [k["name"] for k in items[i - offset]["track"]["artists"]]
        artists = ','.join(artists)
        album_list.append(album)
        song_list.append(song)
        release_date_list.append(release_date)
        artists_list.append(artists)

        if (i + 1) % 100 == 0:
            tracks = sp.next(tracks)
            items = tracks["items"]
            offset = i + 1

        i += 1

    final_data = list(zip(song_list, artists_list, album_list, release_date_list))
    return final_data

def write_to_csv(data, output_file="songs.csv"):
    details = ["Name", "Artist", "Album", "Release Date"]
    with open(output_file, 'w', newline='') as f:
        write = csv.writer(f)
        write.writerow(details)
        write.writerows(data)

def get_playlist_info_main():
    sp = connect_to_spotify()
    playlist_code = input("Enter the Playlist Link: \n")
    playlist_info = get_playlist_info(sp, playlist_code)
    write_to_csv(playlist_info)
    print(f"Data written to songs.csv")

if __name__ == "__main__":
    main()
