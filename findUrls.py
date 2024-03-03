import csv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Replace 'YOUR_API_KEY' with your actual YouTube API key
API_KEY = 'YOUR_API_KEY'
youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_youtube_url(song):
    query = f"{song['Name']} {song['Artist']} official"

    try:
        search_response = youtube.search().list(
            q=query,
            part='id',
            type='video',
            maxResults=1
        ).execute()

        video_id = search_response['items'][0]['id']['videoId']
        return f'https://www.youtube.com/watch?v={video_id}'
    except HttpError as e:
        print(f"Error searching for '{query}': {e}")
        return None

def main():
    csv_file = 'songs.csv'  # Replace with the path to your CSV file
    output_file = 'song_urls_api.csv'

    with open(csv_file, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        header = csv_reader.fieldnames

        if 'YouTube URL' not in header:
            header.append('YouTube URL')

        rows = []
        for row in csv_reader:
            youtube_url = get_youtube_url(row)
            row['YouTube URL'] = youtube_url
            rows.append(row)

    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        csv_writer = csv.DictWriter(file, fieldnames=header)
        csv_writer.writeheader()
        csv_writer.writerows(rows)

    print(f"YouTube URLs written to {output_file}")

if __name__ == "__main__":
    main()
