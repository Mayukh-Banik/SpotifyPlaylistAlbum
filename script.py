import json
import os
import argparse
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time
import spotdl as Spotdl
import subprocess

def save_client_cache(client_id : str, client_secret : str, filename='client_cache.json') -> None:
    """
    Saves client credentials to a JSON cache file.

    Args:
        client_id (str): Client identifier.
        client_secret (str): Client secret string.
        filename (str): Path to cache file (default: client_cache.json).
    """
    cache_data = {
        'client_id': client_id,
        'client_secret': client_secret
    }

    try:
        with open(filename, 'w') as f:
            json.dump(cache_data, f)
        print("Credentials saved successfully.")
    except IOError as e:
        print(f"Error saving cache: {e}")

def load_client_cache(filename='client_cache.json')-> (tuple[str, str] | tuple[None, None]):
    """
    Loads client credentials from cache file.

    Args:
        filename (str): Path to cache file (default: client_cache.json).

    Returns:
        tuple: (client_id, client_secret) or (None, None) if not found.
    """
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            return data.get('client_id'), data.get('client_secret')
    except FileNotFoundError:
        print("Cache file not found.")
    except json.JSONDecodeError:
        print("Invalid cache format.")
    except Exception as e:
        print(f"Error loading cache: {e}")

    return None, None

def load_playlist(client_id : str, client_secret : str, playlist : str) -> set:
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    offset = 0
    limit = 30
    album_urls = set()
    while True:
        try:
            playlist_tracks = sp.playlist_tracks(
                playlist, 
                limit=limit, 
                offset=offset, 
                fields="items(track(album(external_urls.spotify))), total"
            )
            items = playlist_tracks.get('items', [])
            if not items:
                break  # No more tracks to fetch
            for item in items:
                album_url = item['track']['album']['external_urls']['spotify']
                album_urls.add(album_url)  # Add to set (prevents duplicates)
            offset += limit
            if offset >= playlist_tracks['total']:
                break  
            time.sleep(1)
        except spotipy.exceptions.SpotifyException as e:
            print(f"Error fetching playlist: {e}")
            break
    return album_urls

def main():
    parser = argparse.ArgumentParser(description="A sample CLI tool for managing client credentials.")

    parser.add_argument("-i", "--client_id", type=str, help="Enter Spotify Client ID")
    parser.add_argument("-s", "--client_secret", type=str, help="Enter Spotify Client Secret")
    parser.add_argument("-p", "--playlist", type=str, help="Spotify Playlist Link")
    parser.add_argument("-o", "--output", type=str, help="Folder Location for where to download, default current directory")

    args = parser.parse_args()
    output : str

    if args.output:
        output = args.output
    else:
        output = os.getcwd()


    if args.client_id and args.client_secret:
        save_client_cache(args.client_id, args.client_secret)
    if args.playlist:
        a, b = load_client_cache()
        c = load_playlist(a, b, args.playlist)
        for d in c:
            command = ["python", "-m", "spotdl", d, "--output", output]
            result = subprocess.run(command, text=True)

if __name__ == "main":
    main()