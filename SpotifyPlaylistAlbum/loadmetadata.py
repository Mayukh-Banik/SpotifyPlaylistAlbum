import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import re
import json

# Authentication
client_id = '25e17729eae1417d8d583abe8d6469e4'
client_secret = 'fcc9a9b065fa4a5da5a4180cb907f7e0'
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

def get_first_10_tracks(playlist_url):
    # Extract playlist ID from URL
    # playlist_id = re.search(r'playlist/(\w+)', playlist_url).group(1)
    
    # Get first page of tracks (up to 100 tracks)
    a = sp.playlist_tracks(playlist_url)
    with open("metadata.txt", "w") as f:
        f.write(json.dumps(a))
    # results = sp.playlist_tracks(playlist_id)
    
    # # Take only first 10 tracks
    # tracks = results['items'][:10]
    
    # # Extract metadata
    # metadata_list = []
    # for track in tracks:
    #     try:
    #         track_info = track['track']
    #         audio_features = sp.audio_features(track_info['id'])[0]
            
    #         metadata = {
    #             'Track Name': track_info['name'],
    #             'Artist': ', '.join([artist['name'] for artist in track_info['artists']]),
    #             'Album': track_info['album']['name'],
    #             'Duration (min)': round(track_info['duration_ms']/60000, 2),
    #             'Popularity': track_info['popularity'],
    #             'Explicit': track_info['explicit'],
    #             'Danceability': audio_features['danceability'],
    #             'Energy': audio_features['energy'],
    #             'Tempo': audio_features['tempo']
    #         }
    #         metadata_list.append(metadata)
    #     except:
    #         continue
    
    # return pd.DataFrame(metadata_list)

# Usage example
playlist_url = "https://open.spotify.com/playlist/2clFmrybJFNDZG5ZHwAueR?si=242f4db8ab4a4248"
# df = get_first_10_tracks(playlist_url)
# print(df)
get_first_10_tracks(playlist_url)