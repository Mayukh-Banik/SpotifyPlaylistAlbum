import json
import os
import argparse
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time
import subprocess
import sys
from datetime import datetime

def save_client_cache(client_id : str, client_secret : str, filename='credentialCache.json') -> None:
    """
    Saves client credentials to a JSON cache file.

    Args:
        client_id (str): Client identifier.
        client_secret (str): Client secret string.
        filename (str): Path to cache file (default: credentialCache.json).
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

def load_client_cache(filename='credentialCache.json')-> (tuple[str, str] | tuple[None, None]):
    """
    Loads client credentials from cache file.

    Args:
        filename (str): Path to cache file (default: credentialCache.json).

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

def cachePlaylistLinks(playlistLink: str, client_id: str, client_secret: str, filename="playlistNamesCache.json") -> None:
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            json.dump({}, f)
    
    try:
        with open(filename, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}

        # Get album links, names, and artist names with load_playlist
        album_links = load_playlist(client_id, client_secret, playlistLink)

        # Create list of tuples: (album_url, album_name, artist_name, False) for download flag
        album_links_with_flags = [(url, name, artist, False) for url, name, artist in album_links]

        # Add/overwrite the playlist entry
        data[playlistLink] = {
            "timestamp": datetime.now().isoformat(),
            "album_links": album_links_with_flags
        }

        # Save the updated data to the file
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

        print(f"Added new playlist: {playlistLink} with album links and artist names.")

    except IOError:
        print("Error opening or writing to file")

    return None

def runDownLoadCommand(albumURL : str, outputDir : str, timeout = 500) -> bool:
    try:
        command = ["python", "-m", "spotdl", albumURL, "--output", outputDir]
        result = subprocess.run(
            command,
            check=True,
            timeout=timeout
        )
    except Exception as e:
        print(e)
        return True
    return True

def loadCachedPlaylist(playlistLink : str, filename = "playlistNamesCache.json") -> None:
    try:
        with open(filename, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
        if playlistLink in data:
            print("Playlist link found in data")
        else:
            print(f"Playlist {playlistLink} not found in cache.")
    except IOError:
        print("Error opening or writing to file")

def manage_playlist_downloads(playlistLink: str, filename="playlistNamesCache.json"):
    try:
        with open(filename, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                print("Error: JSON is malformed.")
                return
    except IOError:
        print("Error opening file.")
        return
    if playlistLink not in data:
        print(f"Playlist {playlistLink} not found in the cache.")
        return
    print(f"\nManaging Playlist: {playlistLink} (Last updated: {data[playlistLink]['timestamp']})")
    album_links = data[playlistLink].get("album_links", [])
    for i, (album_url, album_name, album_artist, download_flag) in enumerate(album_links):
        response = input(f"Would you like to download: {album_name} by {album_artist}? (y/n, default is y): ").strip().lower()
        if response == "n":
            print(f"Deleting {album_name} by {album_artist}")
            album_links.pop(i) 
    data[playlistLink]["album_links"] = album_links
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print("\nUpdated playlist data saved.")
    except IOError:
        print("Error saving to file.")

def load_playlist(client_id: str, client_secret: str, playlist: str) -> set:
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    offset = 0
    limit = 30
    album_data = set()
    while True:
        try:
            playlist_tracks = sp.playlist_tracks(
                playlist, 
                limit=limit, 
                offset=offset, 
                fields="items(track(album(name, external_urls.spotify), artists(name))), total"
            )
            items = playlist_tracks.get('items', [])
            if not items:
                break
            for item in items:
                album_name = item['track']['album']['name']
                album_url = item['track']['album']['external_urls']['spotify']
                artist_name = item['track']['artists'][0]['name']
                print(album_name, artist_name)
                album_data.add((album_url, album_name, artist_name))
            offset += limit
            if offset >= playlist_tracks['total']:
                break
            time.sleep(1)
        except spotipy.exceptions.SpotifyException as e:
            print(f"Error fetching playlist: {e}")
            break
    return album_data

def processPlaylistDownloads(playlistLink: str, outputDir : str, count : int, filename="playlistNamesCache.json"):
    try:
        with open(filename, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                print("Error: JSON is malformed.")
                return
    except IOError:
        print("Error opening file.")
        return
    if playlistLink not in data:
        print(f"Playlist {playlistLink} not found in the cache.")
        return
    print(f"\nManaging Playlist: {playlistLink} (Last updated: {data[playlistLink]['timestamp']})")
    album_links = data[playlistLink].get("album_links", [])
    index : int
    index = 0
    for i, (album_url, album_name, album_artist, download_flag) in enumerate(album_links):
        if index >= count:
            break
        if not download_flag:
            print(f"\nProcessing: {album_name} by {album_artist}...")
            if runDownLoadCommand(album_url, outputDir):
                album_links[i] = (album_url, album_name, album_artist, True)
                print(f"Download for {album_name} by {album_artist} completed and marked as downloaded.")
            else:
                print(f"Failed to download {album_name} by {album_artist}.")
            try:
                with open(filename, "w") as f:
                    json.dump(data, f, indent=4)
                print("Updated playlist data saved after this download.")
            except IOError:
                print("Error saving to file.")
            index = index + 1
    print("\nFinished downloading playlist upto count")

def main():
    parser = argparse.ArgumentParser(description="A tool using Spotdl and Spotify Web API to make either a backup of all albums from a playlist in a JSON format, or to download all albums using Spotdl."
                                     "\n Must have spotdl and spotipy installed through pip, and a spotiy web app account.\n\n"
                                     "Use -i and -s first, then do -p -o -c, afterwards do -p -e and finally do -p -l")
    parser.add_argument("-i", "--client_id", type=str, help="Enter Spotify Client ID.")
    parser.add_argument("-s", "--client_secret", type=str, help="Enter Spotify Client Secret.")
    parser.add_argument("-p", "--playlist", type=str, help="Spotify Playlist Link.")
    parser.add_argument("-o", "--output", type=str, help="Folder Location for where to download, default current directory")
    parser.add_argument("-c", "--cache_link", help="Saves playlist album links in a JSON file. Stored in script local directory under file paylistNamesCache.json", action="store_true")
    parser.add_argument("-e", "--edit_cache", help="CLI for which albums to include or exclude. Must go through every album at once, otherwise none of the changes are saved.", action="store_true")
    parser.add_argument("-l", "--load_link", type=int, help="Uses cached values to download all albums, default value of 10 albums at a time. Ensure its less than 100 otherwise it can take a while.", const=10, nargs="?")

    help_flag_passed = any(arg in sys.argv for arg in ("-h", "--help"))

    args = parser.parse_args()

    if len(sys.argv) == 1 or help_flag_passed:
        parser.print_help()
        sys.exit(0)

    if bool(args.client_id) ^ bool(args.client_secret):
        parser.error("Both --client_id and --client_secret must be provided together.")
    
    if args.client_id and args.client_secret:
        save_client_cache(args.client_id, args.client_secret)
    
    client_id, client_secret = load_client_cache()
    if client_id == None or client_secret == None:
        print("Client ID and Secret Key must be provided for all operations.")
        sys.exit(1)

    playlistLink = args.playlist
    if playlistLink == None:
        print("Playlist link must be provided for all services, except for setting credentials")
        sys.exit(2)

    output = args.output if args.output is not None else os.getcwd()
    
    if args.cache_link:
        cachePlaylistLinks(playlistLink, client_id, client_secret)

    if args.edit_cache:
        manage_playlist_downloads(playlistLink)

    if args.load_link:
        processPlaylistDownloads(playlistLink, output, args.load_link)


if __name__ == "__main__":
    main()