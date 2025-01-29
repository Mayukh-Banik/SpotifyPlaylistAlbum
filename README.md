# SpotifyPlaylistAlbum

Uses spot-dl https://github.com/spotDL/spotify-downloader to download all albums in a spotify playlist only. Must supply your own spotify API key credentials.

Get Spotify API from:
```
https://developer.spotify.com/
```

And then run:
```
pip install spotdl
python -m spotdl --download-ffmpeg
pip install spotipy
```

After cloning the repository, do:
```
python script.py -i CLIENT_ID -s CLIENT_SECRET
python script.py -p PLAYLIST_LINK -o "OUTPUT DIRECTORY"
```
